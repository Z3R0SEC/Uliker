import random, uuid, string
import requests as httpx


def get_cookie(user, passw):
    accessToken = '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'error_detail_type': 'button_with_disabled',
        'source': 'device_based_login',
        'email': user,
        'password': passw,
        'access_token': accessToken,
        'generate_session_cookies': '1',
        'meta_inf_fbmeta': '',
        'advertiser_id': str(uuid.uuid4()),
        'currently_logged_in_userid': '0',
        'locale': 'en_US',
        'client_country_code': 'US',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
        'api_key': '62f8ce9f74b12f84c123cc23437a4a32'
    }
    headers = {
        'User-Agent': "[FBAN/FB4A;FBAV/196.0.0.29.99;FBPN/com.facebook.katana;FBLC/en_US;FBBV/135374479;FBCR/SMART;FBMF/samsung;FBBD/samsung;FBDV/SM-A720F;FBSV/8.0.0;FBCA/armeabi-v7a:armeabi;FBDM={density=3.0,width=1080,height=1920};FB_FW/1;]",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com',
        'X-FB-Net-HNI': str(random.randint(10000, 99999)),
        'X-FB-SIM-HNI': str(random.randint(10000, 99999)),
        'X-FB-Connection-Type': 'MOBILE.LTE',
        'X-Tigon-Is-Retry': 'False',
        'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;nc=1;fc=0;bc=0;cid=62f8ce9f74b12f84c123cc23437a4a32',
        'x-fb-device-group': str(random.randint(1000, 9999)),
        'X-FB-Friendly-Name': 'ViewerReactionsMutation',
        'X-FB-Request-Analytics-Tags': 'graphservice',
        'X-FB-HTTP-Engine': 'Liger',
        'X-FB-Client-IP': 'True',
        'X-FB-Connection-Bandwidth': str(random.randint(20000000, 30000000)),
        'X-FB-Server-Cluster': 'True',
        'x-fb-connection-token': '62f8ce9f74b12f84c123cc23437a4a32'
    }
    try:
        response = httpx.post("https://b-graph.facebook.com/auth/login", headers=headers, data=data).json()
        if "session_key" in response:
            sb_value = ''.join(random.choices(string.ascii_letters+string.digits+'_', k=24))
            cookie_string = f"sb={sb_value};" + ';'.join(i['name']+'='+i['value'] for i in response['session_cookies'])
            token = response['access_token']
            uid = response['uid']
            name = httpx.get(f"https://graph.facebook.com/v19.0/me?fields=name&access_token={token}").json()
            print(name)
            pp = httpx.get(f"https://graph.facebook.com/{uid}/picture?width=512&height=512&access_token=6628568379%7Cc1e620fa708a1d5696fb991c1bde5662", allow_redirects=True).url
            return {
                "status": True,
                "uid": uid,
                "name": name,
                "photo": pp,
                "cookie": cookie_string,
                "token": token
            }, True
        else:
            return False, response['error']['message']
    except Exception as e:
        print(e)
        return False, f"Error: {e} | Log this error to +27847611848"
