import os
import json
import pytest
import subprocess
import hashlib
from pathlib import Path

FIXTURE_ROOT = Path(os.path.abspath("tests/fixtures/v1"))
PROJECT_ROOT = Path(os.path.abspath("."))

def normalize_json(data):
    """Recursively remove dynamic metadata like build_id, generated_at, source_commit and normalize path separators to allow deterministic comparison."""
    if isinstance(data, dict):
        normalized = {}
        for k, v in data.items():
            if k in {'build_id', 'generated_at', 'source_commit', 'input_hash', '_metadata'}:
                pass
            elif k == 'metadata' and isinstance(v, dict):
                normalized[k] = normalize_json(v)
            else:
                normalized[k] = normalize_json(v)
        return normalized
    elif isinstance(data, list):
        return [normalize_json(i) for i in data]
    elif isinstance(data, str):
        return data.replace('\\', '/')
    return data

def run_pipeline(fixture_name, output_dir):
    base_dir = FIXTURE_ROOT / fixture_name
    intermediate_dir = output_dir / "intermediate"
    view_models_dir = output_dir / "view_models"
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    view_models_dir.mkdir(parents=True, exist_ok=True)
    
    env = os.environ.copy()
    
    # 1. Resolve Graph
    subprocess.run(["python", "scripts/resolve_graph.py", "--data-dir", str(base_dir), "--output-dir", str(intermediate_dir)], check=True, cwd=PROJECT_ROOT, env=env)
    
    # 2. Metrics Engine
    subprocess.run(["python", "scripts/metrics_engine.py", "--intermediate-dir", str(intermediate_dir)], check=True, cwd=PROJECT_ROOT, env=env)
    
    # 3. Compile Intermediate
    subprocess.run(["python", "scripts/compile_intermediate.py", "--intermediate-dir", str(intermediate_dir)], check=True, cwd=PROJECT_ROOT, env=env)
    
    # 4. Policy Engine
    subprocess.run(["python", "scripts/policy_engine.py", 
                    "--intermediate-file", str(intermediate_dir / "facts.json"), 
                    "--config-file", "career-data/policy/market_rules.json", 
                    "--output-file", str(intermediate_dir / "filtered_facts.json")], check=True, cwd=PROJECT_ROOT, env=env)
                    
    # 5. Build View Models
    # subprocess.run(["python", "scripts/build_view_models.py", 
    #                 "--intermediate-file", str(intermediate_dir / "filtered_facts.json"),
    #                 "--output-dir", str(view_models_dir)], check=True, cwd=PROJECT_ROOT, env=env)

def assert_snapshot_match(request, artifact_path, snapshot_filename, fixture_name="minimal"):
    if not artifact_path.exists():
        pytest.skip(f"{artifact_path} does not exist yet.")
        
    with open(artifact_path, 'r', encoding='utf-8') as f:
        current_data = json.load(f)
        
    normalized_current = normalize_json(current_data)
    
    snapshot_path = FIXTURE_ROOT / fixture_name / "expected" / snapshot_filename
    
    update_snapshots = request.config.getoption("--snapshot-update")
    
    if update_snapshots or not snapshot_path.exists():
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(normalized_current, f, indent=2)
        print(f"Updated snapshot for {snapshot_filename}")
        return
        
    with open(snapshot_path, 'r', encoding='utf-8') as f:
        snapshot_data = normalize_json(json.load(f))
        
    assert normalized_current == snapshot_data, f"Snapshot mismatch for {snapshot_filename}. Run with --snapshot-update to overwrite."

def test_reproducibility(tmp_path):
    """build() -> hash() -> build() -> hash() -> assert identical"""
    out1 = tmp_path / "build1"
    out2 = tmp_path / "build2"
    
    run_pipeline("minimal", out1)
    run_pipeline("minimal", out2)
    
    artifacts1 = sorted(out1.rglob("*.json"))
    artifacts2 = sorted(out2.rglob("*.json"))
    
    assert len(artifacts1) == len(artifacts2), "Different number of artifacts generated"
    assert len(artifacts1) > 0, "No artifacts generated"
    
    for a1, a2 in zip(artifacts1, artifacts2):
        assert a1.name == a2.name
        
        with open(a1, 'r', encoding='utf-8') as f: d1 = normalize_json(json.load(f))
        with open(a2, 'r', encoding='utf-8') as f: d2 = normalize_json(json.load(f))
        
        s1 = json.dumps(d1, sort_keys=True)
        s2 = json.dumps(d2, sort_keys=True)
        
        h1 = hashlib.sha256(s1.encode()).hexdigest()
        h2 = hashlib.sha256(s2.encode()).hexdigest()
        
        assert h1 == h2, f"{a1.name} is not reproducible between builds"

@pytest.fixture(scope="module")
def built_minimal_fixture(tmp_path_factory):
    out_dir = tmp_path_factory.mktemp("minimal_build")
    run_pipeline("minimal", out_dir)
    return out_dir

def test_minimal_snapshot_resolved_graph(request, built_minimal_fixture):
    assert_snapshot_match(request, built_minimal_fixture / "intermediate" / "resolved_graph.json", "resolved_graph.snapshot.json")

def test_minimal_snapshot_metrics(request, built_minimal_fixture):
    assert_snapshot_match(request, built_minimal_fixture / "intermediate" / "metrics.json", "metrics.snapshot.json")

def test_minimal_snapshot_intermediate(request, built_minimal_fixture):
    assert_snapshot_match(request, built_minimal_fixture / "intermediate" / "facts.json", "facts.snapshot.json")
    
def test_minimal_snapshot_policy_output(request, built_minimal_fixture):
    assert_snapshot_match(request, built_minimal_fixture / "intermediate" / "filtered_facts.json", "filtered_facts.snapshot.json")

def test_minimal_semantic_assertions(built_minimal_fixture):
    with open(built_minimal_fixture / "intermediate" / "resolved_graph.json", 'r') as f:
        graph = json.load(f)
        
    entities_dict = graph.get("entities", {})
    entities = list(entities_dict.values())
    
    employments = [e for e in entities if e.get("entity_type") == "Employment"]
    assert len(employments) == 1, f"Expected 1 Employment, got {len(employments)}"
    
    evidences = [e for e in entities if e.get("entity_type") == "Evidence"]
    assert len(evidences) == 1, f"Expected 1 Evidence, got {len(evidences)}"
    
    orphan_nodes = graph.get("orphan_nodes", [])
    assert len(orphan_nodes) == 0, f"Found orphan nodes: {orphan_nodes}"
    
    ids = [e["id"] for e in entities]
    assert len(ids) == len(set(ids)), "Duplicate IDs found in resolved graph"
    
def test_provenance_regression(built_minimal_fixture):
    facts_path = built_minimal_fixture / "intermediate" / "facts.json"
    if facts_path.exists():
        with open(facts_path, 'r') as f:
            data = json.load(f)
            provenance = data.get("provenance", [])
            for p in provenance:
                assert "statement_id" in p
                assert "source_ids" in p
