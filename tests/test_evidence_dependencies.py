import unittest
import yaml
from pathlib import Path

class TestEvidenceDependencies(unittest.TestCase):
    def test_no_missing_evidence_dependencies(self):
        root = Path(__file__).resolve().parent.parent
        manifest_file = root / "evidence" / "manifest.yml"
        claims_dir = root / "career-data" / "facts" / "claims"
        emp_file = root / "career-data" / "facts" / "employment.yml"
        edu_file = root / "career-data" / "facts" / "education.yml"
        
        self.assertTrue(manifest_file.exists(), "manifest.yml missing")
        manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8")).get("entries", {})
        manifest_ev_ids = set(manifest.keys())
        
        referenced_ev_ids = set()
        if claims_dir.exists():
            for cfile in claims_dir.glob("*.yml"):
                cdata = yaml.safe_load(cfile.read_text(encoding="utf-8"))
                for c in cdata.get("claims", []):
                    for ev in c.get("evidence", []):
                        referenced_ev_ids.add(ev)
                        
        emp_data = yaml.safe_load(emp_file.read_text(encoding="utf-8")).get("employment_records", [])
        for e in emp_data:
            for ev in e.get("evidence", []):
                referenced_ev_ids.add(ev)
                
        edu_data = yaml.safe_load(edu_file.read_text(encoding="utf-8")).get("education_records", [])
        for q in edu_data:
            for ev in q.get("evidence", []):
                referenced_ev_ids.add(ev)
                
        missing_ids = referenced_ev_ids - manifest_ev_ids
        self.assertEqual(len(missing_ids), 0, f"Missing evidence IDs in manifest: {missing_ids}")

if __name__ == "__main__":
    unittest.main()
