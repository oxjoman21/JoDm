import requests
from .log import Log
from .headers import get_headers
from .proxy import ProxyHandler
from .config import config 
from .solver import solve
import time 
import random 

log = Log()

def start_messaging(user_id, token, message):
    try:
        session = requests.Session()
        headers = get_headers(token)
        if not headers:
            return False
            
        url = "https://discord.com/api/v9/users/@me/channels"
        payload = {"recipient_id": user_id}

        proxies = ProxyHandler().get_proxy() if config.get("use_proxies") else None
        
        r = session.post(url, headers=headers, json=payload, proxies=proxies, timeout=config.get("timeout", 10))
        
        if r.status_code == 429:
            retry_after = float(r.json().get('retry_after', 5))
            log.error(f"Rate limited, waiting {retry_after}s")
            time.sleep(retry_after + 0.5)
            return False
            
        r.raise_for_status()
        channel_id = r.json().get("id")
        
        if channel_id:
            log.suc(f"Opened Dm --> {token[:25]}... --> {user_id}")
            return send_message(channel_id, message, token, headers, session)
            
        return False
        
    except Exception as e:
        if config.get("debug"):
            log.error(f"DM failed --> {str(e)}")
        return False

def send_message(channel_id, message, token, headers, session):
    try:
        url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
        payload = {
            "content": message,
            "nonce": str(random.randint(1000000000000000000, 9999999999999999999)),
            "flags": 0,
            "mobile_network_type": "unknown",
            "tts": False
        }

        proxies = ProxyHandler().get_proxy() if config.get("use_proxies") else None
        
        r = session.post(
            url=url,
            headers=headers,
            json=payload, 
            proxies=proxies,
            timeout=config.get("timeout", 10)
        )
        
        if r.status_code == 429:
            retry_after = float(r.json().get('retry_after', 5))
            log.error(f"Rate limited, waiting {retry_after}s")
            time.sleep(retry_after + 0.5)
            return False

        if "captcha-required" in r.text:
            r = r.json()
            captcha_sitekey = r.get("captcha_sitekey")
            captcha_rqdata = r.get("captcha_rqdata")
            captcha_rqtoken = r.get("captcha_rqtoken")
            log.inf(f"Solving Captcha --> {captcha_sitekey}")

            solution = solve(captcha_sitekey, captcha_rqdata)
            if not solution:
                log.error("Failed to solve captcha")
                return False

            headers.update({
                "X-Captcha-Key": solution,
                "X-Captcha-Rqtoken": captcha_rqtoken
            })

            r = session.post(
                url=url,
                headers=headers,
                json=payload,
                proxies=proxies,
                timeout=config.get("timeout", 10)
            )

            if r.status_code == 200:
                log.suc(f"Sent Message after Captcha --> {token[:25]}... --> {channel_id}")
                return True
            else:
                log.error(f"Failed to send Message after Solve --> {token[:25]}... --> {channel_id} --> {r.text}")
                return False
        
        if r.status_code == 200:
            log.suc(f"Sent Message --> {token[:25]}... --> {channel_id}")
            return True
            
        log.error(f"Failed to send message: Status {r.status_code} --> {r.text}")
        return False
        
    except Exception as e:
        if config.get("debug"):
            log.error(f"Send failed --> {str(e)}")
        return False