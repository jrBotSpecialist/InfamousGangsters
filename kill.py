import re
from dupe import MultiSession
from melt import get_post_secret
import base64
import requests
# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

def euo(multi_session):
  print('Starting online list extraction..')
  url = "https://infamousgangsters.com/site.php?page=users_online"

  headers_get = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
  }

  multi_session = MultiSession("session_cookie.json")

  response_tuple = multi_session.get(url, headers=headers_get)

  response = response_tuple[0]

  if response.status_code == 200:

    # extract profile links
    links = re.findall(r'<a href="site\.php\?page=viewprofile&user=(\w+)">', response.text)

    # initialize counter
    count = 1

    # open file for writing 
    with open('search_list.txt', 'w') as f:

      for link in links:
        print(link, file=f)

    # print numbered usernames to console
    for link in links:
      print(str(count) + ". " + link)
      count += 1

  return links

def save_captcha_image(multi_session, image_file_path):
    url = "https://infamousgangsters.com/crimes-verify.php?bullets=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "image/avif,image/webp,*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "referrer": "https://infamousgangsters.com/site.php?page=kill"
    }
    multi_session = MultiSession("session_cookie.json")
    response_list = multi_session.get(url, headers=headers)

    for response in response_list:
     if response.status_code == 200:
        # Save the image as a PNG file in the specified file path
        with open(image_file_path, 'wb') as image_file:
            image_file.write(response.content)
        print(YELLOW + 'Captcha image saved successfully' + ENDC)
     else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")

# Define the global variable
result = None

def solve(f):
    with open(f, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('ascii')
        url = 'https://api.apitruecaptcha.org/one/gettext'

        data = { 
            'userid':'Macs1991', 
            'apikey':'QnUjH2qqt8IBBHSg4yXq',  
            'data': encoded_string
        }
        response = requests.post(url=url, json=data)
        data = response.json()
        return data

search_counter = 0

def sfm(multi_session, usernames):
    global search_counter
    for username in usernames:
        url = "https://infamousgangsters.com/site.php?page=kill"

        headers_get = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        }

        post_secret = get_post_secret(multi_session)

        payload = {
            "postsecret": post_secret,
            "VwLEMlW2OGV2xyVb5Ya02j7umOjyWcMPsxer9+u0=": "",
            "WQINd1W2OGW/huDxrsBprLkw2txPO0plBAsv0EwD=": "",
            "WgJLn1W2OGUYft/aCjkX/kzYF/pZo/JBF4ZLCRMn=": username,
            "XAKuIFW2OGViyqHPb5HygD7ZXqPa0SV1Sx7vypRN=": "",
            "XgLm9FW2OGU3HGog3rtC+jR7sfw/QhTnR92Xl3nL=": "",
            "YAJgzFW2OGXwOAyhtpJGVyK/nhNCCK7wUcgrNzs3=": "",
            "YQLrT1W2OGUC4i5Lh4vkzxxO1LRTx9nOP/iiT0/A=": "",
            "YgKX9VW2OGUUNkVSAPXj7rZT9EWUWur84KBvWrc8=": "",
            "ZAI3w1W2OGVRMKOd/nI/VBxFeHBwULPato4MsAvi": "23",
            "ZQJOGFW2OGWephKLf94PUYdVBgSs4+WZgLcJoRj6=": "",
            "ZgLkg1W2OGXhTeXZrNfu2l0Q4f3oL/LEzzkdo5UH=": "",
            "aAIYalW2OGWjlAMa7Ph4sloxAFGvL04rxhXRfB7N=": "",
            "aQJyUVW2OGUNGuCEzMZxgftgK3ha/u8+1Pbz97EQ=": "",
            "submit": "Search!"
        }

        multi_session = MultiSession("session_cookie.json")

        response_tuple = multi_session.post(url, headers=headers_get, data=payload)

        response = response_tuple[0]
        counter = search_counter
        if response.status_code == 200:
            search_counter += 1
            print(GREEN + "Search started for: ", username + ENDC)

        if search_counter == 50:
            # Call the sfmc function after 50 searches
            sfmc(multi_session, usernames, counter)
            break



def sfmc(multi_session, usernames, counter):
  global search_counter
  
  search_counter = counter
  
  for username in usernames[search_counter:]:
    save_captcha_image(multi_session, "kill.png")

    url = "https://infamousgangsters.com/site.php?page=kill"
    
    headers_get = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    }
    result = solve("C:\\Users\\Student\\Desktop\\InfamousGangsters\\python-ig\\kill.png")
    ocr_result = result.get("result")
    post_secret = get_post_secret(multi_session)
    print("Catpcha solved: ", ocr_result,"User searched: ", username)
    payload = {
    "postsecret": post_secret,
    "VwLEMlW2OGV2xyVb5Ya02j7umOjyWcMPsxer9+u0=": "",
    "WQINd1W2OGW/huDxrsBprLkw2txPO0plBAsv0EwD=": "",
    "WgJLn1W2OGUYft/aCjkX/kzYF/pZo/JBF4ZLCRMn=": username,
    "XAKuIFW2OGViyqHPb5HygD7ZXqPa0SV1Sx7vypRN=": "",
    "XgLm9FW2OGU3HGog3rtC+jR7sfw/QhTnR92Xl3nL=": "",
    "YAJgzFW2OGXwOAyhtpJGVyK/nhNCCK7wUcgrNzs3=": "", 
    "YQLrT1W2OGUC4i5Lh4vkzxxO1LRTx9nOP/iiT0/A=": "",
    "YgKX9VW2OGUUNkVSAPXj7rZT9EWUWur84KBvWrc8=": "",
    "ZAI3w1W2OGVRMKOd/nI/VBxFeHBwULPato4MsAvi": "23",
    "ZQJOGFW2OGWephKLf94PUYdVBgSs4+WZgLcJoRj6=": "",
    "ZgLkg1W2OGXhTeXZrNfu2l0Q4f3oL/LEzzkdo5UH=": "",
    "aAIYalW2OGWjlAMa7Ph4sloxAFGvL04rxhXRfB7N=": "",
    "aQJyUVW2OGUNGuCEzMZxgftgK3ha/u8+1Pbz97EQ=": "", 
    "bulletcode": ocr_result,
    "submit": "Search!"
    }
    
    multi_session = MultiSession("session_cookie.json")

    response_tuple = multi_session.post(url, headers=headers_get, data=payload)
    search_counter += 1
    response = response_tuple[0]

    if response.status_code == 200:
        print(GREEN + "Search started for: ", username + ENDC)
