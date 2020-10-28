import requests
import json


#### URLS #####
get_token_url = 'https://opentdb.com/api_token.php?command=request'

def get_token(url):
    r = requests.get(url) 
    if r.status_code > 301:
        print(f"Error: Status code: {r.status_code}")
    elif r.json()['response_code'] != 0:
        print(f"Error: Response code: {r.json()['response_code']}")
    else:
        return r.json()['token']

token = get_token(get_token_url)
