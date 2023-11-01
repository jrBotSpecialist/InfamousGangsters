import re
from dupe import MultiSession

# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

def join_oc(multi_session):
    print(YELLOW + "Checking for oc invite.." + ENDC)
    # Step 1: Perform the initial GET request to extract the oc value
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin"
    }
    url = "https://infamousgangsters.com/site.php?page=oc"
    referrer = "https://infamousgangsters.com/site.php?page=igforum&forum=1"

    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
    response_list = multi_session.get(url, headers=headers)


    for response in response_list:
     if response.status_code == 200:

         # Extract the oc value from the response text
         text = response.text
         match = re.search(r'name="ocid" value="(\d+)"', text)
     if not match or len(match.groups()) < 1:
        print(RED + "No OC invite to accept!" + ENDC)
        return

    oc_value = match.group(1)

    # Step 2: Send a POST request with the extracted oc value
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    post_data = f"ocid={oc_value}&Submit=Accept"
    post_url = "https://infamousgangsters.com/site.php?page=oc"
    
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")

    post_response = multi_session.post(post_url, headers=headers, data=post_data)

    for response in response_list:
     if response.status_code == 200:

        # You can handle the POST response here if needed
        post_text = post_response.text
        print(GREEN + "Joined an OC" + ENDC)
