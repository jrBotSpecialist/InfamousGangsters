from bs4 import BeautifulSoup
import requests
from dupe import MultiSession

# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

def gta_post_request(multi_session):
    print(YELLOW + "Getting GTA page" + ENDC)
    # Your GTA POST request URL
    gta_url = "https://infamousgangsters.com/site.php?page=gta"
    
    # Define the GTA POST data
    gta_data = {
        'e43fd': 'Steal a car!',
    }
    
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
        multi_session = MultiSession("session_cookie.json")

        # Make the GTA POST request with the session and data
        gta_response_list = multi_session.post(gta_url, data=gta_data, headers=headers)
        
        # Handle the response as needed
        for response in gta_response_list:
          if response.status_code == 200:
            
            # Extract and filter text from the response
            gta_response_text = response.text

            # Parse the HTML response
            gta_html = BeautifulSoup(gta_response_text, 'html.parser')

            # Find the message element
            gta_message_element = gta_html.find('td', class_='bodymain')
            
            if gta_message_element:
                gta_message_element = gta_message_element.find('div', align='center')
                if gta_message_element:
                    gta_full_message = gta_message_element.get_text()
                    gta_stolen_message = next((line for line in gta_full_message.split('\n') if line.startswith('You stole a')), None)
                    if gta_stolen_message:
                        print(GREEN + gta_stolen_message + ENDC)
                    else:
                        print(RED + "You are in jail or the timer has not completed." + ENDC)
                else:
                    print("Message element not found inside 'td' with class 'bodymain'.")
            else:
                print("Message element not found. You are most likely in Jail.")
          else:
            print(f"GTA POST request failed with status code {response.status_code}")
    except Exception as error:
        print(f"An error occurred while processing the GTA request: {error}")
