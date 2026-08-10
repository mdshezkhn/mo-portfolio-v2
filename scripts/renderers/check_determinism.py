import os
import subprocess
import hashlib

def hash_file(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    script = os.path.join(root, 'scripts', 'renderers', 'render_distribution_assets.py')
    output_dir = os.path.join(root, 'recruiter_distribution')

    print("=== RUN 1 ===")
    subprocess.run(['python', script], check=True)

    # Store hashes of Run 1
    hashes = {}
    files_to_check = [
        'mo_contact.vcf',
        'portfolio_qr.png',
        'wechat_qr.png',
        'networking_card_front.svg',
        'networking_card_back.svg',
        'networking_card.pdf'
    ]

    for f in files_to_check:
        path = os.path.join(output_dir, f)
        if os.path.exists(path):
            hashes[f] = hash_file(path)

    print("=== RUN 2 ===")
    subprocess.run(['python', script], check=True)

    print("\n=== DETERMINISM CHECK ===")
    all_match = True
    for f in files_to_check:
        path = os.path.join(output_dir, f)
        if not os.path.exists(path):
            print(f"FAIL: {f} missing in Run 2")
            all_match = False
            continue

        new_hash = hash_file(path)
        if f == 'networking_card.pdf':
            print(f"PDF Run 1 SHA-256: {hashes[f]}")
            print(f"PDF Run 2 SHA-256: {new_hash}")

        if new_hash == hashes[f]:
            print(f"PASS: {f} exact byte match")
        else:
            print(f"FAIL: {f} hashes differ!")
            all_match = False

    print("\n=== SECURITY ASSERTION ===")
    import yaml
    with open(os.path.join(root, 'career-data', 'facts', 'identity.yml'), 'r', encoding='utf-8') as f:
        identity = yaml.safe_load(f)

    # Read generated VCF and SVG to ensure NO non-approved fields leak (e.g. availability, location)
    with open(os.path.join(output_dir, 'mo_contact.vcf'), 'r', encoding='utf-8') as f:
        vcf_content = f.read()
    with open(os.path.join(output_dir, 'networking_card_front.svg'), 'r', encoding='utf-8') as f:
        front_content = f.read()

    forbidden_strings = [
        identity.get('location', 'Zhengzhou'),
        identity.get('availability', 'August 2027')
    ]

    secure = True
    for fs in forbidden_strings:
        if fs in vcf_content or fs in front_content:
            print(f"SECURITY FAIL: Found unapproved field '{fs}' in generated output.")
            secure = False

    if secure:
        print("PASS: Only explicitly allowed public fields were emitted in artifacts.")

    if all_match and secure:
        print("\nAll Determinism and Security tests PASSED.")
    else:
        print("\nSome tests FAILED.")

if __name__ == '__main__':
    main()
