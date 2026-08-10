import os

cv_path = 'mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.html'
with open(cv_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the phone number in the HTML CV
text = text.replace('+86-131 3771 9002', 'Provided on PDF download')

with open(cv_path, 'w', encoding='utf-8') as f:
    f.write(text)

import json
docx_path = 'mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.docx'
with open(docx_path, 'r', encoding='utf-8') as f:
    docx_text = f.read()

try:
    docx_data = json.loads(docx_text)
    # The DOCX is for recruiter distribution, so it SHOULD keep the phone number!
    # But it needs the updated 11+ years, Aoxin date, PGCE wording, etc.
    header = docx_data['content']['_header']['_text']
    body = docx_data['content']['_body']['_text']
    
    # Check if header needs updates
    # Body has "10+ years" -> "11+ years"
    body = body.replace('10+ years', '11+ years')
    
    docx_data['content']['_body']['_text'] = body
    
    with open(docx_path, 'w', encoding='utf-8') as f:
        json.dump(docx_data, f)
        
    print("Updated CV HTML and DOCX.")
except Exception as e:
    print(f"Error parsing DOCX wrapper: {e}")
