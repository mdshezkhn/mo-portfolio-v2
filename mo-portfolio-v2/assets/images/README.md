# images/

All website images organized by category.

## Naming Convention

Use descriptive, lowercase, hyphenated filenames:

```
✅ profile-headshot-2026.webp
✅ classroom-reading-grade6-2025.webp
✅ teacher-training-gedu-2023.webp

❌ IMG_3847.jpg
❌ photo1.jpg
❌ final_FINAL_v2.jpg
```

## Subfolders

| Folder | Contents | Recommended Format | Max Size |
|---|---|---|---|
| `profile/` | Headshots and portraits | WebP | 200KB |
| `hero/` | Hero section backgrounds | WebP | 400KB |
| `classroom/` | Classroom photography | WebP | 300KB |
| `leadership/` | PD, training, leadership events | WebP | 300KB |
| `gallery/` | General gallery photos | WebP | 300KB |
| `certificates/` | Certificate thumbnail previews | WebP | 100KB |
| `logos/` | School and organisation logos | WebP/SVG | 50KB |
| `timeline/` | Timeline event photos | WebP | 200KB |
| `projects/` | Project and curriculum screenshots | WebP | 200KB |
| `screenshots/` | Tool, platform, LMS screenshots | WebP | 200KB |
| `social/` | Social media preview image (1200×630px) | WebP | 200KB |

## Performance Notes

- Hero portrait (`profile/`) is loaded `eager` — keep under 200KB.
- All other images use `loading="lazy"` — can be slightly larger but compress where possible.
- Preferred format: WebP. Fall back to JPEG for photos, PNG for logos with transparency.
- Always include explicit `width` and `height` attributes in HTML to prevent layout shift.
