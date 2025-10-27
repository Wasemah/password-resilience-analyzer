"""wordlist utilities"""

import os

# Extended common passwords (top 200+)
extended_common_passwords = {
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
    'dallas', 'austin', 'thunder', 'taylor', 'matrix',
    'william', 'corvette', 'hello', 'martin', 'heather',
    'secret', 'fucker', 'merlin', 'diamond', '1234qwer',
    'gfhjkm', 'computer', 'super', 'internet', 'apple',
    'passwort', 'orange', 'god', 'sexy', 'thx1138',
    'arsenal', 'iloveyou', 'a1b2c3', '123abc', 'windows',
    'money', 'password1', 'sample', 'hackme', 'admin123',
    'welcome', 'pussy', 'pass123', 'adminadmin', 'qwe123',
    'hello123', 'monkey123', 'password123', 'welcome123',
    'admin1', 'test123', '123456a', 'qweasd', 'baseball123'
}

# Common passwords list (alias for compatibility)
common_passwords = extended_common_passwords

def load_wordlist(filepath):
    """Load custom wordlist from file with error handling"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Wordlist file not found: {filepath}")
    
    wordlist = set()
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip comments
                    wordlist.add(line)
    except Exception as e:
        raise IOError(f"Error reading wordlist: {e}")
    
    return wordlist

def generate_rockyou_sample():
    """Generate a sample rockyou wordlist for testing"""
    sample_passwords = list(extended_common_passwords)[:50]  # Top 50 common
    return set(sample_passwords)
