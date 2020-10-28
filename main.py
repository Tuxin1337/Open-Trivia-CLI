import requests
import json


#### URLS ####
get_token_url = 'https://opentdb.com/api_token.php?command=request'
base_url = 'https://opentdb.com/api.php?'
lookup_categorys_url = 'https://opentdb.com/api_category.php'
#### VARS ####
amount = 10
run = True
logo = '''
   ____                     _______   _       _          _____ _      _____ 
  / __ \                   |__   __| (_)     (_)        / ____| |    |_   _|
 | |  | |_ __   ___ _ __      | |_ __ ___   ___  __ _  | |    | |      | |  
 | |  | | '_ \ / _ \ '_ \     | | '__| \ \ / / |/ _` | | |    | |      | |  
 | |__| | |_) |  __/ | | |    | | |  | |\ V /| | (_| | | |____| |____ _| |_ 
  \____/| .__/ \___|_| |_|    |_|_|  |_| \_/ |_|\__,_|  \_____|______|_____|
        | |                                                                 
        |_|                                                                 '''
version = "0.1"

def intro():
    print(logo)
    print()
    print('Hello and welcome to Open Trivia CLI')
    print('Write "help" to get a quick help')

def make_request(url):
    r = requests.get(url) 
    if r.status_code > 301:
        print(f"Error: Status code: {r.status_code}")
    else:
        return r

def get_token(url):
    r = make_request(url)
    return r.json()['token']

def get_questions(**kwargs):
    url = base_url + f"amount={amount}&token={token}" # Create URL with amount and token
    for key, value in kwargs.items(): # Add custom properties
        url = url + f"&{key}={value}"
    r = make_request(url) #Make request

    return r.json()

def print_categorys(): # Print all available categorys
    categorys = make_request(lookup_categorys_url)
    for category in categorys.json()['trivia_categories']:
        print(f"{category['name']} | {category['id']}, ")

def user_input_handler(user_input):
    user_input = user_input.lower()
    if user_input == '?':
        print_categorys()
    elif user_input in ['v', 'version']:
        print(f"Version: {version}")
    else:
        print("Help:")
        print('     Write "?" to get a list of categorys')
        print('     Write "q" to exit the programm')
        print('     Write "v" to get the version')

token = get_token(get_token_url)


# Main loop
intro()
while run:
    user_input = input('>> ')
    if user_input.lower() in ['q','exit']:
        break
    user_input_handler(user_input)
