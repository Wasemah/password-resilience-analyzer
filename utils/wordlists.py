"""Wordlist utilities for common passwords"""

import os

# Common passwords list (top 100 most common)
common_passwords = {
    '123456', 'password', '12345678', 'qwerty', '123456789',
    '12345', '1234', '111111', '1234567', 'dragon',
    '123123', 'baseball', 'abc123', 'football', 'monkey',
    'letmein', '696969', 'shadow', 'master', '666666',
    'qwertyuiop', '123321', 'mustang', '1234567890',
    'michael', '654321', 'superman', '1qaz2wsx', '7777777',
    'fuckyou', '121212', '000000', 'qazwsx', '123qwe',
    'killer', 'trustno1', 'jordan', 'jennifer', 'zxcvbnm',
    'asdfgh', 'hunter', 'buster', 'soccer', 'harley',
    'batman', 'andrew', 'tigger', 'sunshine', 'iloveyou',
    'fuckme', '2000', 'charlie', 'robert', 'thomas',
    'hockey', 'ranger', 'daniel', 'starwars', 'klaster',
    '112233', 'george', 'asshole', 'computer', 'michelle',
    'jessica', 'pepper', '1111', 'zxcvbn', '555555',
    '11111111', '131313', 'freedom', '777777', 'pass',
    'fuck', 'maggie', '159753', 'aaaaaa', 'ginger',
    'princess', 'joshua', 'cheese', 'amanda', 'summer',
    'love', 'ashley', '6969', 'nicole', 'chelsea',
    'biteme', 'matthew', 'access', 'yankees', '987654321',
    'dallas', 'austin', 'thunder', 'taylor', 'matrix'
}

def load_wordlist(filepath):
    """Load custom wordlist from file"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Wordlist file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return set(line.strip() for line in f if line.strip())
