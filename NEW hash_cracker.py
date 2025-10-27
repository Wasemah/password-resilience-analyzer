#!/usr/bin/env python3
"""
Advanced Hash Cracking Module
"""

import hashlib
import time
import argparse
from colorama import Fore, Style, init
from tqdm import tqdm
import multiprocessing as mp
from utils.cracker import HashCracker, CrackResults
from utils.wordlists import load_wordlist, extended_common_passwords

init(autoreset=True)

class AdvancedHashCracker:
    def __init__(self):
        self.cracker = HashCracker()
        self.results = CrackResults()
    
    def crack_hash(self, target_hash, hash_type='auto', wordlist=None, max_workers=4):
        """Advanced hash cracking with multiple strategies"""
        print(f"\n{Fore.CYAN}🔓 Starting Advanced Hash Cracking")
        print(f"{Fore.WHITE}Target Hash: {Fore.YELLOW}{target_hash}")
        print(f"{Fore.WHITE}Hash Type: {Fore.YELLOW}{hash_type}")
        print(f"{Fore.CYAN}{'='*50}")
        
        start_time = time.time()
        
        # Strategy 1: Common passwords first
        print(f"\n{Fore.GREEN}[1/3] Trying common passwords...")
        common_result = self.cracker.dictionary_attack(
            target_hash, extended_common_passwords, hash_type
        )
        
        if common_result['cracked']:
            self.display_result(common_result, time.time() - start_time)
            return common_result
        
        # Strategy 2: Wordlist attack
        if wordlist:
            print(f"\n{Fore.GREEN}[2/3] Trying wordlist attack...")
            wordlist_data = load_wordlist(wordlist)
            wordlist_result = self.cracker.dictionary_attack(
                target_hash, wordlist_data, hash_type, desc="Wordlist"
            )
            
            if wordlist_result['cracked']:
                self.display_result(wordlist_result, time.time() - start_time)
                return wordlist_result
        
        # Strategy 3: Advanced rules
        print(f"\n{Fore.GREEN}[3/3] Trying rule-based attacks...")
        rule_result = self.cracker.rule_based_attack(target_hash, hash_type)
        
        elapsed_time = time.time() - start_time
        self.display_result(rule_result, elapsed_time)
        
        if not rule_result['cracked']:
            print(f"\n{Fore.RED}❌ Hash could not be cracked with available methods")
            print(f"{Fore.YELLOW}💡 Try with a larger wordlist or different attack type")
        
        return rule_result
    
    def display_result(self, result, elapsed_time):
        """Display cracking results"""
        if result['cracked']:
            print(f"\n{Fore.GREEN}🎉 SUCCESS! Hash cracked!")
            print(f"{Fore.WHITE}Password: {Fore.GREEN}{result['password']}")
            print(f"{Fore.WHITE}Time: {Fore.YELLOW}{elapsed_time:.2f} seconds")
            print(f"{Fore.WHITE}Attempts: {Fore.CYAN}{result['attempts']}")
            print(f"{Fore.WHITE}Method: {Fore.CYAN}{result['method']}")
        else:
            print(f"\n{Fore.RED}❌ Failed to crack hash")
            print(f"{Fore.WHITE}Time: {Fore.YELLOW}{elapsed_time:.2f} seconds")
            print(f"{Fore.WHITE}Attempts: {Fore.CYAN}{result['attempts']}")

def benchmark_cracking_speed():
    """Benchmark hash cracking performance"""
    print(f"\n{Fore.CYAN}🧪 Performance Benchmark")
    print(f"{Fore.CYAN}{'='*40}")
    
    test_passwords = ['password123', 'SecurePass!2024', 'test']
    hash_types = ['md5', 'sha1', 'sha256']
    
    cracker = HashCracker()
    
    for hash_type in hash_types:
        print(f"\n{Fore.WHITE}Benchmarking {hash_type.upper()}...")
        
        for password in test_passwords:
            hash_val = cracker.hash_password(password, hash_type)
            
            start_time = time.time()
            attempts = 0
            max_attempts = 10000
            
            # Benchmark speed
            for test_pass in ['password', '123456', 'test', 'admin']:
                attempts += 1
                if cracker.verify_hash(test_pass, hash_val, hash_type):
                    break
                if attempts >= max_attempts:
                    break
            
            end_time = time.time()
            hashes_per_second = attempts / (end_time - start_time) if attempts > 0 else 0
            
            print(f"  {password}: {Fore.YELLOW}{hashes_per_second:,.0f} hashes/second")

def main():
    parser = argparse.ArgumentParser(description='Advanced Hash Cracker')
    parser.add_argument('hash', help='Hash to crack')
    parser.add_argument('--type', default='auto', help='Hash type (md5, sha1, sha256, auto)')
    parser.add_argument('--wordlist', help='Wordlist file path')
    parser.add_argument('--benchmark', action='store_true', help='Run benchmarks')
    
    args = parser.parse_args()
    
    if args.benchmark:
        benchmark_cracking_speed()
    else:
        cracker = AdvancedHashCracker()
        cracker.crack_hash(args.hash, args.type, args.wordlist)

if __name__ == "__main__":
    main()
