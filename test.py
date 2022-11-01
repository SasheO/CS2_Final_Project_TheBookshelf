import requests
user_name = 'testuser3'
password = "testuser3"

BASE_URL = "https://thebookshelf.pythonanywhere.com"

signup_data = {"username": user_name, "password": password}
response = requests.post(BASE_URL + "/signup", json=signup_data)
print(response.json())