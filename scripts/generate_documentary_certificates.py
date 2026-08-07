from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def generate_all_certificates():
    root = Path(__file__).resolve().parent.parent
    cert_dir = root / "mo-portfolio-v2" / "assets" / "images" / "certificates"
    cert_dir.mkdir(parents=True, exist_ok=True)

    certificates_data = [
        {
            "id": "pgce",
            "svg_filename": "pgce-doc.svg",
            "bg_color": "#FCFBFA",
            "border_color": "#1E3A5F",
            "accent_color": "#C5A059",
            "logo_text": "UC",
            "inst_name": "UNIVERSITY OF CUMBRIA",
            "inst_sub": "UNITED KINGDOM",
            "cert_type": "This is to certify that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has been awarded the qualification of",
            "title": "Postgraduate Certificate in Education (PGCE)",
            "sub_title": "Primary Education • Master's Level (60 Credits)",
            "redactions": ["[STUDENT ID REDACTED]", "[CERT NO. REDACTED]"],
            "seal_text": "CUMBRIA",
            "seal_sub": "OFFICIAL SEAL",
            "date": "Date of Award: Academic Year 2025–2026",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        },
        {
            "id": "pgce-transcript",
            "svg_filename": "pgce-transcript-doc.svg",
            "bg_color": "#FAFAFA",
            "border_color": "#1E3A5F",
            "accent_color": "#C5A059",
            "logo_text": "UC",
            "inst_name": "UNIVERSITY OF CUMBRIA — ACADEMIC TRANSCRIPT",
            "inst_sub": "POSTGRADUATE CERTIFICATE IN EDUCATION (PRIMARY)",
            "cert_type": "Official Academic Record",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "Master's Level Modules Completed (60 Credits Total)",
            "title": "PGCE7000 (30 Cr) • PGCE7002 (30 Cr)",
            "sub_title": "Raising Achievement (Pass) • Quality Teaching (Pass - 75%)",
            "redactions": ["[STUDENT NO. REDACTED]", "[TRANSCRIPT AUTH REDACTED]"],
            "seal_text": "ACADEMIC",
            "seal_sub": "TRANSCRIPT",
            "date": "Date Conferred: 9 July 2026",
            "footer": "OFFICIAL ACADEMIC TRANSCRIPT RECORD — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        },
        {
            "id": "bed",
            "svg_filename": "bed-doc.svg",
            "bg_color": "#FFFDF9",
            "border_color": "#2D4A3E",
            "accent_color": "#C5A059",
            "logo_text": "UOK",
            "inst_name": "UNIVERSITY OF KASHMIR",
            "inst_sub": "FACULTY OF EDUCATION",
            "cert_type": "This is to certify that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has been admitted to the degree of",
            "title": "BACHELOR OF EDUCATION (B.ED.)",
            "sub_title": "Professional Teacher Qualification • 2021–2024",
            "redactions": ["[ROLL NO. REDACTED]", "[SERIAL NO. REDACTED]"],
            "seal_text": "",
            "seal_sub": "",
            "date": "Date of Declaration of Result: January 12, 2024",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        },
        {
            "id": "bsc",
            "svg_filename": "bsc-doc.svg",
            "bg_color": "#FCFCFD",
            "border_color": "#1E293B",
            "accent_color": "#C5A059",
            "logo_text": "MU",
            "inst_name": "UNIVERSITY OF MUMBAI",
            "inst_sub": "FACULTY OF SCIENCE",
            "cert_type": "This is to certify that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has passed the examination for the degree of",
            "title": "BACHELOR OF SCIENCE (B.SC. PHYSICS)",
            "sub_title": "Specialization: Physics & Physical Sciences • 2004–2007",
            "redactions": ["[PRN NUMBER REDACTED]", "[SEAT NO. REDACTED]"],
            "seal_text": "MUMBAI",
            "seal_sub": "CONTROLLER",
            "date": "Conferred: June 2007",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        },
        {
            "id": "ma",
            "svg_filename": "ma-doc.svg",
            "bg_color": "#F8FAFC",
            "border_color": "#334155",
            "accent_color": "#D97706",
            "logo_text": "HU",
            "inst_name": "HARRIS UNIVERSITY",
            "inst_sub": "UNITED STATES OF AMERICA",
            "cert_type": "Official Qualification Record",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "Master of Arts Degree Documented",
            "title": "M.A. IN ENGLISH LANGUAGE & LITERATURE",
            "sub_title": "Completed • 2007–2009",
            "redactions": ["[ARCHIVE DOCUMENTATION RETAINED]", "[PUBLIC DISPLAY LIMITED]"],
            "seal_text": "ARCHIVE",
            "seal_sub": "RECORDED",
            "date": "Documented: 2009",
            "footer": "DOCUMENTED QUALIFICATION — SUPPORTING DOCUMENTATION RETAINED IN PROFESSIONAL EVIDENCE ARCHIVE"
        },
        {
            "id": "tesol",
            "svg_filename": "tesol-doc.svg",
            "bg_color": "#FAFAFA",
            "border_color": "#0F2942",
            "accent_color": "#C5A059",
            "logo_text": "GTC",
            "inst_name": "GLOBAL TESOL COLLEGE",
            "inst_sub": "EDMONTON, ALBERTA, CANADA",
            "cert_type": "This certifies that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has successfully completed the advanced professional program for",
            "title": "TESOL CERTIFICATION (240 HOURS)",
            "sub_title": "Specialization: Advanced Primary & Adult EAL Pedagogy",
            "redactions": ["[REG NUMBER REDACTED]", "[QR AUTH REDACTED]"],
            "seal_text": "CANADA",
            "seal_sub": "GTC SEAL",
            "date": "Date of Issue: November 2017",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        },
        {
            "id": "tefl",
            "svg_filename": "tefl-doc.svg",
            "bg_color": "#F8FAFC",
            "border_color": "#1B365D",
            "accent_color": "#C5A059",
            "logo_text": "TR",
            "inst_name": "TEACHER RECORD",
            "inst_sub": "INTERNATIONAL TEFL ACCREDITATION",
            "cert_type": "This is to certify that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has completed 120 hours of instruction in",
            "title": "TEFL CERTIFICATION (120 HOURS)",
            "sub_title": "Teaching English as a Foreign Language",
            "redactions": ["[CERTIFICATE ID REDACTED]", "[VERIFICATION LINK REDACTED]"],
            "seal_text": "TEFL",
            "seal_sub": "VERIFIED",
            "date": "Date of Completion: July 2025",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        },
        {
            "id": "british-council",
            "svg_filename": "british-council-doc.svg",
            "bg_color": "#F0F4F8",
            "border_color": "#002B49",
            "accent_color": "#0091FF",
            "logo_text": "BC",
            "inst_name": "BRITISH COUNCIL",
            "inst_sub": "5 PROFESSIONAL DEVELOPMENT CERTIFICATES COLLECTION",
            "cert_type": "This collection confirms that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has completed 5 professional development modules in",
            "title": "PRIMARY EDUCATION & EAL PEDAGOGY",
            "sub_title": "Assessment, Language Development & Classroom Practice",
            "redactions": ["[COLLECTION ID REDACTED]", "[MODULE CODES REDACTED]"],
            "seal_text": "COUNCIL",
            "seal_sub": "BRITISH",
            "date": "Issued: 2021–2024",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — 5 CERTIFICATES COLLECTION IN EVIDENCE ARCHIVE"
        },
        {
            "id": "unicef",
            "svg_filename": "unicef-doc.svg",
            "bg_color": "#F7FAFC",
            "border_color": "#1C64F2",
            "accent_color": "#00A9E0",
            "logo_text": "UN",
            "inst_name": "UNICEF",
            "inst_sub": "UNITED NATIONS CHILDREN'S FUND",
            "cert_type": "This is to certify that",
            "name": "MOHAMMED SHEHZAD KHAN",
            "award_intro": "has completed the professional learning program for",
            "title": "UNICEF – CHILDREN'S RIGHTS AND CHILD PROTECTION",
            "sub_title": "Child Protection, Equity, Inclusive Education & UN CRC",
            "redactions": ["[RECORD ID REDACTED]", "[DIGITAL SIGNATURE REDACTED]"],
            "seal_text": "UNICEF",
            "seal_sub": "OFFICIAL",
            "date": "Date of Completion: 2024",
            "footer": "DOCUMENTARY EVIDENCE PREVIEW — SENSITIVE IDENTIFIERS REDACTED FOR PRIVACY"
        }
    ]

    for item in certificates_data:
        # 1. Generate SVG
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
  <defs>
    <filter id="shadow_{item['id']}" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.15"/>
    </filter>
    <linearGradient id="grad_{item['id']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{item['bg_color']}"/>
      <stop offset="100%" stop-color="#E2E8F0"/>
    </linearGradient>
  </defs>

  <!-- Parchment Background -->
  <rect width="800" height="560" fill="url(#grad_{item['id']})" rx="8" filter="url(#shadow_{item['id']})"/>
  
  <!-- Outer Double Border -->
  <rect x="20" y="20" width="760" height="520" fill="none" stroke="{item['border_color']}" stroke-width="3" rx="4"/>
  <rect x="28" y="28" width="744" height="504" fill="none" stroke="{item['accent_color']}" stroke-width="1.5" stroke-dasharray="8,4"/>

  <!-- Logo Header -->
  <g transform="translate(400, 75)">
    <circle cx="0" cy="0" r="30" fill="{item['border_color']}"/>
    <text x="0" y="6" font-family="'Fraunces', serif" font-size="12" font-weight="bold" fill="{item['accent_color']}" text-anchor="middle">{item['logo_text']}</text>
  </g>

  <!-- Institution Heading -->
  <text x="400" y="130" font-family="'Fraunces', 'Georgia', serif" font-size="22" font-weight="bold" fill="{item['border_color']}" text-anchor="middle" letter-spacing="1.5">{item['inst_name']}</text>
  <text x="400" y="150" font-family="'Manrope', sans-serif" font-size="11" font-weight="600" fill="#64748B" text-anchor="middle" letter-spacing="2">{item['inst_sub']}</text>

  <!-- Divider Line -->
  <line x1="250" y1="165" x2="550" y2="165" stroke="{item['accent_color']}" stroke-width="1.5"/>

  <!-- Body Text -->
  <text x="400" y="195" font-family="'Georgia', serif" font-size="14" font-style="italic" fill="#475569" text-anchor="middle">{item['cert_type']}</text>
  
  <!-- Candidate Name -->
  <text x="400" y="235" font-family="'Fraunces', 'Georgia', serif" font-size="26" font-weight="bold" fill="#0F172A" text-anchor="middle">{item['name']}</text>

  <text x="400" y="270" font-family="'Georgia', serif" font-size="14" font-style="italic" fill="#475569" text-anchor="middle">{item['award_intro']}</text>

  <!-- Award Title -->
  <text x="400" y="308" font-family="'Fraunces', 'Georgia', serif" font-size="18" font-weight="bold" fill="{item['border_color']}" text-anchor="middle">{item['title']}</text>
  <text x="400" y="332" font-family="'Manrope', sans-serif" font-size="12" font-weight="600" fill="{item['accent_color']}" text-anchor="middle">{item['sub_title']}</text>

  <!-- Redaction Stamps -->
  <g transform="translate(140, 395)">
    <rect width="210" height="26" fill="#0F172A" rx="4"/>
    <text x="105" y="17" font-family="'Manrope', sans-serif" font-size="9" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{item['redactions'][0]}</text>
  </g>

  <g transform="translate(450, 395)">
    <rect width="210" height="26" fill="#0F172A" rx="4"/>
    <text x="105" y="17" font-family="'Manrope', sans-serif" font-size="9" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{item['redactions'][1]}</text>
  </g>

  <!-- Official Seal -->
  <g transform="translate(400, 465)">
    <circle cx="0" cy="0" r="30" fill="none" stroke="{item['accent_color']}" stroke-width="2"/>
    <circle cx="0" cy="0" r="26" fill="none" stroke="{item['accent_color']}" stroke-width="1" stroke-dasharray="4,2"/>
    <text x="0" y="-4" font-family="'Manrope', sans-serif" font-size="8" font-weight="bold" fill="{item['accent_color']}" text-anchor="middle">{item['seal_sub']}</text>
    <text x="0" y="8" font-family="'Fraunces', serif" font-size="10" font-weight="bold" fill="{item['border_color']}" text-anchor="middle">{item['seal_text']}</text>
  </g>

  <!-- Date & Verification Notice -->
  <text x="80" y="490" font-family="'Manrope', sans-serif" font-size="11" fill="#64748B">{item['date']}</text>
  <text x="720" y="490" font-family="'Manrope', sans-serif" font-size="11" fill="#059669" font-weight="bold" text-anchor="end">✓ Documented Evidence</text>

  <!-- Privacy Footer Banner -->
  <rect x="20" y="515" width="760" height="25" fill="{item['border_color']}" rx="0 0 4 4"/>
  <text x="400" y="532" font-family="'Manrope', sans-serif" font-size="9" fill="#E2E8F0" text-anchor="middle" font-weight="500">{item['footer']}</text>
</svg>"""
        
        svg_file = cert_dir / item["svg_filename"]
        svg_file.write_text(svg_content, encoding="utf-8")

        # 2. Generate Raster WebP Derivative Images (full: 1200x840, medium: 800x560, thumbnail: 400x280)
        img_full = Image.new("RGB", (1200, 840), color=item["bg_color"])
        draw = ImageDraw.Draw(img_full)
        
        # Outer Double Border
        draw.rectangle([30, 30, 1170, 810], outline=item["border_color"], width=4)
        draw.rectangle([42, 42, 1158, 798], outline=item["accent_color"], width=2)
        
        # Header Badge
        draw.ellipse([555, 75, 645, 165], fill=item["border_color"])
        draw.text((600, 120), item["logo_text"], fill=item["accent_color"], anchor="mm")
        
        # Titles & Text
        draw.text((600, 200), item["inst_name"], fill=item["border_color"], anchor="mm")
        draw.text((600, 230), item["inst_sub"], fill="#64748B", anchor="mm")
        draw.line([(375, 255), (825, 255)], fill=item["accent_color"], width=2)
        
        draw.text((600, 295), item["cert_type"], fill="#475569", anchor="mm")
        draw.text((600, 355), item["name"], fill="#0F172A", anchor="mm")
        draw.text((600, 405), item["award_intro"], fill="#475569", anchor="mm")
        draw.text((600, 460), item["title"], fill=item["border_color"], anchor="mm")
        draw.text((600, 495), item["sub_title"], fill=item["accent_color"], anchor="mm")
        
        # Redactions
        draw.rectangle([210, 590, 535, 630], fill="#0F172A")
        draw.text((372, 610), item["redactions"][0], fill="#F8FAFC", anchor="mm")
        
        draw.rectangle([665, 590, 990, 630], fill="#0F172A")
        draw.text((827, 610), item["redactions"][1], fill="#F8FAFC", anchor="mm")
        
        # Seal
        draw.ellipse([555, 680, 645, 770], outline=item["accent_color"], width=3)
        draw.text((600, 725), item["seal_text"], fill=item["border_color"], anchor="mm")
        
        # Footer
        draw.rectangle([30, 772, 1170, 810], fill=item["border_color"])
        draw.text((600, 791), item["footer"], fill="#E2E8F0", anchor="mm")
        
        # Save derivative resolutions
        full_path = cert_dir / f"{item['id']}-full.webp"
        medium_path = cert_dir / f"{item['id']}-medium.webp"
        thumb_path = cert_dir / f"{item['id']}-thumbnail.webp"
        
        img_full.save(full_path, "WEBP", quality=92)
        
        img_medium = img_full.resize((800, 560), Image.Resampling.LANCZOS)
        img_medium.save(medium_path, "WEBP", quality=90)
        
        img_thumb = img_full.resize((400, 280), Image.Resampling.LANCZOS)
        img_thumb.save(thumb_path, "WEBP", quality=88)

    print(f"Successfully generated SVGs and WebP derivative images for {len(certificates_data)} items (including PGCE transcript) in {cert_dir}")

if __name__ == "__main__":
    generate_all_certificates()
