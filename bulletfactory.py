from bs4 import BeautifulSoup
import requests
from PIL import Image
import re
import pytesseract
import cv2
import numpy as np
from dupe import MultiSession
import json
import base64

# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

def make_request(multi_session):
    url = "https://infamousgangsters.com/site.php?page=bulletfactory"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "referrer": "https://infamousgangsters.com/site.php?page=users_online"
    }
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
    response_list = multi_session.get(url, headers=headers)

    for response in response_list:
     if response.status_code == 200:
        print(YELLOW + 'Navigated to bulletfactory page' + ENDC)
     else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def save_captcha_image(multi_session, image_file_path):
    url = "https://infamousgangsters.com/crimes-verify.php?bullets=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "image/avif,image/webp,*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "referrer": "https://infamousgangsters.com/site.php?page=bulletfactory"
    }
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
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

def make_bullet_factory_request(multi_session, ocr_result):
    url = "https://infamousgangsters.com/site.php?page=bulletfactory"

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
        "referrer": "https://infamousgangsters.com/site.php?page=bulletfactory"
    }

    # Replace 'DXZE8' with the actual OCR result
    body = f"buybullets=55&bulletcode={ocr_result}&give=Buy%21"
    multi_session = MultiSession("C:\\Users\\Student\\Desktop\\python-ig\\session_cookie.json")
    response_list = multi_session.post(url, headers=headers, data=body)

    for response in response_list:
     if response.status_code == 200:
        print(GREEN + 'You boughts 55 bullets!' + ENDC)

        # Your code to handle the extracted text goes here
     else:
        print(f"Failed to make bullet factory request. Status code: {response.status_code}")

def check_bullet_factory_and_buy_bullets(multi_session):
    url = "https://infamousgangsters.com/site.php?page=bulletfactory"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "referrer": "https://infamousgangsters.com/site.php?page=igforum&forum=1"
    }

    response_list = multi_session.get(url, headers=headers)

    for response in response_list:
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all text within the 'font' tag
            font_elements = soup.find_all('font', {'color': '#999999', 'size': '3'})
            
            for font_element in font_elements:
                # Search for the text containing the number
                match = re.search(r'It currently has (\d+) bullets', font_element.get_text())

                if match:
                    number = int(match.group(1))
                    print(f"Extracted number: {number}")
                    bullets = number
                    if bullets >= 55:
                        print("There are 55 or more bullets in the bullet factory.")
                        # Call make_bullet_factory_request with the OCR result (replace 'ocr_result' with the actual value)
                        result = solve('C:\\Users\\Student\\Desktop\\InfamousGangsters\\python-ig\\captcha.png')
                        ocr_result = result.get("result")
                        make_bullet_factory_request(multi_session, ocr_result)
                    else:
                        print("There are not enough bullets in the bullet factory.")
                else:
                    print("No numeric value found in the bullet text.")
        else:
            print(f"Failed to make the GET request. Status code: {response.status_code}")