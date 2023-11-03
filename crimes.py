import requests
from bs4 import BeautifulSoup
from dupe import MultiSession

# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

# Function to fetch crimes
def fetch_crimes(multi_session):
    print(YELLOW + "Doing crimes" + ENDC)
    # Your POST request URL
    post_request_url = "https://infamousgangsters.com/site.php?page=crimes"
    
    # Define your complete POST data as a string
    post_data = (
        "+++++++++++++e43fd%5B%5D++++++++++++++=e43fd&"
        "++++++++++++e43fd%5B%5D+++++++++++++++++=af557a9630d3d83bab5&"
        "++++++++++++e43fd%5B%5D++++++%5B%5D=e31f6&"
        "++++++++++++++e43fd%5B%5D+++++%5B%5D=fc6eef2fbbd6bdd&"
        "+++++++e43fd%5B%5D+++++++++++++++++++++%5B%5D=74ebe&"
        "++++++++++++e43fd%5B%5D++++++++++++++++++++%5B%5D=b1eda4277d9d86c901e&"
        "+++++++++++++++++e43fd%5B%5D++++++++++++++%5B%5D=145a7a3a7&"
        "+++++++++++++++++e43fd%5B%5D++++++++%5B%5D=c61d6&"
        "++++++++++++e43fd%5B%5D+++++++++++++++%5B%5D=adf70894&"
        "+++++++++++++e43fd%5B%5D+++%5B%5D=01d2&"
        "++++++++e43fd%5B%5D+++++++++++++++crimetypes%5B%5D=822a0ee&"
        "submit=Commit%21"
    )
    
    # Define headers for the POST request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }
    
    try:
        # Make the POST request with the session and data
        multi_session = MultiSession("session_cookie.json")

        post_response_list = multi_session.post(post_request_url, data=post_data, headers=headers)
        
        # Handle the response as needed
        for response in post_response_list:
         if response.status_code == 200:
            
            # Extract and filter text from the response using BeautifulSoup
            crimesResponseText = response.text
            crimesHTML = BeautifulSoup(crimesResponseText, 'html.parser')
            messages = [node.text.strip() for node in crimesHTML.select('.bodymain') if
                        any(keyword in node.text for keyword in ["You successfully", "You were caught", "You found"])]

            for message in messages:
                print(GREEN + message + ENDC)
         else:
            print(f"POST request failed with status code {response.status_code}")
    except Exception as error:
        print(f'An error occurred while making the fetch request to the bullets page: {error}')
