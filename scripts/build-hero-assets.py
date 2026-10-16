#!/usr/bin/env python
"""
build-hero-assets.py — turns the intro video into a seamless looping hero.

Pipeline (guide §3):
  1. Detect the person (or take manual --crop W:H:X:Y) and crop tightly
     around them, head to toe, centred. Scale to 768 px wide.
  2. Whiten the background (colorlevels rimax/gimax/bimax 0.98) so the
     off-white studio backdrop becomes pure white and melts into the page.
  3. Make the loop seamless: take the first N seconds (default 10),
     cross-fade the last 0.5 s of picture into the first 0.5 s
     (ffmpeg xfade); same cross-fade on the audio, sample-accurate in
     numpy (ffmpeg acrossfade can drop audio). Never stretch or retime.
  4. Export hero.mp4 (H.264 yuv420p CRF 24 preset slow, AAC 96k,
     +faststart) and hero.webm (VP9 CRF 36, Opus 80k).
  5. portrait-bust.webp 480x600 (head-to-shirt still) from --portrait
     (or the clearest frame) and og.jpg 1200x630.

Placeholder mode: --placeholder PHOTO builds a silent, seamless
"breathing zoom" clip from a still so the site ships with a real video
before the Google Flow recording exists.

Usage:
  python scripts/build-hero-assets.py intro.mp4 [--crop 800:1000:560:80]
  python scripts/build-hero-assets.py --placeholder assets/photo.webp
"""
import argparse
import array
import json
import math
import shutil
import subprocess
import sys
import wave
from pathlib import Path

try:
    import numpy as np
except ImportError:
    np = None  # only needed when the source has audio

ROOT = Path(__file__).resolve().parent.parent
FF = "ffmpeg"
PROBE = "ffprobe"


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def probe(path: Path) -> dict:
    out = run([PROBE, "-v", "quiet", "-print_format", "json", "-show_streams", str(path)]).stdout
    return json.loads(out)


def size_of(info: dict):
    for s in info["streams"]:
        if s.get("codec_type") == "video":
            return int(s["width"]), int(s["height"])
    raise SystemExit("no video stream found")


