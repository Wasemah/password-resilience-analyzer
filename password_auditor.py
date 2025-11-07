#!/usr/bin/env python3
"""
Password Security Auditor - Advanced Version
Comprehensive tool for password strength analysis and hash cracking
"""

import hashlib
import math
import string
import json
import time
from datetime import datetime
from colorama import Fore, Style, init
import argparse
import os
from tqdm import tqdm

from utils.hashing import compute_hashes, hash_password, hash_types
from utils.wordlists import load_wordlist, common_passwords, extended_common_passwords
from utils.cracker import HashCracker, CrackResults
from hash_cracker import benchmark_cracking_speed

# Initialize colorama for cross-platform colored output
init(autoreset=True)

PasswordAuditor = AdvancedPasswordAuditor

class AdvancedPasswordAuditor:
    def __init__(self):
        self.common_passwords = extended_common_passwords
        self.cracker = HashCracker()
        self.audit_history = []
    
    
    def calculate_entropy(self, password):
        """Calculate password entropy in bits with advanced analysis"""
        if not password:
            return 0, 0, 0
            
        # Advanced character pool analysis
        char_categories = {
            'lower': len([c for c in password if c in string.ascii_lowercase]),
            'upper': len([c for c in password if c in string.ascii_uppercase]),
            'digits': len([c for c in password if c in string.digits]),
            'special': len([c for c in password if c in string.punctuation]),
            'other': len([c for c in password if c not in string.printable])
        }
        
        # Determine character pool size
        pool_size = 0
        if char_categories['lower'] > 0: pool_size += 26
        if char_categories['upper'] > 0: pool_size += 26
        if char_categories['digits'] > 0: pool_size += 10
        if char_categories['special'] > 0: pool_size += 32
        if char_categories['other'] > 0: pool_size += 50  # Unicode/etc
        
        # Calculate entropy
        entropy = len(password) * math.log2(pool_size) if pool_size > 0 else 0
        
        # Pattern detection penalty
        pattern_penalty = self.detect_patterns(password)
        adjusted_entropy = max(0, entropy - pattern_penalty)
        
        return adjusted_entropy, entropy, char_categories
    
    def detect_patterns(self, password):
        """Detect common patterns and apply entropy penalty"""
        penalty = 0
        
        # Sequential characters
        sequences = ['123', 'abc', 'qwe', 'asd', 'zxc', '987', '321']
        for seq in sequences:
            if seq in password.lower():
                penalty += 10
                
        # Repeated characters
        for char in set(password):
            count = password.count(char)
            if count > len(password) * 0.5:  # More than 50% same char
                penalty += 15
                
        # Keyboard patterns
        keyboard_rows = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                if row[i:i+3] in password.lower():
                    penalty += 8
                    
        return penalty
    
    def strength_rating(self, entropy):
        """Convert entropy to strength rating with color coding"""
        if entropy < 28: return "Very Weak", Fore.RED
        elif entropy < 36: return "Weak", Fore.RED
        elif entropy < 60: return "Moderate", Fore.YELLOW
        elif entropy < 128: return "Strong", Fore.GREEN
        else: return "Very Strong", Fore.CYAN
    
    def check_common_password(self, password):
        """Check if password is in common password lists"""
        return password.lower() in self.common_passwords
    
    def time_to_crack_estimate(self, entropy):
        """Estimate time to crack based on entropy"""
        # Assuming 10^9 hashes/second (modern GPU)
        hashes_per_second = 10**9
        possible_combinations = 2 ** entropy
        
        seconds = possible_combinations / hashes_per_second
        
        if seconds < 60:
            return f"{seconds:.2f} seconds", Fore.GREEN
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes", Fore.YELLOW
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours", Fore.YELLOW
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days", Fore.RED
        else:
            return f"{seconds/31536000:.2f} years", Fore.RED
    
    def analyze_password(self, password):
        """Comprehensive password analysis with advanced metrics"""
        print(f"\n{Fore.CYAN}🔓 Advanced Password Analysis")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.WHITE}Password: {Fore.YELLOW}{'*' * len(password)} (length: {len(password)})")
        print(f"{Fore.CYAN}{'-'*60}")
        
        # Advanced analysis
        entropy, raw_entropy, char_categories = self.calculate_entropy(password)
        strength, strength_color = self.strength_rating(entropy)
        is_common = self.check_common_password(password)
        crack_time, crack_color = self.time_to_crack_estimate(entropy)
        
        # Display comprehensive results
        print(f"{Fore.WHITE}Strength Rating: {strength_color}{strength} {self.get_strength_icon(strength)}")
        print(f"{Fore.WHITE}Adjusted Entropy: {Fore.YELLOW}{entropy:.2f} bits")
        print(f"{Fore.WHITE}Raw Entropy: {Fore.YELLOW}{raw_entropy:.2f} bits")
        print(f"{Fore.WHITE}Time to Crack: {crack_color}{crack_time}")
        print(f"{Fore.WHITE}Common Password: {Fore.RED if is_common else Fore.GREEN}{is_common}")
        
        # Detailed character analysis
        print(f"\n{Fore.WHITE}Character Analysis:")
        total_chars = len(password)
        for category, count in char_categories.items():
            if count > 0:
                percentage = (count / total_chars) * 100
                color = Fore.GREEN if percentage > 10 else Fore.YELLOW
                print(f"  {category.title()}: {color}{count} ({percentage:.1f}%)")
        
        # Pattern detection
        patterns = self.detect_advanced_patterns(password)
        if patterns:
            print(f"\n{Fore.RED}⚠️  Detected Patterns:")
            for pattern in patterns:
                print(f"  {Fore.RED}❌ {pattern}")
        
        # Hash examples
        hashes = compute_hashes(password)
        print(f"\n{Fore.WHITE}Hash Examples:")
        for algo, hash_val in list(hashes.items())[:3]:  # Show first 3
            print(f"  {algo.upper()}: {Fore.CYAN}{hash_val[:16]}...")
        
        # Recommendations
        self.provide_advanced_recommendations(password, entropy, char_categories, is_common, patterns)
        
        # Save to audit history
        self.audit_history.append({
            'timestamp': datetime.now().isoformat(),
            'password_length': len(password),
            'entropy': entropy,
            'strength': strength,
            'analysis': {
                'char_categories': char_categories,
                'is_common': is_common,
                'patterns': patterns
            }
        })
    
    def detect_advanced_patterns(self, password):
        """Detect advanced password patterns"""
        patterns = []
        lower_pass = password.lower()
        
        # Common sequences
        sequences = [
            '123', '234', '345', '456', '567', '678', '789', '987', '876', '765',
            'abc', 'bcd', 'cde', 'def', 'efg', 'fgh', 'ghi', 'hij', 'ijk', 'jkl',
            'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop', 'asd', 'sdf',
            'dfg', 'fgh', 'ghj', 'hjk', 'jkl', 'zxc', 'xcv', 'cvb', 'vbn', 'bnm'
        ]
        
        for seq in sequences:
            if seq in lower_pass:
                patterns.append(f"Sequential pattern: '{seq}'")
                break
        
        # Repeated characters
        for char in set(password):
            if password.count(char) >= 3:
                patterns.append(f"Repeated character: '{char}' {password.count(char)} times")
                break
        
        # Date patterns (simple detection)
        if any(year in password for year in ['1980', '1990', '1991', '1992', '2000', '2001', '2020', '2021', '2022', '2023']):
            patterns.append("Contains common year")
            
        return patterns
    
    def get_strength_icon(self, strength):
        """Get icon for strength rating"""
        icons = {
            "Very Weak": "🔴",
            "Weak": "🟠", 
            "Moderate": "🟡",
            "Strong": "🟢",
            "Very Strong": "🔵"
        }
        return icons.get(strength, "⚪")
    
    def provide_advanced_recommendations(self, password, entropy, char_categories, is_common, patterns):
        """Provide advanced security recommendations"""
        print(f"\n{Fore.CYAN}💡 Security Recommendations:")
        
        recommendations = []
        
        # Length recommendations
        if len(password) < 12:
            recommendations.append(f"{Fore.RED}❌ Use at least 12 characters (current: {len(password)})")
        elif len(password) < 16:
            recommendations.append(f"{Fore.YELLOW}⚠️  Consider using 16+ characters for stronger security")
        else:
            recommendations.append(f"{Fore.GREEN}✅ Excellent password length")
        
        # Entropy recommendations
        if entropy < 60:
            recommendations.append(f"{Fore.RED}❌ Increase complexity with mixed character types")
        else:
            recommendations.append(f"{Fore.GREEN}✅ Good entropy level")
        
        # Common password check
        if is_common:
            recommendations.append(f"{Fore.RED}❌ This is a commonly used password - choose something unique")
        
        # Character diversity
        if char_categories['lower'] == 0:
            recommendations.append(f"{Fore.YELLOW}⚠️  Add lowercase letters")
        if char_categories['upper'] == 0:
            recommendations.append(f"{Fore.YELLOW}⚠️  Add uppercase letters") 
        if char_categories['digits'] == 0:
            recommendations.append(f"{Fore.YELLOW}⚠️  Add numbers")
        if char_categories['special'] == 0:
            recommendations.append(f"{Fore.YELLOW}⚠️  Add special characters")
        
        # Pattern recommendations
        if patterns:
            recommendations.append(f"{Fore.RED}❌ Avoid predictable patterns and sequences")
        
        # Display recommendations
        for rec in recommendations:
            print(f"  {rec}")
    
    def generate_report(self, filename=None):
        """Generate comprehensive audit report"""
        if not filename:
            filename = f"password_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_audits': len(self.audit_history),
                'tool_version': '2.0.0'
            },
            'audits': self.audit_history,
            'summary': {
                'average_entropy': sum(audit['entropy'] for audit in self.audit_history) / len(self.audit_history),
                'strong_passwords': sum(1 for audit in self.audit_history if audit['strength'] in ['Strong', 'Very Strong']),
                'weak_passwords': sum(1 for audit in self.audit_history if audit['strength'] in ['Very Weak', 'Weak'])
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{Fore.GREEN}✅ Audit report saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Advanced Password Security Auditor')
    parser.add_argument('password', nargs='?', help='Password to analyze')
    parser.add_argument('--hash', help='Hash to crack')
    parser.add_argument('--wordlist', help='Custom wordlist file')
    parser.add_argument('--benchmark', action='store_true', help='Run performance benchmarks')
    parser.add_argument('--report', help='Generate audit report file')
    
    args = parser.parse_args()
    
    auditor = AdvancedPasswordAuditor()
    
    if args.benchmark:
        benchmark_cracking_speed()
    elif args.hash:
        from hash_cracker import main as cracker_main
        cracker_main()
    elif args.password:
        auditor.analyze_password(args.password)
        if args.report:
            auditor.generate_report(args.report)
    else:
        # Interactive mode
        print(f"{Fore.CYAN}🔓 Advanced Password Security Auditor v2.0")
        print(f"{Fore.WHITE}Enter a password to analyze (or 'quit' to exit):")
        
        while True:
            try:
                password = input(f"\n{Fore.GREEN}Password: {Style.RESET_ALL}")
                if password.lower() in ['quit', 'exit', 'q']:
                    if input(f"\n{Fore.YELLOW}Generate audit report? (y/n): ").lower() == 'y':
                        auditor.generate_report()
                    break
                auditor.analyze_password(password)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Exiting...")
                break

if __name__ == "__main__":
    main()
