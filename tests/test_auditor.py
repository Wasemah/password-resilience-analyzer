"""Tests for password auditor"""

import unittest
from password_auditor import PasswordAuditor

class TestPasswordAuditor(unittest.TestCase):
    def setUp(self):
        self.auditor = PasswordAuditor()
    
    def test_entropy_calculation(self):
        self.assertGreater(self.auditor.calculate_entropy("StrongPass123!"), 50)
        self.assertLess(self.auditor.calculate_entropy("123"), 10)
    
    def test_common_password(self):
        self.assertTrue(self.auditor.check_common_password("password"))
        self.assertFalse(self.auditor.check_common_password("MyUniquePass123!"))
    
    def test_strength_rating(self):
        self.assertEqual(self.auditor.strength_rating(20), "Very Weak")
        self.assertEqual(self.auditor.strength_rating(70), "Strong")

if __name__ == '__main__':
    unittest.main()
