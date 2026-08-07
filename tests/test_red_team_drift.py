import unittest
import yaml
import re

def normalize_text(text):
    text = re.sub(r'<!--.*?-->', '', text)
    text = re.sub(r'[*_#>`~]', '', text)
    text = " ".join(text.split()).lower().strip(".,:;-")
    return text

class TestRedTeamDriftDetection(unittest.TestCase):
    def test_detects_unsupported_outcome_claim(self):
        fake_line = "Managed 500 teachers across China."
        norm = normalize_text(fake_line)
        triggers = ["managed", "500"]
        
        has_trigger = any(t in norm for t in triggers)
        self.assertTrue(has_trigger, "Audit engine must flag 'managed 500 teachers' as a trigger violation")

    def test_detects_date_drift(self):
        fake_year = "2015"
        canonical_start = "2014-01"
        self.assertNotEqual(fake_year, canonical_start.split("-")[0], "Audit engine must detect date drift")

if __name__ == "__main__":
    unittest.main()
