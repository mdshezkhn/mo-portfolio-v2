import re

with open('mo-portfolio-v2/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print('ACT II:', content.find('        <!-- ACT II'))
print('journey:', content.find('        <section id="journey"'))
print('ACT III:', content.find('        <!-- ACT III'))
print('credentials:', content.find('        <section id="credentials"'))
print('ACT IV:', content.find('        <!-- ACT IV'))

