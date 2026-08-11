import pytest
import json
import yaml
from pathlib import Path
import subprocess

def run_build_domain_model():
    subprocess.run(["python", "scripts/builders/build_domain_model.py"], check=True)

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def test_single_role_resolution():
    roles_data = load_yaml(Path("career-data/facts/roles.yml"))
    emp_data = load_yaml(Path("career-data/facts/employment.yml"))
    
    valid_roles = {r['id']: r for r in roles_data['roles']}
    
    for emp in emp_data['employment_records']:
        assert 'role_id' in emp, f"Employment {emp['id']} missing role_id"
        assert emp['role_id'] in valid_roles, f"Employment {emp['id']} has invalid role_id {emp['role_id']}"
        assert isinstance(emp['role_id'], str)

def test_whitehat_title_invariant():
    roles_data = load_yaml(Path("career-data/facts/roles.yml"))
    emp_data = load_yaml(Path("career-data/facts/employment.yml"))
    
    valid_roles = {r['id']: r for r in roles_data['roles']}
    whitehat_emp = next((e for e in emp_data['employment_records'] if e['id'] == 'EMP-2004'), None)
    
    assert whitehat_emp is not None
    assert valid_roles[whitehat_emp['role_id']]['title'] == 'Assistant Manager — Teacher Quality & Development'

def test_empty_claims_preserve_employment_record():
    run_build_domain_model()
    
    with open('artifacts/cv_view_models/portfolio.json', 'r', encoding='utf-8') as f:
        portfolio = json.load(f)
        
    emp_2003 = next((e for e in portfolio['experience'] if 'Aoxin International School' in e['company'] and '2018' in e['date']), None)
    assert emp_2003 is not None, "EMP-2003 should be preserved despite zero claims"
    assert len(emp_2003['bullets']) == 0, "Zero verified claims must produce zero unsupported achievement bullets"

def test_cascade_all_employers():
    run_build_domain_model()
    
    with open('artifacts/cv_view_models/master.json', 'r', encoding='utf-8') as f:
        master = json.load(f)
    
    with open('artifacts/cv_view_models/portfolio.json', 'r', encoding='utf-8') as f:
        portfolio = json.load(f)

    expected_employers = [
        ("Aoxin International School", "EAL / English Teacher", "2024-02 - 2026-07"),
        ("GEDU Global Education", "Training and Quality Lead", "2022-09 - 2023-08"),
        ("WhiteHat Jr", "Assistant Manager — Teacher Quality & Development", "2020-08 - 2022-07"),
        ("Aoxin International School", "EAL / English Teacher", "2018-07 - 2020-08"),
        ("Eton House Kindergarten", "ESL Teacher and Teacher Trainer", "2017-08 - 2018-06"),
        ("Helen China TEFL Network", "ESL Teacher", "2016-11 - 2017-08"),
        ("Scholars Academy", "English, Science and Mathematics Teacher", "2014-01 - 2016-11")
    ]
    
    assert len(master['experience']) == 7
    assert len(portfolio['experience']) == 7
    
    for i, (expected_employer, expected_title, expected_dates) in enumerate(expected_employers):
        assert master['experience'][i]['company'] == expected_employer
        assert master['experience'][i]['role'] == expected_title
        assert master['experience'][i]['date'] == expected_dates
        
        assert portfolio['experience'][i]['company'] == expected_employer
        assert portfolio['experience'][i]['role'] == expected_title
        assert portfolio['experience'][i]['date'] == expected_dates

def test_negative_role_scrambling():
    roles_data = load_yaml(Path("career-data/facts/roles.yml"))
    emp_data = load_yaml(Path("career-data/facts/employment.yml"))
    
    valid_roles = {r['id']: r for r in roles_data['roles']}
    whitehat_emp = next((e for e in emp_data['employment_records'] if e['id'] == 'EMP-2004'), None)
    
    whitehat_emp['role_id'] = 'ROLE-8000' 
    
    with pytest.raises(AssertionError):
        assert valid_roles[whitehat_emp['role_id']]['title'] == 'Assistant Manager — Teacher Quality & Development'
