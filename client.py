import requests

BASE_URL = "https://thebookshelf.pythonanywhere.com/"

login_or_signup = input("Enter 'L' to login or 'S' to sign up:").lower().strip()

username = input("enter username: ")
password = input("enter password: ")

def login(username, password):
    login_data = {"username": username, "password": password}
    response = requests.post(BASE_URL + "login", json=login_data)
    # response = requests.get(BASE_URL)
    print(response)
    print(response.json())