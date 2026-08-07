import re, os
html_path = 'mo-portfolio-v2/index.html'
cert_dir = 'mo-portfolio-v2/assets/images/certificates/'
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find all references to assets/images/certificates/
pattern = re.compile(r'assets/images/certificates/([^\"\'\s\>]+)')
matches = set(pattern.findall(content))

print('HTML Reference Check against Disk:')
print('-'*50)
all_found = True
for match in sorted(matches):
    full_path = os.path.join(cert_dir, match)
    exists = os.path.exists(full_path)
    if not exists:
        all_found = False
    status = 'FOUND' if exists else 'MISSING'
    print(f'{match.ljust(30)} : {status}')

print('-'*50)
if all_found:
    print('All referenced images exist on disk.')
else:
    print('Some referenced images are MISSING.')
