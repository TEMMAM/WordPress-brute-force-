Advanced WordPress login testing tool with WAF (Web Application Firewall) evasion capabilities.

## ⚠️ Legal Disclaimer
**This tool is for authorized security testing and educational purposes only.**  
Unauthorized use against systems you don't own or have explicit permission to test is illegal.  
By using this tool, you agree to use it only for lawful purposes.

## Features
- Multiple WAF bypass techniques
- Dynamic request throttling
- Randomized user agents
- Session rotation
- IP spoofing via headers
- URL encoding variations

## Installation
```bash
git clone https://github.com/TEMMAM/WordPress-brute-force-.git
cd WordPress-brute-force-
pip install -r requirements.txt

## Usage 

from src.waf_bruteforce import WAFBruteforcer

tester = WAFBruteforcer(
    target_url="http://test-site.com/wp-login.php",
    username="admin",
    wordlist_path="wordlists/example_passwords.txt"
)
tester.execute_attack()

