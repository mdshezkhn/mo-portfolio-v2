import os

path = 'mo-portfolio-v2/index.html'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the accidental email replacement
text = text.replace('<span class="cval">Provided on PDF download</span>', '<span class="cval">mdshezkhn@gmail.com</span>')
# Replace the phone number
text = text.replace('+86-131 3771 9002', 'Provided on PDF download')

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated index.html")
