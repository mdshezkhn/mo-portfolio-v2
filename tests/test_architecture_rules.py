import os
import ast
import pytest
from pathlib import Path

# The resolver and other upstream scripts that process YAML
ALLOWED_YAML_READERS = {
    'resolve_graph.py',
    'validate_yaml.py',
    'validate_ids.py',
    'allocate_ids.py',
    'migrate_initial_ids.py',
    'migrate_employment.py',
    'migrate_education.py',
    'create_minimal_fixture.py',
    
    # Legacy / Utility / Audit Scripts
    'validate_evidence.py',
    'generate_canonical_profile.py',
    'verify_canonical_profile.py',
    'verify_claims.py',
    'verify_title_fields.py',
    'career_analytics.py',
    'generate_schemas.py',
    'generate_contracts.py',
    'ci_pipeline.py',
    'audit_claims.py',
    'audit_credentials.py',
    'audit_evidence.py',
    'audit_live_site.py',
    'audit_numeric_literals.py',
    'compile_claim_register.py',
    'cross_match_facts.py',
    'detect_legacy_content.py',
    'discover_assets.py',
    'extract_canonical_facts.py',
    'impact_analysis.py',
    'migrate_claim_register.py',
    'validate_schemas.py',
    'verify_all_dependencies.py',
    'verify_public_scope.py'
}

def test_id_governance_in_ci():
    """Ensure that validate_ids.py is executed in the CI pipeline."""
    ci_file = Path('scripts/ci_pipeline.py')
    with open(ci_file, 'r', encoding='utf-8') as f:
        content = f.read()
        assert 'validate_ids.py' in content, "Architectural violation: validate_ids.py must run in CI"
        assert 'build_id_registry.py' not in content, "Architectural violation: build_id_registry is deprecated"

def test_pipeline_stages_in_ci():
    """Ensure that the pipeline architecture stages are executed in the correct order."""
    ci_file = Path('scripts/ci_pipeline.py')
    with open(ci_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    stages = [
        'resolve_graph.py',
        'metrics_engine.py',
        'content_quality_engine.py',
        'selection_engine.py',
        'policy_engine.py'
    ]
    
    last_pos = -1
    for stage in stages:
        pos = content.find(stage)
        assert pos != -1, f"Architectural violation: {stage} missing from CI pipeline"
        assert pos > last_pos, f"Architectural violation: {stage} runs out of order"
        last_pos = pos

def test_no_yaml_imports_downstream():
    """Ensure that no scripts downstream of the resolver import the yaml module."""
    scripts_dir = Path('scripts')
    violators = []
    for py_file in scripts_dir.glob('*.py'):
        if py_file.name in ALLOWED_YAML_READERS:
            continue
        with open(py_file, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=py_file.name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'yaml': violators.append(py_file.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'yaml': violators.append(py_file.name)
    assert not violators, f"Architectural violation: The following downstream scripts import yaml: {violators}"

def test_no_facts_reading_downstream():
    """Ensure that no downstream scripts attempt to read from career-data/facts."""
    scripts_dir = Path('scripts')
    violators = []
    for py_file in scripts_dir.glob('*.py'):
        if py_file.name in ALLOWED_YAML_READERS:
            continue
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'career-data/facts' in content or 'career-data\\facts' in content:
                violators.append(py_file.name)
    assert not violators, f"Architectural violation: Downstream scripts reading raw facts directory: {violators}"

def test_policy_no_pathlib():
    """Ensure Policy Engine does not perform file I/O operations (no pathlib)."""
    policy_file = Path('scripts/policy_engine.py')
    if not policy_file.exists():
        return
    with open(policy_file, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=policy_file.name)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name != 'pathlib', "Policy engine must be pure and cannot import pathlib"
        elif isinstance(node, ast.ImportFrom):
            assert node.module != 'pathlib', "Policy engine must be pure and cannot import pathlib"

def test_generator_dependencies():
    """Ensure Generators do not read Intermediate representation directly."""
    scripts_dir = Path('scripts')
    generators = [f for f in scripts_dir.glob('*.py') if f.name.startswith('generate_') and f.name not in ('generate_schemas.py', 'generate_contracts.py')]
    violators = []
    for gen_file in generators:
        with open(gen_file, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=gen_file.name)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'compile_intermediate' in alias.name: violators.append(gen_file.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and 'compile_intermediate' in node.module: violators.append(gen_file.name)
    assert not violators, f"Architectural violation: Generators cannot import compile_intermediate: {violators}"

def test_view_models_contain_no_functions():
    """Ensure View Models contain only presentation data, no logic/functions."""
    view_model_file = Path('scripts/build_view_models.py')
    if not view_model_file.exists():
        return
    with open(view_model_file, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=view_model_file.name)
    violators = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for body_item in node.body:
                if isinstance(body_item, ast.FunctionDef) and body_item.name != '__init__':
                    violators.append(f"{node.name}.{body_item.name}")
    assert not violators, f"Architectural violation: View Models cannot contain logic methods: {violators}"
