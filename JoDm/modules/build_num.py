import re
import tls_client

headers = {
    "Accept": "*/*",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Referer": "https://discord.com/login",
    "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}

session = tls_client.Session(client_identifier="chrome_124")

def extract_asset_files():
    try:
        request = session.get("https://discord.com/login", headers=headers)
        if request.status_code == 200:
            pattern = r'<script\s+src="([^"]+\.js)"\s+defer>\s*</script>'
            matches = re.findall(pattern, request.text)
            return matches
    except:
        pass
    return []

def get_build_number():
    CURRENT_BUILD = "251937" 
    
    try:
        files = extract_asset_files()
        if not files:
            return CURRENT_BUILD
            
        for file in files:
            try:
                build_url = f"https://discord.com{file}"
                response = session.get(build_url, headers=headers)
                if response.status_code == 200 and "buildNumber" in response.text:
                    build_number = response.text.split('build_number:"')[1].split('"')[0]
                    return build_number
            except:
                continue
                
    except Exception as e:
        pass
        
    return CURRENT_BUILD