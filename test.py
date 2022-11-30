import requests

user_name = 'Elei'
password = "ComplexPassword@2022"
book_owned = 'Food Recipe'

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
book_search_data = {"book title": "Pachinko"}
response = requests.get(BASE_URL + "book_search", json=book_search_data)
print(response)
print(response.json())

#test response if requested book is not in server
book_search_data = {"book title": "Little Women"}
response = requests.get(BASE_URL + "book_search", json=book_search_data)
print(response)
print(response.json())

#test response if user doesn't put 'book title' in the input dictionary
book_search_data = {"book": "trial"}
response = requests.get(BASE_URL + "book_search", json=book_search_data)
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

#test lender granting book request
grant_book_search_data = {
  "lender username" : user_name,
  "book" : 'Food Recipes',
  "borrower username" : 'mimmiso',
  "decision" : False 
  } 
response = requests.get(BASE_URL + "grant_book_search", json=grant_book_search_data)
print(response)
print(response.json())

# test user viewing all their chats
my_chats_data = {"username": user_name, "option": "view chats"}
response = requests.get(BASE_URL + "my_chats", json=my_chats_data)
print(response)
print(response.json())

# test user viewing chat message in specific chat
my_chats_data = {"username": user_name, "option": "view messages", "with": "Sashe"}
response = requests.get(BASE_URL + "my_chats", json=my_chats_data)
print(response)
print(response.json())

# test user sending chat message to other user
my_chats_data = {"username": user_name, "option": "send messages", "with": "Sashe", "message": "Sure, do you live around DC? We can meet up at a cafe to exchange books ;)"}
response = requests.get(BASE_URL + "my_chats", json=my_chats_data)
print(response)
print(response.json())