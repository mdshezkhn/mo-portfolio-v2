import os
import json
import unittest
from bs4 import BeautifulSoup
from pathlib import Path

class TestJourneyCardsDOM(unittest.TestCase):
    def setUp(self):
        # Paths
        self.workspace_root = Path(__file__).parent.parent.parent
        self.html_path = self.workspace_root / "mo-portfolio-v2" / "index.html"
        self.view_model_path = self.workspace_root / "artifacts" / "cv_view_models" / "portfolio.json"

        # Load canonical view model
        with open(self.view_model_path, 'r', encoding='utf-8') as f:
            self.view_model = json.load(f)
            
        # Build lookup by canonical ID
        self.expected_by_id = {exp['id']: exp for exp in self.view_model.get('experience', [])}
        
        # Parse HTML
        with open(self.html_path, 'r', encoding='utf-8') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')
            
    def test_journey_cards_match_canonical_state(self):
        """
        Verifies that the rendered Journey cards in index.html exactly match
        the canonical expectations established in the portfolio.json view model.
        """
        # Find the timeline section
        timeline_section = self.soup.find(id="journey")
        self.assertIsNotNone(timeline_section, "Journey section not found in DOM")
        
        # Find all cards
        cards = timeline_section.find_all(class_="tl-item")
        
        # Expect exactly the number of employments as the view model
        expected_experiences = self.view_model.get('experience', [])
        self.assertEqual(len(cards), len(expected_experiences), 
                         f"Expected {len(expected_experiences)} journey cards, found {len(cards)}")
        
        # Sort expected experiences by start date descending (newest first)
        expected_ids = sorted(
            self.expected_by_id.keys(),
            key=lambda emp_id: self.expected_by_id[emp_id].get("date", "").split(" - ")[0],
            reverse=True
        )
        
        for emp_id in expected_ids:
            exp = self.expected_by_id[emp_id]
            
            # Find card by canonical ID
            card = timeline_section.find("div", class_="tl-item", attrs={"data-id": emp_id})
            self.assertIsNotNone(card, f"Missing card for canonical ID {emp_id}")
            
            # The h3 contains the role (e.g., "EAL / English Teacher")
            role_el = card.find("h3", class_="tl-title")
            self.assertIsNotNone(role_el, f"Missing h3 (role) in card {emp_id}")
            self.assertEqual(role_el.text.strip(), exp["role"], f"Role mismatch in card {emp_id}")
            
            # The p class="tl-org" contains the company
            company_el = card.find("p", class_="tl-org")
            self.assertIsNotNone(company_el, f"Missing p.tl-org (company) in card {emp_id}")
            self.assertEqual(company_el.text.strip(), exp["company"], f"Company mismatch in card {emp_id}")
            
            # Check responsibilities (role scope) - should always be present with >= 3 items
            resp_items = card.find_all("li", class_="tl-responsibility")
            expected_responsibilities = exp.get("responsibilities", [])
            self.assertGreaterEqual(len(resp_items), 3, 
                f"Expected at least 3 responsibilities for {emp_id} ({exp['company']}), found {len(resp_items)}")
            
            # Verify responsibility text matches canonical
            for j, expected_resp in enumerate(expected_responsibilities):
                self.assertEqual(resp_items[j].text.strip(), expected_resp, 
                    f"Responsibility text mismatch in {emp_id} responsibility {j}")
            
            # Check verified achievements (evidence-backed claims) - only when present
            achievement_items = card.find_all("li", class_="tl-achievement")
            expected_achievements = exp.get("bullets", [])
            self.assertEqual(len(achievement_items), len(expected_achievements),
                f"Expected {len(expected_achievements)} achievements for {emp_id}, found {len(achievement_items)}")
            
            for j, expected_ach in enumerate(expected_achievements):
                self.assertEqual(achievement_items[j].text.strip(), expected_ach,
                    f"Achievement text mismatch in {emp_id} achievement {j}")

    def test_canonical_order_is_reverse_chronological(self):
        """Verify cards render in reverse chronological order by start date."""
        timeline_section = self.soup.find(id="journey")
        self.assertIsNotNone(timeline_section)
        
        cards = timeline_section.find_all(class_="tl-item")
        self.assertEqual(len(cards), 7)
        
        # Extract start dates from data-id order
        rendered_ids = [card.get("data-id") for card in cards]
        self.assertEqual(rendered_ids, [
            "EMP-2006", "EMP-2005", "EMP-2004", "EMP-2003", 
            "EMP-2002", "EMP-2001", "EMP-2000"
        ])

if __name__ == '__main__':
    unittest.main()
