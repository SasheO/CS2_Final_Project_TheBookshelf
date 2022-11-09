# issues: signed up users don't get saved in server but helper function for that works fine

import requests
user_name = 'elei'
password = "CompledPassword5@"
# password = "Testuser4"

BASE_URL = "https://thebookshelf.pythonanywhere.com/"

signup_data = {"username": user_name, "password": password}
response = requests.post(BASE_URL + "signup", json=signup_data)
# response = requests.get(BASE_URL)
print(response.json())