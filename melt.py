import requests
from bs4 import BeautifulSoup
import re
from dupe import MultiSession

# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

# Function to fetch Post Secret
def get_post_secret(multi_session):
    print(YELLOW + 'Getting post secret for melt page...' + ENDC)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://infamousgangsters.com/site.php?page/postsecret'  # Set the referrer in the headers
        }
        multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
    
        post_secret_response_list = multi_session.get('https://infamousgangsters.com/site.php?page=bullets', headers=headers)
        for response in post_secret_response_list:
            if response.status_code == 200:
                post_secret_response_text = response.text
                post_secret_html = BeautifulSoup(post_secret_response_text, 'html.parser')
                post_secret_input = post_secret_html.find('input', {'name': 'postsecret'})
                post_secret_value = post_secret_input['value'] if post_secret_input else None
                return post_secret_value

        print(RED + 'Failed to retrieve the post_secret value.' + ENDC)
        return None

    except Exception as error:
        print(error)
        return None

def fetch_melt(multi_session):
    print(YELLOW + 'Melting a car...' + ENDC)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Referer': 'https://infamousgangsters.com/site.php?page=bullets'
        }

        post_secret_value = get_post_secret(multi_session)

        if post_secret_value:
            print(YELLOW + f'Using post_secret value: {post_secret_value}' + ENDC)
            multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")

            bullets_response_list = multi_session.get('https://infamousgangsters.com/site.php?page=bullets', headers=headers)
            for bullets_response in bullets_response_list:
             if bullets_response.status_code == 200:
                bullets_response_text = bullets_response.text
                bullets_html = BeautifulSoup(bullets_response_text, 'html.parser')
                radio_buttons = bullets_html.find_all('input', {'type': 'radio'})

                if len(radio_buttons) >= 50:  # Changed to 50 because lists are zero-indexed
                    fifth_button_value = radio_buttons[49]['value']  # Changed to 49
                    post_body = f'postsecret={post_secret_value}&meltcar={fifth_button_value}&melt=Melt+car%21&pagenumber=0'

                    # Make the POST request
                    melt_response_list = multi_session.post('https://infamousgangsters.com/site.php?page=bullets', headers=headers, data=post_body)
                    
                    for melt_response in melt_response_list:
                     if melt_response.status_code == 200:
                        melt_response_text = melt_response.text
                        # Extract text from response
                        match = re.search(r'<DIV class=spacer>(.*?)</div>', melt_response_text)
                        if match:
                            text = match.group(1)
                            text = re.sub('<.*?>', '', text)
                            print(GREEN + text + ENDC)
                        else:
                            print(RED + 'Text not found in melt response.' + ENDC)
                     else:
                        print(RED + f'Melt POST request failed with status code {melt_response.status_code}' + ENDC)
                else:
                    print(RED + 'Radio buttons not found or not enough options available.' + ENDC)
             else:
                print(RED + f'Bullets GET request failed with status code {bullets_response.status_code}' + ENDC)
        else:
            print(RED + 'Failed to get post_secret value. Cannot proceed with the melt.' + ENDC)
    except Exception as error:
        print(error)