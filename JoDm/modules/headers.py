import base64
import json
from .build_num import get_build_number
from .cookies import get_cookies
from .log import Log
from .config import config

log = Log()

def get_headers(token):
    try:
        if not token:
            log.error("No token provided")
            return None
            
        if config.get("debug"):
            log.dbg(f"Generating headers for token --> {token[:25]}...")
            
        cookie = get_cookies()
        if not cookie:
            return None
            
        if config.get("debug_headers"):
            log.dbg(f"Using cookie --> {cookie}")
            
        build_nm = get_build_number()
        if not build_nm:
            return None
            
        if config.get("debug"):
            log.dbg(f"Using build number --> {build_nm}")

        x_super_properties = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "de-DE",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "browser_version": "124.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": build_nm,
            "client_event_source": None
        }

        try:
            x_super_properties_encoded = base64.b64encode(
                json.dumps(x_super_properties, separators=(',', ':')).encode('utf-8')
            ).decode('utf-8')
        except Exception as e:
            log.error(f"Failed to encode properties --> {str(e)}")
            return None

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "de-DE,de;q=0.9",
            "authorization": token,
            "content-type": "application/json",
            "cookie": cookie,
            "origin": "https://discord.com",
            "referer": "https://discord.com/channels/@me",
            "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "x-debug-options": "bugReporterEnabled",
            "x-discord-locale": "de",
            "x-discord-timezone": "Europe/Berlin",
            "x-super-properties": x_super_properties_encoded,
            "TE": "trailers"
        }

        if headers:
            if config.get("debug"):
                log.dbg("Headers generated successfully")
            return headers

        log.error("Failed to generate headers")
        return None

    except Exception as e:
        log.error(f"Error generating headers --> {str(e)}")
        return None
