import requests

BASE_URL = "https://thebookshelf.pythonanywhere.com/"

def login(username, password):
    login_data = {"username": username, "password": password}
    response = requests.post(BASE_URL + "login", json=login_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])
    if output['msg'] == f"welcome back, {username}":
        return True
    return False
    

def signup(username, password):
    signup_data = {"username": username, "password": password}
    response = requests.post(BASE_URL + "signup", json=signup_data)
    if response.status_code != 200:
        print(f"Error encountered logging in. Error code: {response.status_code}")
        return
    output = response.json()
    print(output['msg'])
    if output['msg'] == f"welcome back, {username}":
        return True
    return False


login_or_signup = input("Enter 'L' to login or 'S' to sign up:").lower().strip()

username = input("enter username: ")
password = input("enter password: ")