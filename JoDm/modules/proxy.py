import random
from .log import Log
from .config import config

log = Log()

class ProxyHandler:
    def __init__(self):
        self.proxies = []
        if config.get("use_proxies"):
            self.load_proxies()

    def load_proxies(self):
        try:
            with open("data/proxies.txt", "r") as f:
                for line in f:
                    line = line.strip()
                    if ":" in line:
                        parts = line.split(":")
                        if len(parts) >= 4:
                            username, password = parts[0], parts[1]
                            host, port = parts[-2], parts[-1]
                            proxy = f"http://{username}:{password}@{host}:{port}"
                            self.proxies.append(proxy)
            if self.proxies:
                log.suc(f"Loaded {len(self.proxies)} proxies")
            else:
                log.error("No valid proxies found")
        except Exception as e:
            log.error(f"Failed to load proxies --> {e}")

    def get_proxy(self):
        if not self.proxies or not config.get("use_proxies"):
            return None
        proxy = random.choice(self.proxies)
        return {"http": proxy, "https": proxy}
