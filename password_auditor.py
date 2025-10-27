#!/usr/bin/env python3
"""
Password Security Auditor
A comprehensive tool for password strength analysis and hash cracking
"""

import hashlib
import math
import string
from passlib.hash import pbkdf2_sha256, bcrypt
from colorama import Fore, Style, init
import argparse
import time
from utils.hashing import compute_hashes, hash_types
from utils.wordlists import load_wordlist, common_passwords

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class PasswordAuditor:
    def __init__(self):
        self.common_passwords = common_passwords
        
    def calculate_entropy(self, password):
        """Calculate password entropy in bits"""
        if not password:
            return 0
            
        # Character pool analysis
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digits = any(c in string.digits for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        # Determine character pool size
        pool_size = 0
        if has_lower: pool_size += 26
        if has_upper: pool_size += 26
        if has_digits: pool_size += 10
        if has_special: pool_size += 32
        
        # Calculate entropy
        entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
        return entropy
    
    def strength_rating(self, entropy):
        """Convert entropy to strength rating"""
        if entropy < 28: return "Very Weak"
        elif entropy < 36: return "Weak"
        elif entropy < 60: return "Moderate"
        elif entropy < 128: return "Strong"
        else: return "Very Strong"
    
    def check_common_password(self, password):
        """Check if password is in common password list"""
        return password.lower() in self.common_passwords
    
    def analyze_password(self, password):
        """Comprehensive password analysis"""
        print(f"\n{Fore.CYAN}🔓 Analyzing Password: {password}")
        print("-" * 50)
        
        # Basic metrics
        length = len(password)
        entropy = self.calculate_entropy(password)
        strength = self.strength_rating(entropy)
        is_common = self.check_common_password(password)
        
        # Character composition
        has_lower = any(c in string.ascii_lowercase for c in password)
        has_upper = any(c in string.ascii_uppercase for c in password)
        has_digits = any(c in string.digits for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        # Display results
        print(f"{Fore.WHITE}Length: {Fore.YELLOW}{length} characters")
        print(f"{Fore.WHITE}Entropy: {Fore.YELLOW}{entropy:.2f} bits")
        print(f"{Fore.WHITE}Strength: {self.get_strength_color(strength)}{strength}")
        print(f"{Fore.WHITE}Common Password: {Fore.RED if is_common else Fore.GREEN}{is_common}")
        
        # Character composition
        print(f"\n{Fore.WHITE}Character Composition:")
        print(f"  Lowercase: {Fore.GREEN if has_lower else Fore.RED}{has_lower}")
        print(f"  Uppercase: {Fore.GREEN if has_upper else Fore.RED}{has_upper}")
        print(f"  Digits: {Fore.GREEN if has_digits else Fore.RED}{has_digits}")
        print(f"  Special: {Fore.GREEN if has_special else Fore.RED}{has_special}")
        
        # Recommendations
        self.provide_recommendations(length, entropy, has_lower, has_upper, has_digits, has_special, is_common)
    
    def get_strength_color(self, strength):
        """Return color based on strength rating"""
        colors = {
            "Very Weak": Fore.RED,
            "Weak": Fore.RED,
            "Moderate": Fore.YELLOW,
            "Strong": Fore.GREEN,
            "Very Strong": Fore.CYAN
        }
        return colors.get(strength, Fore.WHITE)
    
    def provide_recommendations(self, length, entropy, has_lower, has_upper, has_digits, has_special, is_common):
        """Provide security recommendations"""
        print(f"\n{Fore.CYAN}💡 Recommendations:")
        
        if length < 8:
            print(f"{Fore.RED}  ❌ Use at least 8 characters (current: {length})")
        else:
            print(f"{Fore.GREEN}  ✅ Good password length")
            
        if entropy < 36:
            print(f"{Fore.RED}  ❌ Increase complexity with mixed character types")
        else:
            print(f"{Fore.GREEN}  ✅ Good entropy level")
            
        if is_common:
            print(f"{Fore.RED}  ❌ Avoid common passwords - choose something unique")
            
        if not has_lower:
            print(f"{Fore.YELLOW}  ⚠️  Add lowercase letters")
        if not has_upper:
            print(f"{Fore.YELLOW}  ⚠️  Add uppercase letters")
        if not has_digits:
            print(f"{Fore.YELLOW}  ⚠️  Add numbers")
        if not has_special:
            print(f"{Fore.YELLOW}  ⚠️  Add special characters")

def main():
    parser = argparse.ArgumentParser(description='Password Security Auditor')
    parser.add_argument('password', nargs='?', help='Password to analyze')
    parser.add_argument('--hash', help='Hash to crack')
    parser.add_argument('--wordlist', help='Custom wordlist file')
    
    args = parser.parse_args()
    
    auditor = PasswordAuditor()
    
    if args.password:
        auditor.analyze_password(args.password)
    elif args.hash:
        print(f"{Fore.YELLOW}Hash cracking feature coming soon!")
    else:
        # Interactive mode
        print(f"{Fore.CYAN}🔓 Password Security Auditor")
        print(f"{Fore.WHITE}Enter a password to analyze (or 'quit' to exit):")
        
        while True:
            try:
                password = input(f"\n{Fore.GREEN}Password: {Style.RESET_ALL}")
                if password.lower() in ['quit', 'exit', 'q']:
                    break
                auditor.analyze_password(password)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting...")
                break

if __name__ == "__main__":
    main()
