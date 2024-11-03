import json
from .log import Log

log = Log()

def load_config():
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
            
        return {
            "timeout": config.get("timeout", 10),
            "attempts": config.get("attempts", 3),
            "debug": config.get("debug", False),
            "threads": config.get("threads", 1),
            "delay": config.get("delay", 60),
            "retry_delay": config.get("retry_delay", 5),
            "use_proxies": config.get("use_proxies", False),
            "use_scraper": config.get("use_scraper", False),
            "server_id": config.get("server_id", ""),
            "captcha_service": config.get("captcha_service",""),
            "captcha_key": config.get("captcha_key","")
        }
    except Exception as e:
        log.error(f"Error loading config --> {e}")
        return {
            "timeout": 10,
            "attempts": 3, 
            "debug": False,
            "threads": 1,
            "delay": 60,
            "retry_delay": 5,
            "use_proxies": False,
            "use_scraper": False,
            "server_id": ""
        }

config = load_config()