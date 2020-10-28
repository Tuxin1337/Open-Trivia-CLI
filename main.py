import requests
import json


#### URLS ####
get_token_url = 'https://opentdb.com/api_token.php?command=request'
base_url = 'https://opentdb.com/api.php?'
lookup_categorys_url = 'https://opentdb.com/api_category.php'
lookup_category_url = 'https://opentdb.com/api_count.php?category='
#### VARS ####
token = ""
amount = 10
global run
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
    run = True
    global token
    if token == "": # Check if token exits
        token = get_token(get_token_url) # Get new token

    # check if category is available
    categorys_url = f"{lookup_category_url}{kwargs['category']}"
    categorys = make_request(categorys_url)
    try:
        categorys.json()
    except:
        if kwargs['category'] != "":
            run = False
    if run:
        url = base_url + f"amount={amount}&token={token}" # Create URL with amount and token
        for key, value in kwargs.items(): # Add custom properties
            url = url + f"&{key}={value}"
        r = make_request(url) #Make request
        return r.json()
    else:
        print('Category ID is not available, please check "?" for IDs')

def ask_questions(questions):
    for question in questions['results']:
       print(question) 


def print_categorys(): # Print all available categorys
    categorys = make_request(lookup_categorys_url)
    for category in categorys.json()['trivia_categories']:
        print(f"{category['name']} | {category['id']}, ")

def new_questions():
    run = True
    # How many questions
    print("How many questions do you want to get asked? (Default: 10)")
    amount = input(">> ")
    if amount == "":
        amount = 10
    try:
        amount = int(amount)
    except:
        print('Pls specify an integer for ammount')
    if amount < 1 or amount > 50: 
        print('Pls specify amount between 1 to 50')
        run = False


    # Which category
    if run:
        print("In which category do you want to get asked? (Default: all)")
        category = input(">> ")
        if category != "":
            try:
                category = int(category)
            except:
                print('Pls specify an integer for category (check: "?")')
                run = False
    
    
    # Which type
    if run:
        print("Which type of questions do you want to get asked? (boolean, multiple, Default: multiple)")
        question_type = input(">> ")
        if question_type != "":
            question_type = question_type.lower()
            if question_type not in ['boolean', 'multiple']:
                print('Use "boolean" or "multiple" for question type')
                run = False
    
    
    # Which difficulty 
    if run:
        print("Which difficulty should the questions are? (easy, medium, hard, Default: Random)")
        difficulty = input(">> ")
        if difficulty != "":
            difficulty = difficulty.lower()
            if difficulty not in ['easy', 'medium', 'hard']:
                print('Please choice a "easy", "medium" or "hard"')
    



    if run:
        questions = get_questions(amount=amount, type=question_type, category=category, difficulty=difficulty)
        if questions != None:
            ask_questions(questions)
        else:
            print('Send N to retry')
    else:
        print('Send N to retry')

def user_input_handler(user_input):
    user_input = user_input.lower()
    if user_input == '?':
        print_categorys()
    elif user_input in ['v', 'version']:
        print(f"Version: {version}")
    elif user_input in ['q', 'exit', 'quit']:
        print("Bye!")
    elif user_input in ['new', 'n']:
        new_questions()
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
