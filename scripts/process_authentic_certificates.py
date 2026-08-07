import os
from pathlib import Path
from PIL import Image, ImageDraw

def process_certificates():
    root = Path(__file__).resolve().parent.parent
    src_dir = root / "temp_certs" / "word" / "media"
    dest_dir = root / "mo-portfolio-v2" / "assets" / "images" / "certificates"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    redactions = {
        "image1.png": [ # B.Ed (Kashmir)
            (0.04, 0.02, 0.35, 0.04), # Top left Sr No
            (0.40, 0.02, 0.10, 0.03), # Top center No
            (0.60, 0.02, 0.35, 0.04), # Top right No
            (0.40, 0.77, 0.20, 0.13)  # QR Code bottom
        ],
        "image2.png": [ # B.Sc (Mumbai)
            (0.05, 0.88, 0.20, 0.05), # Bottom left barcode
            (0.80, 0.88, 0.15, 0.05)  # Bottom right number
        ],
        "image3.png": [ # MA (Harris)
            # No obvious redaction needed
        ],
        "image4.png": [ # PGCE (Cumbria)
            (0.02, 0.88, 0.15, 0.05) # Bottom left number
        ],
        "image5.png": [ # TEFL
            (0.04, 0.01, 0.15, 0.12), # QR code top left
            (0.35, 0.90, 0.50, 0.04)  # Cert number
        ],
        "image6.png": [ # Adv TESOL
            (0.10, 0.65, 0.25, 0.05) # Cert ID
        ],
        "image7.png": [ # Spec TESOL
            (0.10, 0.65, 0.25, 0.05) # Cert ID
        ],
        "image8.png": [ # Found TESOL
            (0.10, 0.67, 0.25, 0.05) # Cert ID
        ],
        "image9.png": [ # UNICEF
        ]
    }
    
    output_mapping = {
        "image1.png": "bed",
        "image2.png": "bsc",
        "image3.png": "ma",
        "image4.png": "pgce",
        "image5.png": "tefl",
        "image6.png": "tesol-adv",
        "image7.png": "tesol-bus",
        "image8.png": "tesol-found",
        "image9.png": "unicef"
    }

    for img_name, out_name in output_mapping.items():
        img_path = src_dir / img_name
        if not img_path.exists():
            continue
            
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            draw = ImageDraw.Draw(img)
            width, height = img.size
            
            for (px, py, pw, ph) in redactions.get(img_name, []):
                x = int(px * width)
                y = int(py * height)
                w = int(pw * width)
                h = int(ph * height)
                draw.rectangle([x, y, x+w, y+h], fill="#1a1a1a")
                
            full_w = min(1600, width)
            full_ratio = full_w / float(width)
            full_h = int(float(height) * float(full_ratio))
            img_full = img.resize((full_w, full_h), Image.Resampling.LANCZOS)
            img_full.save(dest_dir / f"{out_name}-doc-full.webp", format="WEBP", quality=85)
            
            med_w = min(800, width)
            med_ratio = med_w / float(width)
            med_h = int(float(height) * float(med_ratio))
            img_med = img.resize((med_w, med_h), Image.Resampling.LANCZOS)
            img_med.save(dest_dir / f"{out_name}-doc-med.webp", format="WEBP", quality=80)

            thumb_w = min(400, width)
            thumb_ratio = thumb_w / float(width)
            thumb_h = int(float(height) * float(thumb_ratio))
            img_thumb = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            img_thumb.save(dest_dir / f"{out_name}-doc-thumb.webp", format="WEBP", quality=75)

            print(f"Processed {out_name}")

if __name__ == '__main__':
    process_certificates()
