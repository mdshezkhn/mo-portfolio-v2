import yaml

with open('career-data/facts/employment.yml', 'r') as f:
    data = yaml.safe_load(f)

for emp in data['employment_records']:
    if emp['employer_id'] == 'ORG-1000': # Scholars Academy
        emp['cv_highlights'] = [
            'Taught English, Science and Mathematics across upper-primary and secondary classes, adapting instruction for varied learner needs and curriculum requirements',
            'Supported diverse learners through targeted feedback and intervention strategies'
        ]
    elif emp['employer_id'] == 'ORG-1006': # Zhejiang University
        emp['cv_highlights'] = [
            'Taught across multiple school contexts through the Helen China TEFL Network (Zhejiang University)',
            'Adapted teaching strategies for diverse age groups from early years to secondary',
            "Developed students' spoken confidence through structured communicative activities",
            'Applied continuous formative assessment to monitor and support language development'
        ]
    elif emp['employer_id'] == 'ORG-1004': # Eton House
        emp['cv_highlights'] = [
            'Built foundational language skills for kindergarten learners through immersive ESL instruction',
            'Delivered demonstration lessons and mentored colleagues to strengthen early years ESL practice',
            'Created age-appropriate communicative activities for young multilingual learners'
        ]
    elif emp['employer_id'] == 'ORG-1001' and emp['role_id'] == 'ROLE-8003': # Aoxin 2018-2020
        emp['cv_highlights'] = [
            'Delivered foundational EAL and English instruction to primary and lower-secondary learners in a bilingual international school',
            'Directed Grade 5 writing moderation across multiple teaching teams, ensuring consistent assessment standards',
            'Created differentiated learning experiences enabling multilingual learners at varying proficiency levels to progress in their language development',
            'Mentored newly appointed teachers, supporting their successful integration and maintaining instructional quality'
        ]
    elif emp['employer_id'] == 'ORG-1003': # WhiteHat Jr
        emp['cv_highlights'] = [
            'Led teacher-quality and professional-development initiatives across a distributed teaching workforce, using coaching, quality assurance, and LMS data to identify instructional gaps and improve consistency',
            'Created teacher training programmes and curriculum resources for distributed teaching teams',
            'Used classroom observations and LMS analytics to identify teaching trends and improve instructional consistency',
            'Delivered targeted professional development sessions on assessment practices and instructional strategies'
        ]
    elif emp['employer_id'] == 'ORG-1002': # GEDU
        emp['cv_highlights'] = [
            'Led a 15-person trainer team and delivered professional-development programmes reaching 200+ educators across international campuses in the UK, Dubai and Malta',
            'Created and delivered bespoke pedagogical workshops focused on rigorous assessment practices',
            'Developed quality assurance frameworks that strengthened instructional consistency across international campuses'
        ]
    elif emp['employer_id'] == 'ORG-1001' and emp['role_id'] == 'ROLE-8006': # Aoxin 2024-Present
        emp['cv_highlights'] = [
            'Teach primary learners across Years 1–6, supporting access to English-medium Science and Mathematics through language scaffolding and differentiated instruction',
            'Deliver engaging EAL instruction enabling multilingual learners to access the curriculum through English',
            'Plan differentiated curriculum-aligned lessons enabling learners at varied proficiency levels to progress',
            'Use formative assessment to track individual progress, adjust instruction, and ensure each learner works toward appropriate language and content targets',
            'Apply evidence-informed questioning strategies that increase participation and language output among multilingual learners',
            'Collaborate with Chinese co-teachers to strengthen instructional consistency and adapt the school-based curriculum for EAL learners',
            "Report regularly to families with detailed written feedback on each child's language development and next steps"
        ]

with open('career-data/facts/employment.yml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, sort_keys=False, default_flow_style=False, allow_unicode=True)
