import requests 
from .log import Log 
from .config import config

log = Log()

def solve(sitekey,rqdata):

    captcha_service = config.get("captcha_service").lower()
    captcha_key = config.get("captcha_key")

    if captcha_service == "csolver":
        return csolver(sitekey,rqdata,captcha_key)

def csolver(sitekey,rqdata,captcha_key):

    headers = {'API-Key': captcha_key}

    payload = {
    'task': 'hCaptchaEnterprise',
    'sitekey': sitekey,
    'site': "discord.com",
#    'proxy': proxy,
    'rqdata': rqdata
}

    try:
        r = requests.post("https://api.csolver.xyz/solve", headers=headers, json=payload)

        if r.status_code == 200:
            job_id = r.json().get("job_id")

        if job_id:

            headers = {'API-Key': captcha_key}

            while True:

                r = requests.get(f"https://api.csolver.xyz/result/{job_id}", headers=headers)

                if r.status_code == 200:
                    r = r.json()
                    status = r.get('status')
                    if status == 'completed':
                        solution = r.get("solution")
                        log.suc(f"Solved Captcha --> {solution[:20]}")
                        return solution
                    else:
                        continue

    except Exception as e:
        log.error(f"Error solving captcha --> {str(e)}")

