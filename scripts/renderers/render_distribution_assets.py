import os
import yaml
import qrcode
import base64
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
import vobject
import shutil
import PyPDF2

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'career-data', 'facts')
TEMPLATE_DIR = os.path.join(ROOT_DIR, 'scripts', 'templates')
OUTPUT_DIR = os.path.join(ROOT_DIR, 'recruiter_distribution')

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMPLATE_DIR, exist_ok=True)

def load_canonical_data():
    with open(os.path.join(DATA_DIR, 'identity.yml'), 'r', encoding='utf-8') as f:
        identity = yaml.safe_load(f)

    # Security/Schema Allowlist Validation
    if 'name' not in identity:
        raise ValueError("CRITICAL BLOCKER: 'name' missing.")

    if 'name_structured' not in identity:
        raise ValueError("CRITICAL BLOCKER: 'name_structured' missing.")
    struct = identity['name_structured']
    if 'family' not in struct or 'given' not in struct or 'additional' not in struct:
        raise ValueError("CRITICAL BLOCKER: 'name_structured' must explicitly define family, given, and additional fields.")

    if 'networking_title' not in identity:
        raise ValueError("CRITICAL BLOCKER: 'networking_title' missing.")
    nt = identity['networking_title']
    if 'value' not in nt or 'approved_for' not in nt or 'recruiter_distribution' not in nt['approved_for']:
        raise ValueError("CRITICAL BLOCKER: 'networking_title' lacks explicit recruiter_distribution approval governance.")

    channels = identity.get('contact_channels', {})
    if 'email' not in channels or 'phone' not in channels or 'linkedin' not in channels or 'portfolio' not in channels:
        raise ValueError("CRITICAL BLOCKER: Required public contact channels (email, phone, linkedin, portfolio) missing.")
    if 'wechat' in channels and channels['wechat'].get('public'):
        pass # WeChat is approved

    # Output explicit allowed structure only
    return {
        'name': identity['name'],
        'name_structured': struct,
        'networking_title': nt['value'],
        'email': channels['email']['value'],
        'phone': channels['phone']['value'],
        'linkedin': channels['linkedin']['value'],
        'portfolio': channels['portfolio']['value'],
        'wechat_public': channels.get('wechat', {}).get('public', False)
    }

def generate_vcard(identity):
    v = vobject.vCard()
    v.add('n')
    struct = identity['name_structured']
    v.n.value = vobject.vcard.Name(family=struct['family'], given=struct['given'], additional=struct['additional'])
    v.add('fn')
    v.fn.value = identity['name']

    v.add('title')
    v.title.value = identity['networking_title']

    email = v.add('email')
    email.value = identity['email']
    email.type_param = 'INTERNET'

    tel = v.add('tel')
    tel.value = identity['phone']
    tel.type_param = 'CELL'

    v.add('url')
    v.url.value = identity['portfolio']

    vcard_path = os.path.join(OUTPUT_DIR, 'mo_contact.vcf')
    with open(vcard_path, 'w', encoding='utf-8') as f:
        # Standardize line endings to CRLF as per RFC for exact determinism checks across OS
        content = v.serialize().replace('\r\n', '\n').replace('\n', '\r\n')
        f.write(content)
    print(f"Generated vCard at {vcard_path}")

def generate_portfolio_qr(identity):
    url = identity['portfolio']
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_path = os.path.join(OUTPUT_DIR, 'portfolio_qr.png')
    img.save(qr_path)

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    data_uri = f"data:image/png;base64,{b64}"

    print(f"Generated Portfolio QR at {qr_path}")
    return data_uri

def verify_and_copy_wechat_qr(identity):
    if not identity['wechat_public']:
        return False

    source_path = os.path.join(ROOT_DIR, 'mo-portfolio-v2', 'assets', 'images', 'social', 'wechat-qr.png')
    dest_path = os.path.join(OUTPUT_DIR, 'wechat_qr.png')

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"CRITICAL BLOCKER: Required WeChat QR asset not found at {source_path}. This asset is mandated by the canonical contact policy for China distribution.")

    shutil.copy2(source_path, dest_path)
    print(f"Copied WeChat QR to {dest_path}")
    return True

def check_placeholders(svg_content, filename):
    if '{{' in svg_content or '}}' in svg_content:
        raise ValueError(f"CRITICAL BLOCKER: Unresolved placeholders found in {filename}.")

