"""Advanced hash cracking utilities"""

import hashlib
import itertools
import string
from tqdm import tqdm
import time

class HashCracker:
    def __init__(self):
        self.common_leet_map = {
            'a': ['a', 'A', '4', '@'],
            'b': ['b', 'B', '8'],
            'e': ['e', 'E', '3'],
            'g': ['g', 'G', '9'],
            'i': ['i', 'I', '1', '!'],
            'l': ['l', 'L', '1', '|'],
            'o': ['o', 'O', '0'],
            's': ['s', 'S', '5', '$'],
            't': ['t', 'T', '7'],
            'z': ['z', 'Z', '2']
        }
    
    def hash_password(self, password, algorithm):
        """Hash password with specified algorithm"""
        password = password.encode('utf-8')
        
        if algorithm == 'md5':
            return hashlib.md5(password).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(password).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(password).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(password).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    def verify_hash(self, password, target_hash, algorithm):
        """Verify if password matches target hash"""
        return self.hash_password(password, algorithm) == target_hash
    
    def detect_hash_type(self, hash_string):
        """Auto-detect hash type based on length"""
        length = len(hash_string)
        
        if length == 32: return 'md5'
        elif length == 40: return 'sha1'
        elif length == 64: return 'sha256'
        elif length == 128: return 'sha512'
        else: return 'unknown'
    
    def dictionary_attack(self, target_hash, wordlist, hash_type='auto', desc="Cracking"):
        """Perform dictionary attack with progress bar"""
        if hash_type == 'auto':
            hash_type = self.detect_hash_type(target_hash)
        
        attempts = 0
        start_time = time.time()
        
        with tqdm(total=len(wordlist), desc=desc, unit="word") as pbar:
            for password in wordlist:
                attempts += 1
                if self.verify_hash(password, target_hash, hash_type):
                    return {
                        'cracked': True,
                        'password': password,
                        'attempts': attempts,
                        'time': time.time() - start_time,
                        'method': 'dictionary'
                    }
                pbar.update(1)
        
        return {
            'cracked': False,
            'password': None,
            'attempts': attempts,
            'time': time.time() - start_time,
            'method': 'dictionary'
        }
    
    def rule_based_attack(self, target_hash, hash_type='auto', max_length=6):
        """Rule-based attack with common password patterns"""
        if hash_type == 'auto':
            hash_type = self.detect_hash_type(target_hash)
        
        attempts = 0
        start_time = time.time()
        
        # Common base words
        base_words = ['password', 'admin', 'test', 'guest', '123', 'qwerty']
        
        # Common suffixes and prefixes
        suffixes = ['', '1', '12', '123', '!', '!!', '2024', '2023']
        prefixes = ['', '1', '12', '!']
        
        total_combinations = len(base_words) * len(suffixes) * len(prefixes)
        
        with tqdm(total=total_combinations, desc="Rule-based", unit="combo") as pbar:
            for base in base_words:
                for prefix in prefixes:
                    for suffix in suffixes:
                        attempts += 1
                        
                        # Try different combinations
                        candidates = [
                            prefix + base + suffix,
                            base.capitalize() + suffix,
                            base.upper() + suffix,
                        ]
                        
                        for candidate in candidates:
                            if self.verify_hash(candidate, target_hash, hash_type):
                                return {
                                    'cracked': True,
                                    'password': candidate,
                                    'attempts': attempts,
                                    'time': time.time() - start_time,
                                    'method': 'rule-based'
                                }
                        
                        pbar.update(1)
        
        return {
            'cracked': False,
            'password': None,
            'attempts': attempts,
            'time': time.time() - start_time,
            'method': 'rule-based'
        }

class CrackResults:
    """Store and manage cracking results"""
    def __init__(self):
        self.results = []
        self.successful_cracks = 0
        self.total_attempts = 0
    
    def add_result(self, result):
        self.results.append(result)
        self.total_attempts += result['attempts']
        if result['cracked']:
            self.successful_cracks += 1
    
    def get_success_rate(self):
        return (self.successful_cracks / len(self.results)) * 100 if self.results else 0
