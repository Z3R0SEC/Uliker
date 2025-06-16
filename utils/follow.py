import uuid
import json
import requests
from requests import get
from bs4 import BeautifulSoup as bs

def id(profile_url):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; A507DL Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/136.0.7103.125 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/506.0.0.61.109;]",
        "Cookie": "hdhhdh"
    })
    username = profile_url.strip().split("/")[-1].split("?")[0]
    url = f"https://mbasic.facebook.com/{username}"
    res = session.get(url, allow_redirects=False)
    if 'Location' in res.headers:
        location = res.headers['Location']
        if location.startswith("fb://profile/"):
            return location.split("fb://profile/")[1].split("?")[0]
    res = session.get(url)
    if "login" in res.url or "save-device" in res.url:
        return None
    soup = BeautifulSoup(res.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if "profile.php?id=" in href:
            return href.split("profile.php?id=")[1].split("&")[0]
    if "entity_id" in res.text:
        return res.text.split('entity_id":"')[1].split('"')[0]
    return None



def follow(target_url, token_list, limit):
    def extract_uid(url):
        return url.split("/")[-1].strip()

    uid = id(target_url)
    print(uid)

    good = 0
    fail = 0
    total = 0

    for token in token_list:
        if int(total) >= int(limit):
            break

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0"
        }

        endpoint = f"https://graph.facebook.com/v18.0/{uid}/subscribers"
        response = requests.post(endpoint, headers=headers)

        if response.status_code == 200:
            good += 1
        else:
            fail += 1

        total += 1

    return f"Sent {good} follower(s). {fail} token(s) failed & {total}/{limit} tokens were used!"


def isvalid(token):
    r = requests.get("https://graph.facebook.com/me", headers={
        "Authorization": f"Bearer {token}"
    })
    return r.status_code == 200



def delete(access_token, page_id="me", limit=20):
    graph_url = "https://graph.facebook.com/v19.0"
    url = f"{graph_url}/{page_id}/posts"
    params = {
        "access_token": access_token,
        "limit": limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "data" not in data:
        return "No posts found on your timeline. Photo deletion is not supported."

    deleted = 0
    failed = 0
    for post in data["data"]:
        post_id = post["id"]
        del_url = f"{graph_url}/{post_id}"
        del_res = requests.delete(del_url, params={"access_token": access_token})
        if del_res.status_code == 200:
            deleted += 1
        else:
            failed += 1
    return f"Deleted {deleted} posts Successfully, {failed} more failed to be deleted via graph!"



def Shield(access_token):
    session_id = str(uuid.uuid4())
    mutation_id = str(uuid.uuid4())

    graphql_variables = {
        "0": {
            "is_shielded": True,
            "session_id": session_id,
            "client_mutation_id": mutation_id
        }
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
    }

    url = "https://graph.facebook.com/graphql"

    status_url = "https://graph.facebook.com/v19.0/me/profile_picture_safety"
    current = requests.get(status_url, params={"access_token": access_token}).json()
    current_state = current.get("is_shielded", False)

    new_state = not current_state
    graphql_variables["0"]["is_shielded"] = new_state
    payload = {
        "variables": json.dumps(graphql_variables),
        "method": "post",
        "doc_id": "1477043292367183",
        "query_name": "IsShieldedSetMutation",
        "strip_defaults": "false",
        "strip_nulls": "false",
        "locale": "en_ZA",
        "client_country_code": "US",
        "fb_api_req_friendly_name": "IsShieldedSetMutation",
        "fb_api_caller_class": "IsShieldedSetMutation",
        "access_token": access_token
    }

    res = requests.post(url, data=payload, headers=headers).json()

    if "errors" in res:
        return f"Activation Error - {res['errors'][0].get('message', 'Unknown error')}"
    else:
        return f"Successfully Turned {'ON' if new_state else 'OFF'}. Profile Shield"
