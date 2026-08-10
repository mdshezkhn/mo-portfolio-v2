import json

data = {
  "title": "Master",
  "asset_name": "CV_Master_v2.0",
  "subtitle": "International Primary Educator | EAL & English | Curriculum & Assessment",
  "claims": [
    "C-001", "C-002", "C-003", "C-004", "C-005", "C-006", "C-007", "C-008", 
    "C-009", "C-010", "C-011", "C-012", "C-013", "C-014", "C-017", "C-019", 
    "C-020", "C-021", "C-022", "C-023"
  ],
  "summary": "International Primary EAL educator with 11+ years of experience across China and India, including primary classroom teaching, multilingual learner support, curriculum development, formative assessment, and teacher development. Experienced in helping EAL learners access the wider curriculum through English and in strengthening instructional quality through mentoring, assessment moderation, and professional learning. Holds a PGCE from the University of Cumbria and is available for August 2027 opportunities.",
  "competencies": [
    "Primary EAL | Multilingual Education | Curriculum Design | Differentiated Instruction | Formative Assessment | Literacy Development | Classroom Management | Assessment Moderation | Teacher Mentoring | Professional Development | Instructional Quality Assurance | Cross-Curricular STEM | Dialogic Teaching | Questioning Strategies | Translanguaging"
  ],
  "experience": [
    {
      "company": "Aoxin International School",
      "date": "February 2024 — Present",
      "title": "EAL / English Teacher",
      "bullets": [
        "Teach primary learners across Years 1–6, supporting access to English-medium Science and Mathematics through language scaffolding and differentiated instruction",
        "Deliver engaging EAL instruction enabling multilingual learners to access the curriculum through English",
        "Plan differentiated curriculum-aligned lessons enabling learners at varied proficiency levels to progress",
        "Use formative assessment to track individual progress, adjust instruction, and ensure each learner works toward appropriate language and content targets",
        "Apply evidence-informed questioning strategies that increase participation and language output among multilingual learners",
        "Collaborate with Chinese co-teachers to strengthen instructional consistency and adapt the school-based curriculum for EAL learners",
        "Report regularly to families with detailed written feedback on each child's language development and next steps"
      ]
    },
    {
      "company": "GEDU Global Education",
      "date": "2022 — 2023",
      "title": "Training and Quality Lead",
      "bullets": [
        "Led a 15-person trainer team and delivered professional-development programmes reaching 200+ educators across international campuses in the UK, Dubai and Malta",
        "Created and delivered bespoke pedagogical workshops focused on rigorous assessment practices",
        "Developed quality assurance frameworks that strengthened instructional consistency across international campuses"
      ]
    },
    {
      "company": "WhiteHat Jr (A BYJU'S Company)",
      "date": "2020 — 2022",
      "title": "Assistant Manager — Teacher Quality and Development",
      "bullets": [
        "Led teacher-quality and professional-development initiatives across a distributed teaching workforce, using coaching, quality assurance, and LMS data to identify instructional gaps and improve consistency",
        "Created teacher training programmes and curriculum resources for distributed teaching teams",
        "Used classroom observations and LMS analytics to identify teaching trends and improve instructional consistency",
        "Delivered targeted professional development sessions on assessment practices and instructional strategies"
      ]
    },
    {
      "company": "Aoxin International School",
      "date": "July 2018 — August 2020",
      "title": "EAL / English Teacher",
      "bullets": [
        "Delivered foundational EAL and English instruction to primary and lower-secondary learners in a bilingual international school",
        "Directed Grade 5 writing moderation across multiple teaching teams, ensuring consistent assessment standards",
        "Created differentiated learning experiences enabling multilingual learners at varying proficiency levels to progress in their language development",
        "Mentored newly appointed teachers, supporting their successful integration and maintaining instructional quality"
      ]
    },
    {
      "company": "Eton House Kindergarten",
      "date": "2017 — 2018",
      "title": "ESL Teacher and Teacher Trainer",
      "bullets": [
        "Built foundational language skills for kindergarten learners through immersive ESL instruction",
        "Delivered demonstration lessons and mentored colleagues to strengthen early years ESL practice",
        "Created age-appropriate communicative activities for young multilingual learners"
      ]
    },
    {
      "company": "Zhejiang University — Helen China TEFL Network",
      "date": "2016 — 2017",
      "title": "ESL Teacher",
      "bullets": [
        "Taught across multiple school contexts through the Helen China TEFL Network (Zhejiang University)",
        "Adapted teaching strategies for diverse age groups from early years to secondary",
        "Developed students' spoken confidence through structured communicative activities",
        "Applied continuous formative assessment to monitor and support language development"
      ]
    },
    {
      "company": "Scholars Academy",
      "date": "2014 — 2016",
      "title": "English, Science and Mathematics Teacher",
      "bullets": [
        "Taught English, Science and Mathematics across upper-primary and secondary classes, adapting instruction for varied learner needs and curriculum requirements",
        "Supported diverse learners through targeted feedback and intervention strategies"
      ]
    }
  ],
  "education": [
    "Postgraduate Certificate in Education (PGCE) — Primary Education, University of Cumbria, UK (2025 — 2026). Postgraduate professional qualification (PGCE7002)",
    "Bachelor of Education (B.Ed.), University of Kashmir (2021 — 2024)",
    "M.A. English Language and Literature, Harris University, USA (2007 — 2009)",
    "B.Sc. Physics, Mumbai University (2004 — 2007)",
    "TESOL Certification (240 hours), Global TESOL College, Canada",
    "TEFL Certification (120 hours), Teacher Record"
  ]
}

with open('templates/cv/profiles/master.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