def detect_crop(src: Path, at: float = 1.0) -> str:
    """Find the non-white (person) bounding box in a sample frame and build
    a 4:5 crop centred on them, head to toe."""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        frame = Path(f.name)
    try:
        run([FF, "-y", "-ss", str(at), "-i", str(src), "-frames:v", "1", str(frame)])
        from PIL import Image
        im = np.asarray(Image.open(frame).convert("RGB")).astype(int)
        h, w, _ = im.shape
        nonwhite = (im.max(axis=2) < 246)  # any channel clearly below white
        ys, xs = nonwhite.nonzero()
        if len(ys) < 500:
            raise SystemExit("could not detect a person; pass --crop W:H:X:Y manually")
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        pw, ph = x1 - x0, y1 - y0
        margin_x = int(pw * 0.22) + 20
        crop_h = min(h, ph + 2 * int(ph * 0.04) + 16)
        crop_w = min(w, int(crop_h * 0.8), pw + 2 * margin_x)
        crop_w = max(crop_w, int(crop_h * 0.55))          # keep some breathing room
        crop_w = min(crop_w, int(h * 0.8 * (w / h)) if w < h * 0.8 else crop_w)
        crop_w = min(crop_w, w)
        cx = (x0 + x1) // 2
        x = max(0, min(w - crop_w, cx - crop_w // 2))
        y = max(0, min(h - crop_h, y0 - int(ph * 0.03)))
        return f"{crop_w}:{crop_h}:{x}:{y}"
    finally:
        frame.unlink(missing_ok=True)


def crossfade_audio(src: Path, seconds: float, x: float, sr: int = 48000) -> Path | None:
    """Equal-power cross-fade of the last x seconds into the first x seconds,
    sample-accurate, then drop the first x seconds → seamless audio loop."""
    info = probe(src)
    if not any(s.get("codec_type") == "audio" for s in info["streams"]):
        return None
    if np is None:
        print("numpy missing — trying plain copy (loop may click)")
        return None
    raw = run([FF, "-i", str(src), "-t", str(seconds), "-vn", "-ac", "2", "-ar", str(sr),
               "-f", "f32le", "-acodec", "pcm_f32le", "-"]).stdout
    a = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
    n = int(x * sr)
    out = a[: len(a) - n].copy()
    tail = a[len(a) - n:]
    head = a[:n]
    t = np.linspace(0.0, math.pi / 2, n, dtype=np.float32)  # equal power
    blend = (tail * np.cos(t) + head * np.sin(t)).astype(np.float32)
    loop = np.concatenate([out, blend])                      # starts at t=x, ends at state of t=x
    tmp = ROOT / "portfolio-src" / "hero-loop-audio.wav"
    tmp.parent.mkdir(exist_ok=True)
    with wave.open(str(tmp), "wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((np.clip(loop, -1, 1) * 32767).astype("<i2").tobytes())
    return tmp


def build_from_video(src: Path, crop: str | None, seconds: float, x: float, outdir: Path):
    crop = crop or detect_crop(src)
    print(f"[crop] {crop}")
    base = f"crop={crop},scale=768:-2:flags=lanczos,colorlevels=rimax=0.98:gimax=0.98:bimax=0.98,setsar=1"
    seg = outdir.parent / "portfolio-src" / "seg.mp4"
    seg.parent.mkdir(exist_ok=True)
    run([FF, "-y", "-i", str(src), "-t", str(seconds), "-vf", base, "-an",
         "-c:v", "libx264", "-crf", "20", "-preset", "fast", str(seg)])

    dur = float(run([PROBE, "-v", "quiet", "-show_entries", "format=duration",
                     "-of", "csv=p=0", str(seg)]).stdout.strip())
    fade_out = dur - x
    xfaded = seg.parent / "seg-xfade.mp4"
    fc = (
        f"[0:v]split=2[a][b];"
        f"[b]trim=0:{x},setpts=PTS-STARTPTS[head];"
        f"[a][head]xfade=transition=fade:duration={x}:offset={fade_out - x},"
        f"trim={x}:setpts=PTS-STARTPTS[v]"
    )
    run([FF, "-y", "-i", str(seg), "-filter_complex", fc, "-map", "[v]",
         "-an", "-c:v", "libx264", "-crf", "20", "-preset", "fast", str(xfaded)])

    audio = crossfade_audio(src, seconds, x)
    common = ["-map", "0:v:0"]
    if audio:
        common += ["-map", "1:a:0", "-shortest"]
    else:
        print("[audio] none in source → silent loop")

    mp4 = outdir / "hero.mp4"
    run([FF, "-y", "-i", str(xfaded), *( [ "-i", str(audio) ] if audio else [] ), *common,
         "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p",
         *( ["-c:a", "aac", "-b:a", "96k"] if audio else ["-an"] ),
         "-movflags", "+faststart", str(mp4)])
    webm = outdir / "hero.webm"
    run([FF, "-y", "-i", str(xfaded), *( [ "-i", str(audio) ] if audio else [] ), *common,
         "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-row-mt", "1",
         *( ["-c:a", "libopus", "-b:a", "80k"] if audio else ["-an"] ),
         str(webm)])
    print(f"[ok] {mp4} ({mp4.stat().st_size//1024} KB), {webm} ({webm.stat().st_size//1024} KB)")


def build_placeholder(photo: Path, outdir: Path, seconds: float = 10, fps: int = 30):
    """Silent seamless 'breathing zoom' clip from a still (sine in/out)."""
    total = int(seconds * fps)
    z = f"1.035+0.016*sin(2*PI*on/{total})"
    fc = (f"scale=1536:1920:force_original_aspect_ratio=decrease:flags=lanczos,"
          f"pad=1536:1920:(ow-iw)/2:(oh-ih)/2:white,"
          f"zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=768x960:fps={fps},"
          f"colorlevels=rimax=0.98:gimax=0.98:bimax=0.98,setsar=1")
    mp4 = outdir / "hero.mp4"
    run([FF, "-y", "-loop", "1", "-i", str(photo), "-t", str(seconds), "-vf", fc,
         "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", "-an", str(mp4)])
    webm = outdir / "hero.webm"
    run([FF, "-y", "-loop", "1", "-i", str(photo), "-t", str(seconds), "-vf", fc,
         "-c:v", "libvpx-vp9", "-crf", "36", "-b:v", "0", "-row-mt", "1", "-an", str(webm)])
    print(f"[ok] placeholder {mp4.stat().st_size//1024} KB / {webm.stat().st_size//1024} KB")


def build_stills(portrait: Path | None, outdir: Path):
    """portrait-bust.webp 480x600 (head-to-shirt) and og.jpg 1200x630."""
    if portrait and portrait.exists():
        from PIL import Image
        im = Image.open(portrait).convert("RGB")
        w, h = im.size
        # head-to-shirt: top 52% of a head-to-toe portrait, centred
        bust = im.crop((int(w * 0.16), 0, int(w * 0.84), int(h * 0.52)))
        bust = bust.resize((480, 600), Image.LANCZOS)
        bust.save(outdir.parent / "portrait-bust.webp", "WEBP", quality=88)
        print("[ok] portrait-bust.webp (480x600) — adjust crop to taste")
    else:
        print("[skip] no --portrait given; portrait-bust.webp untouched")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?", help="intro video (mp4/mov)")
    ap.add_argument("--crop", help="manual crop W:H:X:Y (source pixels)")
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--x", dest="xfade", type=float, default=0.5, help="cross-fade seconds")
    ap.add_argument("--portrait", type=Path, help="clear photo for the ID-card bust")
    ap.add_argument("--placeholder", type=Path, help="build placeholder video from a still")
    ap.add_argument("--outdir", type=Path, default=ROOT / "public" / "hero")
    a = ap.parse_args()
    a.outdir.mkdir(parents=True, exist_ok=True)

    if a.placeholder:
        build_placeholder(a.placeholder, a.outdir)
        build_stills(a.portrait or a.placeholder, a.outdir)
        return
    if not a.input:
        ap.error("give an intro video, or --placeholder PHOTO")
    build_from_video(Path(a.input), a.crop, a.seconds, a.xfade, a.outdir)
    build_stills(a.portrait, a.outdir)


if __name__ == "__main__":
    main()
