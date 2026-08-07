import unittest
import yaml
from pathlib import Path

class TestRestrictedClaims(unittest.TestCase):
    def test_restricted_claims_isolated(self):
        root = Path(__file__).resolve().parent.parent
        restricted_file = root / "career-data" / "facts" / "claims" / "restricted.yml"
        self.assertTrue(restricted_file.exists(), "claims/restricted.yml missing")
        
        cdata = yaml.safe_load(restricted_file.read_text(encoding="utf-8")).get("claims", [])
        
        for c in cdata:
            self.assertEqual(c.get("status"), "restricted", f"Claim {c['id']} must have status 'restricted'")
            self.assertEqual(len(c.get("presentation_assets", [])), 0, f"Restricted claim {c['id']} cannot be in presentation assets")

if __name__ == "__main__":
    unittest.main()