def generate_networking_card(identity, qr_data_uri, wechat_data_uri):
    # Process Front
    front_template_path = os.path.join(TEMPLATE_DIR, 'networking_card_front.svg')
    with open(front_template_path, 'r', encoding='utf-8') as f:
        front_content = f.read()

    front_content = front_content.replace('{{ NAME }}', identity['name'])
    front_content = front_content.replace('{{ TITLE }}', identity['networking_title'])
    front_content = front_content.replace('{{ EMAIL }}', identity['email'])
    front_content = front_content.replace('{{ PHONE }}', identity['phone'])

    linkedin_val = identity['linkedin'].replace('https://www.', '').replace('https://', '')
    front_content = front_content.replace('{{ LINKEDIN }}', linkedin_val)
    front_content = front_content.replace('{{ PORTFOLIO_URL }}', identity['portfolio'])

    check_placeholders(front_content, 'networking_card_front.svg')

    front_out_path = os.path.join(OUTPUT_DIR, 'networking_card_front.svg')
    with open(front_out_path, 'w', encoding='utf-8') as f:
        f.write(front_content)

    # Process Back
    back_template_path = os.path.join(TEMPLATE_DIR, 'networking_card_back.svg')
    with open(back_template_path, 'r', encoding='utf-8') as f:
        back_content = f.read()

    back_content = back_content.replace('{{ PORTFOLIO_QR_HREF }}', qr_data_uri)
    if wechat_data_uri:
        back_content = back_content.replace('{{ WECHAT_QR_HREF }}', wechat_data_uri)
    else:
        back_content = back_content.replace('{{ WECHAT_QR_HREF }}', '')

    check_placeholders(back_content, 'networking_card_back.svg')

    back_out_path = os.path.join(OUTPUT_DIR, 'networking_card_back.svg')
    with open(back_out_path, 'w', encoding='utf-8') as f:
        f.write(back_content)

    print(f"Generated SVG Masters at {OUTPUT_DIR}")

    # Generate PDF using svglib and reportlab canvas
    import reportlab.rl_config
    reportlab.rl_config.invariant = 1

    pdf_out_path = os.path.join(OUTPUT_DIR, 'networking_card.pdf')

    from reportlab.graphics import renderPDF
    c = canvas.Canvas(pdf_out_path, pagesize=(3.5*inch, 2*inch))

    d_front = svg2rlg(front_out_path)
    if getattr(d_front, 'width', 0):
        scale_x = (3.5*inch) / d_front.width
        scale_y = (2*inch) / d_front.height
        d_front.scale(scale_x, scale_y)
        d_front.width = 3.5*inch
        d_front.height = 2*inch
    renderPDF.draw(d_front, c, 0, 0)
    c.showPage()

    d_back = svg2rlg(back_out_path)
    if getattr(d_back, 'width', 0):
        scale_x = (3.5*inch) / d_back.width
        scale_y = (2*inch) / d_back.height
        d_back.scale(scale_x, scale_y)
        d_back.width = 3.5*inch
        d_back.height = 2*inch
    renderPDF.draw(d_back, c, 0, 0)
    c.save()
    print(f"Generated PDF Print Version at {pdf_out_path}")

    # Assert PDF Dimensions
    with open(pdf_out_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        if len(reader.pages) != 2:
            raise ValueError(f"CRITICAL BLOCKER: Expected 2 pages in PDF, found {len(reader.pages)}")
        for i, page in enumerate(reader.pages):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            # 3.5 inches = 252 points, 2 inches = 144 points
            if abs(width - 252) > 1 or abs(height - 144) > 1:
                raise ValueError(f"CRITICAL BLOCKER: PDF Page {i+1} dimensions incorrect. Expected 252x144, got {width}x{height}")
    print("PDF Assertions Passed: Exactly 2 pages, exactly 3.5x2 inches (252x144 pt).")

def main():
    print("Starting Recruiter Distribution Kit Generation...")
    identity = load_canonical_data()
    generate_vcard(identity)
    qr_data_uri = generate_portfolio_qr(identity)

    source_path = os.path.join(ROOT_DIR, 'mo-portfolio-v2', 'assets', 'images', 'social', 'wechat-qr.png')
    wechat_data_uri = ""
    if verify_and_copy_wechat_qr(identity):
        with open(source_path, "rb") as image_file:
            wechat_b64 = base64.b64encode(image_file.read()).decode('utf-8')
            wechat_data_uri = f"data:image/png;base64,{wechat_b64}"

    generate_networking_card(identity, qr_data_uri, wechat_data_uri)
    print("Generation Complete.")

if __name__ == '__main__':
    main()
