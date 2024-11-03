#   Feel free to Skid!
#   3.11.2024 | Idk if its flagged atm but it works!
#

from modules.banner import print_banner
from modules.headers import get_headers
from modules.dm import start_messaging
from modules.log import Log
from modules.config import config
from modules.scraper import scrape_members  

import threading
import random
import queue
import time
import os 
from colorama import Fore 
from typing import List, Optional

log = Log()

class MessageWorker:
    def __init__(self, message: str, tokens: List[str], user_ids: List[str]):
        self.message = message
        self.tokens = tokens
        self.user_ids = user_ids
        self.used_pairs = set()
        
    def get_next_pair(self) -> Optional[tuple]:
        try:
            if not self.tokens or not self.user_ids:
                return None
                
            token = random.choice(self.tokens)
            user_id = random.choice(self.user_ids)
            
            pair = (token, user_id)
            attempts = 0
            while pair in self.used_pairs and attempts < 50:
                token = random.choice(self.tokens)
                user_id = random.choice(self.user_ids)
                pair = (token, user_id)
                attempts += 1
                
            self.used_pairs.add(pair)
            return pair
            
        except Exception as e:
            if config.get("debug"):
                log.error(f"Error getting next pair: {str(e)}")
            return None

    def worker(self):
        while True:
            try:
                pair = self.get_next_pair()
                if not pair:
                    if config.get("debug"):
                        log.dbg("No more token/user pairs available")
                    log.error("No valid token/user pairs left")
                    break
                
                token, user_id = pair
                
                for _ in range(config["attempts"]):
                    if start_messaging(user_id, token, self.message):
                        break
                    time.sleep(config["retry_delay"])
                    
                time.sleep(config["delay"])
                
            except Exception as e:
                if config["debug"]:
                    log.error(f"Worker error: {str(e)}")
                time.sleep(config["retry_delay"])

def load_tokens(filename: str = "data/tokens.txt") -> List[str]:
    try:
        with open(filename, "r", encoding='utf-8') as file:
            tokens = [line.strip() for line in file.readlines() if line.strip()]
            
        if not tokens:
            log.fatal("No tokens found in tokens.txt")
            return []
            
        log.suc(f"Loaded {len(tokens)} tokens")
        return tokens
        
    except FileNotFoundError:
        log.fatal(f"File {filename} not found")
        return []
    except Exception as e:
        log.fatal(f"Error loading tokens --> {str(e)}")
        return []

def load_ids(filename: str = "data/ids.txt") -> List[str]:
    try:
        with open(filename, "r", encoding='utf-8') as file:
            user_ids = list(set([line.strip() for line in file.readlines() if line.strip()]))
            
        if not user_ids:
            log.fatal("No user IDs found in ids.txt")
            return []
            
        log.suc(f"Loaded {len(user_ids)} unique user IDs")
        return user_ids
        
    except FileNotFoundError:
        log.fatal(f"File {filename} not found")
        return []
    except Exception as e:
        log.fatal(f"Error loading user IDs --> {str(e)}")
        return []

def main():
    os.system("cls")
    print_banner()
    
    if config.get("debug"):
        log.dbg("Debug mode enabled")
        if config.get("debug_requests"):
            log.dbg("Request debugging enabled")
        if config.get("debug_headers"):
            log.dbg("Header debugging enabled")
    
    tokens = load_tokens()
    if not tokens:
        return
        
    if config.get("use_scraper") and config.get("server_id"):
        log.inf("Scraping members...")
        scrape_members(tokens[0], config["server_id"])
        
    user_ids = load_ids()
    if not user_ids:
        return

    time.sleep(3)

    os.system("cls")

    message = input(f"{Fore.LIGHTYELLOW_EX}[/]{Fore.RESET} Message to send --> ").strip()
    if not message:
        log.fatal("Message cannot be empty")
        return
    
    worker = MessageWorker(message, tokens, user_ids)
    threads = []
    
    for i in range(config["threads"]):
        thread = threading.Thread(target=worker.worker, daemon=True)
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        log.inf("Keyboard Interrupt --> Exiting...")
        
if __name__ == "__main__":
    main()

