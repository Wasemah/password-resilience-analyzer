"""Tests for hash cracker"""

import unittest
from utils.cracker import HashCracker
from utils.hashing import hash_password

class TestHashCracker(unittest.TestCase):
    def setUp(self):
        self.cracker = HashCracker()
        self.test_password = "test123"
        self.test_hash_md5 = hash_password(self.test_password, 'md5')
    
    def test_hash_detection(self):
        self.assertEqual(self.cracker.detect_hash_type(self.test_hash_md5), 'md5')
    
    def test_hash_verification(self):
        self.assertTrue(self.cracker.verify_hash(self.test_password, self.test_hash_md5, 'md5'))
        self.assertFalse(self.cracker.verify_hash('wrong', self.test_hash_md5, 'md5'))
    
    def test_dictionary_attack(self):
        wordlist = {'test123', 'password', 'admin'}
        result = self.cracker.dictionary_attack(self.test_hash_md5, wordlist, 'md5')
        self.assertTrue(result['cracked'])
        self.assertEqual(result['password'], 'test123')

if __name__ == '__main__':
    unittest.main()
