import requests

user_name = 'msmmiso'
password = "CompledPassword5@"
# password = "Testuser4"

BASE_URL = "https://thebookshelf.pythonanywhere.com/"

signup_data = {"username": user_name, "password": password}
response = requests.post(BASE_URL + "login", json=signup_data)
# response = requests.get(BASE_URL)
print(response)
print(response.json())

my_books_data = {
  "option": "view",
  "username": user_name,
  "titles": ["Pachinko", "Against the Loveless World"]
}
response = requests.post(BASE_URL + "my_books", json=my_books_data)
print(response)
print(response.json())