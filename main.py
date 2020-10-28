import requests
import json


#### URLS ####
get_token_url = 'https://opentdb.com/api_token.php?command=request'
base_url = 'https://opentdb.com/api.php?'
lookup_categorys_url = 'https://opentdb.com/api_category.php'
#### VARS ####
token = ""
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
    global token
    if token == "": #check if token exits
        token = get_token(get_token_url)

    url = base_url + f"amount={amount}&token={token}" # Create URL with amount and token
    for key, value in kwargs.items(): # Add custom properties
        url = url + f"&{key}={value}"
    r = make_request(url) #Make request
    print(r.json())
    return r.json()

def print_categorys(): # Print all available categorys
    categorys = make_request(lookup_categorys_url)
    for category in categorys.json()['trivia_categories']:
        print(f"{category['name']} | {category['id']}, ")

def ask_questions():
    print("How many questions do you want to get asked? (Default: 10)")
    amount = input(">> ")
    print("In which category do you want to get asked? (Default: all)")
    category = input(">> ")
    print("Which type of questions do you want to get asked? (boolean, multiple, Default: multiple)")
    question_type = input(">> ")

    run = True

    if amount == "":
        amount = 10
    try:
        amount = int(amount)
    except:
        print('Pls specify an integer for ammount')
    if amount < 0 or amount > 50: 
        print('Pls specify amount btw. 1 to 50')
        run = False
    if category is not "":
        try:
            category = int(category)
        except:
            print('Pls specify an integer for category (check: "?")')
            run = False
    if question_type == "":
        question_type = 'multiple'
    else:
        question_type = question_type.lower()
    if question_type not in ['boolean', 'multiple']:
        print('Use "boolean" or "multiple" for question type')
        run = False

    if run:
        get_questions(amount=amount, type=question_type, category=category)

def user_input_handler(user_input):
    user_input = user_input.lower()
    if user_input == '?':
        print_categorys()
    elif user_input in ['v', 'version']:
        print(f"Version: {version}")
    elif user_input in ['q', 'exit', 'quit']:
        print("Bye!")
    elif user_input in ['new', 'n']:
        ask_questions()
    else:
        print("Help:")
        print('     Write "?" to get a list of categorys')
        print('     Write "q" to exit the programm')
        print('     Write "v" to get the version')



# Main loop
intro()
while run:
    user_input = input('>> ')
    if user_input.lower() in ['q','exit', 'quit']:
        run = False
    user_input_handler(user_input)
