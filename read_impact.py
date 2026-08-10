import re

with open('mo-portfolio-v2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

s_impact = content.find('        <!-- ACT III — THE EVIDENCE')
s_journey = content.find('        <section id="journey"')

print(content[s_impact:s_journey])
