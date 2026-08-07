import os
import yaml
from pathlib import Path

FIXTURE_DIR = Path('tests/fixtures/v1/minimal/facts')
FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

facts = {
    'identity.yml': {
        'id': 'ID-001',
        'entity_type': 'Identity',
        'name': 'Jane Doe',
        'email': 'jane@example.com'
    },
    'organisations.yml': [
        {
            'id': 'ORG-001',
            'entity_type': 'Organisation',
            'name': 'Tech Corp',
            'industry': 'Technology'
        }
    ],
    'roles.yml': [
        {
            'id': 'ROL-001',
            'entity_type': 'Role',
            'title': 'Senior Engineer'
        }
    ],
    'employment.yml': [
        {
            'id': 'EMP-001',
            'entity_type': 'Employment',
            'employer_id': 'ORG-001',
            'role_id': 'ROL-001',
            'start_date': '2020-01-01',
            'end_date': '2023-01-01',
            'status': 'Completed'
        }
    ],
    'institutions.yml': [
        {
            'id': 'INS-001',
            'entity_type': 'Institution',
            'name': 'Tech University'
        }
    ],
    'education.yml': [
        {
            'id': 'EDU-001',
            'entity_type': 'Qualification',
            'institution_id': 'INS-001',
            'degree': 'BSc Computer Science',
            'start_year': 2015,
            'end_year': 2019
        }
    ],
    'certifications.yml': [
        {
            'id': 'CRT-001',
            'entity_type': 'Certification',
            'name': 'Cloud Expert',
            'issuer_id': 'ORG-001',
            'issue_date': '2021-06-01'
        }
    ],
    'evidence.yml': [
        {
            'id': 'EVD-001',
            'entity_type': 'Evidence',
            'target_id': 'EMP-001',
            'type': 'Reference Letter',
            'status': 'Verified'
        }
    ],
    'competencies.yml': [
        {
            'id': 'CMP-001',
            'entity_type': 'Competency',
            'name': 'System Architecture',
            'level': 'Expert'
        }
    ],
    'narratives.yml': [
        {
            'id': 'NAR-001',
            'entity_type': 'Narrative',
            'target_id': 'EMP-001',
            'content': 'Led the migration to microservices.'
        }
    ]
}

for filename, content in facts.items():
    filepath = FIXTURE_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        # Avoid yaml output variations
        yaml.dump(content, f, default_flow_style=False, sort_keys=False)
        
print(f"Created minimal fixture at {FIXTURE_DIR}")
