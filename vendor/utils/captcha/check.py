# Python

import requests
from settings import settings

# check captcha
async def check_captcha(g_recaptcha_response, remote_ip):
    query_string = '''?secret={0}&response={1}&remoteip={2}'''.format(
        settings.get('captcha_secret_key'),
        g_recaptcha_response,
        remote_ip
    )
    api_call = "https://www.google.com/recaptcha/api/siteverify" + query_string
    api_response = await requests.post(api_call)
    api_response = api_response.json()
    if api_response["success"]:
        return True
    return False
