import requests
from bs4 import BeautifulSoup
from dupe import MultiSession

def pre_search(multi_session):
    try:
        # Step 1: Send a GET request to get usernames
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        }

        usernames_url = "https://infamousgangsters.com/site.php?page=users_online"
        multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
        usernames_response_list = multi_session.get(usernames_url, headers=headers)
        usernames_html = usernames_response_list.text

        username_count = 0
        usernames = []

        # Parse HTML to extract usernames
        usernames_soup = BeautifulSoup(usernames_html, 'html.parser')
        username_elements = usernames_soup.select('a[href^="site.php?page=viewprofile&user="]')

        for element in username_elements:
            # Increment the count
            username_count += 1

            # Check if the count reaches 51
            if username_count == 51:
                break  # This will stop the preSearch function

            usernames.append(element.get_text().strip())

        # Sort the usernames alphabetically
        usernames.sort()
    except Exception as e:
        print(f"An error occurred: {e}")

def pre_search():
    try:
        # Step 1: Send a GET request to get usernames
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        }

        usernames_url = "https://infamousgangsters.com/site.php?page=users_online"
        usernames_response = multi_session.get(usernames_url, headers=headers)
        usernames_html = usernames_response.text

        username_count = 0
        usernames = []

        # Parse HTML to extract usernames
        usernames_soup = BeautifulSoup(usernames_html, 'html.parser')
        username_elements = usernames_soup.select('a[href^="site.php?page=viewprofile&user="]')

        for element in username_elements:
            # Increment the count
            username_count += 1

            # Check if the count reaches 51
            if username_count == 51:
                break  # This will stop the preSearch function

            usernames.append(element.get_text().strip())

        # Sort the usernames alphabetically
        usernames.sort()

        # Step 3: Send a GET request to get the post secret
        post_secret_url = "https://infamousgangsters.com/site.php?page=kill"
        post_secret_response = requests.get(post_secret_url, headers=headers)
        post_secret_html = post_secret_response.text

        # Step 4: Extract the post secret
        post_secret_input = BeautifulSoup(post_secret_html, 'html.parser').find('input', {"name": "postsecret"})
        post_secret = post_secret_input['value'] if post_secret_input else ''

        # Step 5: Iterate through usernames and send POST requests
        for username in usernames:
            post_url = "https://infamousgangsters.com/site.php?page=kill"
            post_data = {
                "postsecret": post_secret,
                "GwJidNQv7WRbDHYiuYws4fcCHP3TofHlRG+HfPgC=": "",
                "HQI039Qv7WQA6P0Mlk2TTmcklomxpRdUVntQptf9=": "",
                "HgKAU9Qv7WRw5SVlRKy+0omYNpyyi10yQybGtkOS": username,
                "IAIKY9Qv7WRzsoTqeUS2EFSiXDv5FwBdx4oCGw5Z": "",
                "IgKeVdQv7WToYiCmuL7XKr6bP43KbuzaxmMmkoJR": "",
                "IwJ+BENQv7WSbZgZ41z8+9pb8FeFjV8lro8fWQj3": "",
                "JAL9WNQv7WTwfKwgUVOOTGuS/VxgLEoCjUV6Atjt": "",
                "JgIoYtQv7WS9QVNg9proIfd/1PEN8SPsp5FNZ7km": "",
                "JwLiNtQv7WS6FAPdLRzD2gKQmVfVDJhhEk/jvXLC=": "",
                "KAJ/WdQv7WRgmq4Ok/9Mqk4MkOY68oOYAntFAZsT": "23",
                "KgK9zNQv7WT1YtUXMofqRMZ+ak4zE9dNor5TYcYD": "",
                "KwIdqtQv7WTIXUdhn75ZQYiPP30CIMj5tinsDTuA": "",
                "LQITMNQv7WQJJeL9JB2YVbl2gcAgoOkMwMBkSQHJ": "",
                "LgL8iNQv7WRs3Go1BE/o7KQR2piGg5Hi61gDQQOI": "",
                "submit": "Search!"
            }
            post_response_list = multi_session.post(post_url, data=post_data, headers=headers)

            # Process the result of each POST request if needed
            print(f"Searching {username}..")

    except Exception as error:
        print("Error:", error)