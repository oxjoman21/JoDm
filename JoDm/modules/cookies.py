import requests
import random
from .log import Log 

log = Log()

def get_cookies():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get("https://discord.com/register", headers=headers)
        if r.status_code == 200:
            cookies = r.cookies
            cookie_string = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            
            if cookie_string:
                log.suc("Got Fresh Cookies!")
                with open("data/cookies.txt", "a") as f:
                    f.write(f"{cookie_string}\n")
                return cookie_string
                
        # Wenn neue Cookies fehlschlagen, verwende gespeicherte
        log.inf("Trying saved cookies...")
        with open("data/cookies.txt", "r") as f:
            cookies = f.read().splitlines()
            if cookies:
                log.suc("Using saved cookie")
                return random.choice(cookies)
                
        log.error("Failed to get cookies")
        return None
        
    except Exception as e:
        log.error(f"Cookie error: {str(e)}")
        return None