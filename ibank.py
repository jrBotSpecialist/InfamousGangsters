import requests
from bs4 import BeautifulSoup
from melt import get_post_secret
from dupe import MultiSession

def ibank(multi_session):
    url = "https://infamousgangsters.com/site.php?page=bank"

    # Define the headers and data for the POST request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
    }
    
    post_secret = get_post_secret(multi_session)

    data = {
        "postsecret": post_secret,
        "bankmoneyadd": "53400000000",
        "deposit": "Do it",
        "bankmoneywit": "",
    }
    multi_session = MultiSession("session_cookie.json")
    # Send the POST request
    response_list = multi_session.post(url, data=data, headers=headers)
    
    for response in response_list:
        if response.status_code == 200:
            # Parse the HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the specific message and print it
        spacer_div = soup.find("div", class_="spacer")
        if spacer_div:
            specific_text = spacer_div.text.strip()
            print("Message:", specific_text)
        else:
            print("Spacer div not found in the response.")
    else:
        print("POST request failed")
