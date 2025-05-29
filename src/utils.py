import random
import time
import string
from urllib.parse import quote

def generate_random_user_agent():
    """Generate rotating user agents"""
    versions = {
        'Chrome': f'{random.randint(80, 115)}.0.{random.randint(1000, 9999)}.{random.randint(0, 100)}',
        'Firefox': f'{random.randint(70, 115)}.0',
        'Safari': '605.1.15'
    }
    templates = [
        f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{versions["Chrome"]} Safari/537.36',
        f'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{versions["Firefox"]}) Gecko/20100101 Firefox/{versions["Firefox"]}',
        f'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{versions["Safari"]} Safari/605.1.15'
    ]
    return random.choice(templates)

def random_delay(min_sec=1, max_sec=3):
    """Random delay between requests"""
    time.sleep(random.uniform(min_sec, max_sec))

def obfuscate_payload(payload):
    """Apply random obfuscation techniques"""
    if random.choice([True, False]):
        return quote(payload)
    return payload

def get_random_string(length=8):
    """Generate random strings for cache busting"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
