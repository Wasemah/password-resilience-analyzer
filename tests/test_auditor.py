"""Tests for password auditor"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import the auditor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from password_auditor import PasswordAuditor

class TestPasswordAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = PasswordAuditor()
    
    def test_entropy_calculation(self):
        # calculate_entropy now returns (adjusted_entropy, raw_entropy, char_categories)
        adjusted_entropy, raw_entropy, char_categories = self.auditor.calculate_entropy("StrongPass123!")
        self.assertGreater(adjusted_entropy, 50)
        
        # Test weak password
        adjusted_entropy_weak, raw_entropy_weak, char_categories_weak = self.auditor.calculate_entropy("123")
        self.assertLess(adjusted_entropy_weak, 10)
    
    def test_common_password(self):
        self.assertTrue(self.auditor.check_common_password("password"))
        self.assertFalse(self.auditor.check_common_password("MyUniquePass123!"))
    
    def test_strength_rating(self):
        # strength_rating now returns (rating, color_code)
        rating, color = self.auditor.strength_rating(20)
        self.assertEqual(rating, "Very Weak")
        
        rating, color = self.auditor.strength_rating(70)
        self.assertEqual(rating, "Strong")

if __name__ == '__main__':
    unittest.main()
