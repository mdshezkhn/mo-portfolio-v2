import unittest
import yaml
from pathlib import Path

class TestMetricDrift(unittest.TestCase):
    def test_metric_computation_integrity(self):
        root = Path(__file__).resolve().parent.parent
        emp_file = root / "career-data" / "facts" / "employment.yml"
        self.assertTrue(emp_file.exists())
        
        emp_data = yaml.safe_load(emp_file.read_text(encoding="utf-8")).get("employment_records", [])
        
        physical_countries = set()
        employers = set()
        for e in emp_data:
            employers.add(e["employer_id"])
            if e.get("physical_country"):
                physical_countries.add(e["physical_country"])
                
        self.assertEqual(len(employers), 6, f"Expected 6 unique employer IDs, found {len(employers)}")
        self.assertTrue("India" in physical_countries and "China" in physical_countries, "Physical countries must include India and China")
        self.assertEqual(len(physical_countries), 3, f"Expected physical countries [India, China, UK], found {physical_countries}")

if __name__ == "__main__":
    unittest.main()
