"""Hashing utilities for password auditor"""

import hashlib
import binascii

def compute_hashes(password):
    """Compute multiple hash types for a password"""
    hashes = {}
    
    # MD5
    hashes['md5'] = hashlib.md5(password.encode()).hexdigest()
    
    # SHA1
    hashes['sha1'] = hashlib.sha1(password.encode()).hexdigest()
    
    # SHA256
    hashes['sha256'] = hashlib.sha256(password.encode()).hexdigest()
    
    # SHA512
    hashes['sha512'] = hashlib.sha512(password.encode()).hexdigest()
    
    return hashes

def hash_password(password, algorithm='sha256'):
    """Hash password with specified algorithm"""
    if algorithm == 'md5':
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(password.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(password.encode()).hexdigest()
    elif algorithm == 'sha512':
        return hashlib.sha512(password.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

# Supported hash types
hash_types = ['md5', 'sha1', 'sha256', 'sha512']
