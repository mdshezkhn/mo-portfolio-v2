import re

with open('mo-portfolio-v2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

sections = ['hero', 'story', 'journey', 'impact', 'credentials', 'philosophy']
for s in sections:
    match = re.search(f'<section id=\"{s}\"', content)
    if match:
        print(f'{s}: {match.start()}')
