import requests

BASE_URL = "https://thebookshelf.pythonanywhere.com/"

def login_or_signup(username, password, l_or_s):
    if l_or_s == "l":
        l_or_s = "login"
    else:
        l_or_s = "signup"
    login_data = {"username": username, "password": password}
    response = requests.post(BASE_URL + l_or_s, json=login_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])
    if output['msg'] == f"welcome back, {username}":
        return True
    return False
    
l_or_s = input("Enter 'L' to login or 'S' to sign up:").lower().strip()

username = input("enter username: ")
password = input("enter password: ")

logged_in = login_or_signup(username, password, l_or_s)

if logged_in:
    borrower_or_lender = input("Do you want to be a borrower or lender?\nEnter 'b' for borrower or 'l' for lender: ")