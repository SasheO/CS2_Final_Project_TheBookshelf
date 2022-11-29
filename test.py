import requests

user_name = 'msmmiso'
password = "CompledPassword5@"
book_owned = 'Food Recipes'
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

#test response if requested book is in server
book_request_data = {"book title": "Pachinko"}
response = requests.get(BASE_URL + "book_request", json=book_request_data)
print(response)
print(response.json())

#test response if requested book is not in server
book_request_data = {"book title": "Little Women"}
response = requests.get(BASE_URL + "book_request", json=book_request_data)
print(response)
print(response.json())

#test response if user doesn't put 'book title' in the input dictionary
book_request_data = {"book": "trial"}
response = requests.get(BASE_URL + "book_request", json=book_request_data)
print(response)
print(response.json())

#test borrower making borrow request
borrow_request_data = {"lender username" : user_name,
    "book" : 'Food Recipes',
    "borrower username" : 'mimmiso' }
response = requests.get(BASE_URL + "borrow_request", json=borrow_request_data)
print(response)
print(response.json())

#test lender viewing all their book requests
view_my_requests_data = {"lender username" : user_name}
response = requests.get(BASE_URL + "view_my_requests", json=view_my_requests_data)
print(response)
print(response.json())