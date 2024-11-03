import requests
from .log import Log
from .headers import get_headers
from .config import config
import time

log = Log()

def scrape_members(token, server_id):
    if not config.get("use_scraper"):
        return []
        
    headers = get_headers(token)
    if not headers:
        return []

    channels_url = f"https://discord.com/api/v9/guilds/{server_id}/channels"
    scraped_ids = set()
    
    try:
        session = requests.Session()
        retries = 3
        
        for attempt in range(retries):
            try:
                r = session.get(channels_url, headers=headers)
                
                if r.status_code == 429:
                    retry_after = r.json().get('retry_after', 5)
                    log.error(f"Rate limited, waiting {retry_after}s")
                    time.sleep(float(retry_after))
                    continue
                elif r.status_code == 403:
                    log.error("No access to server")
                    return []
                    
                r.raise_for_status()
                
                channels = r.json()
                text_channels = [c["id"] for c in channels if c["type"] == 0]

                if config.get("debug"):
                    log.dbg(f"Found {len(text_channels)} text channels")

                for channel_id in text_channels:
                    try:
                        messages_url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=100"
                        r = session.get(messages_url, headers=headers)
                        
                        if r.status_code == 403:
                            continue
                            
                        r.raise_for_status()
                        messages = r.json()
                        
                        for msg in messages:
                            author = msg.get("author", {})
                            if not author.get("bot"):
                                user_id = author.get("id")
                                if user_id:
                                    scraped_ids.add(user_id)
                                    if config.get("debug"):
                                        log.dbg(f"Found member --> {user_id}")
                        
                    except Exception as e:
                        if config.get("debug"):
                            log.dbg(f"Error scraping channel {channel_id} --> {str(e)}")
                        continue

                if scraped_ids:
                    log.suc(f"Scraped {len(scraped_ids)} members")
                    with open("data/ids.txt", "a") as f:
                        for user_id in scraped_ids:
                            f.write(f"{user_id}\n")
                
            except Exception as e:
                log.error(f"Failed to scrape members --> {e}")
                if config.get("debug"):
                    log.dbg(f"Full error --> {str(e)}")
                continue
                
        return list(scraped_ids)
                
    except Exception as e:
        log.error(f"Critical error in scraper --> {e}")
        return []