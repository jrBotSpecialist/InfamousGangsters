from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import time
import schedule
import threading  # Import the threading module
from GTA import gta_post_request
from melt import fetch_melt
from crimes import fetch_crimes
import bulletfactory  # Import your custom module
from deadusers import check_stats
from oc import join_oc
import join
import traceback
import json
import requests
import ibank
from dupe import MultiSession
import money
import sell_cars
from kill import euo, sfm
import argparse

# ANSI escape codes for text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
ENDC = "\033[0m"

# Your session cookies
session_cookie_file = "session_cookie.json"

# Create an instance of MultiSession and load the sessions from the JSON file
multi_session = MultiSession(session_cookie_file)

# Check if sessions were loaded successfully
if multi_session:
    print(GREEN + 'Bot is setting up and will start in 7 seconds.' + ENDC)

# Variable to store the OCR result
ocr_result = None

multi_session = MultiSession("session_cookie.json")

def bank():
    ibank.ibank(multi_session)

# Define functions for each task
def run_crimes():
    try:
        fetch_crimes(multi_session)
    except Exception as error:
        print(f"An error occurred in the Crimes function: {error}")

def run_gta():
    try:
        gta_post_request(multi_session)
    except Exception as error:
        print(f"An error occurred in the GTA function: {error}")

def run_melt():
    try:
        fetch_melt(multi_session)
    except Exception as error:
        print(f"An error occurred in the Melt function: {error}")

def run_stats():
    try:
        join_oc(multi_session)
    except Exception as error:
        print(f"An error occurred in the Stats function: {error}")

def clearNleave():
    try:
        join.clearinbox(multi_session, "https://infamousgangsters.com/site.php?page=inbox")
    except Exception as error:
        print(f"An error occurred in the clearNleave function: {error}")

# Function to join crew ocs
def crewoc():
    try:
        # Call functions from the 'join' module and pass the 'session' where needed
        topic_urls = join.getforum(multi_session)
        print(topic_urls)
        base_url = "https://infamousgangsters.com/"
        for url in topic_urls:
            profile_link = join.topic(multi_session, url)
            if profile_link:
                crew_name, user_name, crew_id = join.profile(multi_session, profile_link)
                if crew_id:
                    join.apply(multi_session, crew_id, crew_name, user_name)  # Pass crew_id and user_name
                else:
                    print(RED + f'Failed to get crew_id for {crew_name}' + ENDC)
            else:
                print(f'Failed to get crew_name for {profile_link}')
        else:
            print(f'Failed to get profile_link for {url}')
    except Exception as e:
        # Print the traceback if any unexpected error occurs
        print(RED + 'An error occurred during crewoc() preparing traceback' + ENDC)
        traceback.print_exc()

def qt():
    try:
        smoney_value = money.sellpointsvalue(multi_session)
        bmoney_value = money.buypointsvalue(multi_session)

        if smoney_value and bmoney_value:
            money.sellpoints(multi_session, smoney_value)
            money.buypoints(multi_session, bmoney_value)
        else:
            if not smoney_value:
                print("No value for smoney_value.")
            if not bmoney_value:
                print("No value for bmoney_value.")

    except Exception as e:
        traceback.print_exc()

def run_bullet_factory():
    try:
       # Create instances of MultiSession for session 1 and session 2
       multi_session_1 = MultiSession("session_cookie.json")

       # Use the appropriate multi_session instance for each task
       bulletfactory.make_request(multi_session_1)
       bulletfactory.save_captcha_image(multi_session_1, "captcha.png")
       bulletfactory.check_bullet_factory_and_buy_bullets(multi_session_1)
    except Exception as error:
        print(f"An error occurred in the Bullet Factory function: {error}")

def online():
    try:
        euo(multi_session)
    except Exception as error:
        print("An error occurred during online extraction function: ", error)

def search():
    try:
        # Get list of usernames 
        with open('search_list.txt') as f:
         usernames = f.read().splitlines()

        sfm(multi_session, usernames)
    except Exception as error:
        print("An error occurred during search function: ", error)

parser = argparse.ArgumentParser()

parser.add_argument('--crewoc', action='store_true', help='Applys to CrewOCs & Leave after')
parser.add_argument('--crimes', action='store_true', help='Does Crimes')  
parser.add_argument('--bf', action='store_true', help='Buys Bullets')
parser.add_argument('--qt', action='store_true', help='Quicktrading')
parser.add_argument('--oc', action='store_true', help='Accepts OC Invites')
parser.add_argument('--gta', action='store_true', help='Does GTA')
parser.add_argument('--melt', action='store_true', help='Melts last car (Page: 1)')
parser.add_argument('--bank', action='store_true', help='53.4 bill in interest bank')
parser.add_argument('--online', action='store_true', help='Get users online list')
parser.add_argument('--search', action='store_true', help='Search from search_list.text')


args = parser.parse_args() 



# Create a ThreadPoolExecutor with 8 workers to run the functions in parallel
with ThreadPoolExecutor(max_workers=16) as executor:

    # Schedule the functions using the `schedule` library
    if args.crimes:
        schedule.every(11).seconds.do(lambda: executor.submit(run_crimes))
        run_crimes()

    if args.bf:
        schedule.every(20).seconds.do(lambda: executor.submit(run_bullet_factory))

    if args.crewoc:
       schedule.every(30).seconds.do(lambda: executor.submit(crewoc))
       schedule.every(7).seconds.do(lambda: executor.submit(clearNleave))

    if args.qt:
        schedule.every(40).seconds.do(lambda: executor.submit(qt))

    if args.oc:
        schedule.every(35).seconds.do(lambda: executor.submit(run_stats))

    if args.gta:
        schedule.every(301).seconds.do(lambda: executor.submit(run_gta))
        run_gta()

    if args.melt:
        schedule.every(451).seconds.do(lambda: executor.submit(run_melt))
        run_melt()

    if args.bank:
        schedule.every(1).hour.do(lambda: executor.submit(bank))
        bank()

    if args.online:
        print(GREEN + "Grabbing list of online users" + ENDC)
        online()

    if args.search:
        print(GREEN + "Searching users list" + ENDC)
        search()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print(RED + "Bot stopped by the user (Ctrl+C)" + ENDC)
    except Exception as error:
        print(f"An error occurred: {error}")

