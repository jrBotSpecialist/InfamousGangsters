import requests
from bs4 import BeautifulSoup
from dupe import MultiSession
from melt import get_post_secret

def sellpointsvalue(multi_session):
    url = "https://infamousgangsters.com/site.php?page=quicktrade"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
    }

    referrer = "https://infamousgangsters.com/site.php?page=bulletfactory"
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")

    response_list = multi_session.get(url, headers=headers)
    
    for response in response_list:
     if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the input field with name="smoney"
        smoney_input = soup.find('input', {'name': 'smoney'})

        if smoney_input:
            smoney_value = smoney_input['value']
            print(smoney_value)
            return smoney_value
        else:
            return "Value not found in the response."

    return "Failed to make the GET request."


def buypointsvalue(multi_session):
    url = "https://infamousgangsters.com/site.php?page=quicktrade"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
    }

    referrer = "https://infamousgangsters.com/site.php?page=bulletfactory"
    
    
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
    response_list = multi_session.get(url, headers=headers)
    
    for response in response_list:
      if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the input field with name="smoney"
        bmoney_input = soup.find('input', {'name': 'bmoney'})

        if bmoney_input:
            bmoney_value = bmoney_input['value']
            print(bmoney_value)
            return bmoney_value
        else:
            return "Value not found in the response."

    return "Failed to make the GET request."

def sellpoints(multi_session, smoney_value):
    url = "https://infamousgangsters.com/site.php?page=quicktrade"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }

    referrer = "https://infamousgangsters.com/site.php?page=quicktrade"
    post_secret = get_post_secret(multi_session)
    # Define the POST data
    post_data = {
        "postsecret": post_secret,
        "spoints": "15",
        "smoney": smoney_value,
        "hide": "yes",
        "submit": "Put offer!"
    }
    
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")

    response_list = multi_session.post(url, headers=headers, data=post_data)
    
    for response in response_list:
     if response.status_code == 200:
        print("Points added to quicktrade!")
     else:
        print(f"Failed to make the POST request. Status code: {response.status_code}")

def buypoints(multi_session, bmoney_value):
    url = "https://infamousgangsters.com/site.php?page=quicktrade"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
    }

    referrer = "https://infamousgangsters.com/site.php?page=quicktrade"
    post_secret = get_post_secret(multi_session)
    # Define the POST data
    post_data = {
        "postsecret": post_secret,
        "bpoints": "18",
        "bmoney": bmoney_value,
        "hide": "no",
        "submit": "Put offer!"
    }

    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")

    response_list = multi_session.post(url, headers=headers, data=post_data)
    
    for response in response_list:
     if response.status_code == 200:
        print("Money added to quicktrade!")
     else:
        return f"Failed to make the POST request. Status code: {response.status_code}"