import unittest
import yaml
from pathlib import Path

class TestHarrisGate(unittest.TestCase):
    def test_harris_gate_enforced(self):
        root = Path(__file__).resolve().parent.parent
        edu_file = root / "career-data" / "facts" / "education.yml"
        self.assertTrue(edu_file.exists(), "education.yml missing")
        
        edu_data = yaml.safe_load(edu_file.read_text(encoding="utf-8")).get("education_records", [])
        
        harris_record = None
        for q in edu_data:
            if q["id"] == "QUAL-3001":
                harris_record = q
                break
                
        self.assertIsNotNone(harris_record, "QUAL-3001 (Harris M.A.) record missing")
        self.assertEqual(harris_record["confidence"], "V1", "Harris record confidence must be V1")
        self.assertFalse(harris_record["publication"]["premium_schools"], "Harris record must be excluded from premium_schools")
        self.assertTrue(harris_record["publication"]["verified_only_gate"], "Harris record must have verified_only_gate enabled")

if __name__ == "__main__":
    unittest.main()
