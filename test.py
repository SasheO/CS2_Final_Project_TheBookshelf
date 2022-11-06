import requests
user_name = 'testuser4'
password = "Testuser4@"
# password = "Testuser4"

BASE_URL = "https://thebookshelf.pythonanywhere.com"

signup_data = {"username": user_name, "password": password}
response = requests.post(BASE_URL + "/login", json=signup_data)
print(response.json())