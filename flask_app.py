from flask import Flask, request, jsonify, session
import json, pickle
from book import Book
from user import User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

USERS_IN_SERVER = []
BOOKS_IN_SERVER = {}

app = Flask(__name__)

# to enable user session management
login_manager = LoginManager()

app.secret_key = b'random7classical-entities'

login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id): # needed for flask-login session management
  # verify that username is not taken
  file = open('users.pkl','rb')
  users = pickle.load(file) # will be load a list of already existing User type objects
  file.close()

  for person in users:
    if person.username == user_id:
      return person

def save_user(user_obj):
  load_users_from_server()

  for indx in range(len(USERS_IN_SERVER)):
    person = USERS_IN_SERVER[indx]
    if person.username == user_obj.username:
      USERS_IN_SERVER.pop(indx)
      USERS_IN_SERVER.append(user_obj)
      return

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
  response = {"msg": "Hello bookworm!\n Enter (1) to Login or (2) to Sign Up and access the Bookshelf..."}
  # TODO: enable user to navigate to log in or sign up. If user is signed in, go directly to a book request page.
  return jsonify(response)


@app.route("/logout", methods=['POST'])
@login_required
def logout():
  # TODO: fill in
  logout_user()
  pass


@app.route("/login", methods=['POST'])
def login():
  data = json.loads(request.data)
  response = {'msg': ""} # the response given back to user

  username = data["username"]
  password = data["password"]

  load_users_from_server()

  for person in USERS_IN_SERVER:
    if person.username == username:
      if person.login_check_password(password):
        if login_user(person):
            response['msg'] = f"welcome back, {current_user.username}"
            response["session"] = str(session)
            return jsonify(response)
        else:
            response['msg'] = "login failed"
            return jsonify(response)
      else:
        response['msg'] = "wrong password"
        return jsonify(response)

  response['msg'] = "no such user"
  return jsonify(response)

@app.route("/signup", methods=['POST'])
def signup():
  '''
  this function gets the request data from a client. The json request should contain a username and password.
  The function opens a pkl (pickled) file which is where we are storing already created users,
  checks if no other user has the same username then creates a user object and adds it to our users in the pkl file.
  '''
  response = {'msg': ""} # the response given back to user

  data = json.loads(request.data)
  username = data["username"]
  password = data["password"]

  # verify that username is not taken
  load_users_from_server()

  for person in USERS_IN_SERVER:
    if person.username == username:
      response['msg'] = "username taken, choose another one"
      return jsonify(response)

  # todo: verify password appropriate complexity and neither username nor password is empty string
  complex_password = password_validity(password)
  if complex_password != 'pass':
    response['msg'] = complex_password
    return jsonify(response)

  new_user = User(username, password)
  USERS_IN_SERVER.append(new_user)
  # Open a file to write bytes
  p_file = open('users.pkl', 'wb')
  # Pickle the list
  pickle.dump(USERS_IN_SERVER, p_file)
  p_file.close()
  if login_user(person):
    response['msg'] = f"welcome back, {current_user.username}"
    return jsonify(response)
  else:
    response['msg'] = "login failed"
    return jsonify(response)

# @login_required
# login required does not work because session data is not stored, so the user is essentially not logged in.
@app.route("/my_books", methods=['GET','POST'])
def my_books(): #NOT TESTED
  '''
  input json: contains "option" -> "view", "add", "delete","delete all" are only valid inputs
  contains "username" with username of who sent request
  if option is "delete" or "add": input json contains "titles" - a list of titles to be deleted or added
  '''
  response = {'msg': ""} #response given back to the client

  data = json.loads(request.data)
  option = data['option']
  username = data['username']
  person = load_user(username)

  if option not in ["view", "add", "delete","delete all"]:
    response['msg'] = "invalid option"
    return response

  if option == "view":
    if person.books_in_possession == None:
      response['msg'] = "None"
    else:
      book_titles = [item.title for item in person.books_in_possession]
      response['msg'] = book_titles

  if option == "delete":
    load_books_from_server()
    titles = data['titles']

    for title in titles:
      title_lower = title.lower()
      person.delete_book(title)
      if title_lower in BOOKS_IN_SERVER:
        indx = 0 # will be used as index in case user has more than one book with same title
        for x in range(len(BOOKS_IN_SERVER[title_lower])):
          if BOOKS_IN_SERVER[title_lower][indx][0] == person.username:
            BOOKS_IN_SERVER[title_lower].pop(indx)
            indx -= 1
          indx += 1
        if BOOKS_IN_SERVER[title_lower] == []:
          BOOKS_IN_SERVER.pop(title_lower)

    save_user(person)
    save_users_to_server()
    save_books_to_server()
    person = load_user(person.username)
    if person.books_in_possession == None:
      response['msg'] = "your updated books:" + str(person.books_in_possession)
    else:
      response['msg'] = "your updated books:" + str([x.title for x in person.books_in_possession])


  if option == "add":
    load_books_from_server()

    titles = data['titles']
    for title in titles:
      title_lower = title.lower()
      person.add_book(Book(title, person.username))
      if title_lower in BOOKS_IN_SERVER:
        BOOKS_IN_SERVER[title_lower].append((person.username, True))
      else:
        BOOKS_IN_SERVER[title_lower] = [(person.username, True)]
    save_user(person)
    save_users_to_server()
    save_books_to_server()
    person = load_user(person.username)
    response['msg'] = "your updated books:" + str([x.title for x in person.books_in_possession])

  if option == "delete all":
    if person.books_in_possession == None:
      response['msg'] = "your updated books: 'None'"
      return jsonify(response)
    for item in person.books_in_possession:
      title = item.title
      title_lower = title.lower()
      if title_lower in BOOKS_IN_SERVER:
        indx = 0 # will be used as index in case user has more than one book with same title
        for x in range(len(BOOKS_IN_SERVER[title_lower])):
          if BOOKS_IN_SERVER[title_lower][indx][0] == person.username:
            BOOKS_IN_SERVER[title_lower].pop(indx)
            indx -= 1
          if BOOKS_IN_SERVER[title_lower] == []:
            BOOKS_IN_SERVER.pop(title_lower)
          indx += 1
    save_books_to_server()
    person.books_in_possession = None
    save_user(person)
    save_users_to_server()
    person = load_user(person.username)
    response['msg'] = "your updated books:" + str(person.books_in_possession)

  return jsonify(response)

@app.route("/book_request", methods=['GET']) 
def bookrequest(): 
  response = {'msg': ""} #response given back to the client

  # for testing purposes
  load_books_from_server()
  response['books_in_server'] = str(BOOKS_IN_SERVER)


  data = json.loads(request.data)

  #check if user provided a book title to check and returns a detailed error message if not.
  if "book title" not in data:
    response['msg'] = "Please provide a book title. Remember to make the key of the dictionary 'book title"
    return jsonify(response)

  #check if book requested is in the bookshelf and let the user know if we have the book or not.
  book_title = data['book title'].lower()
  if book_title in BOOKS_IN_SERVER:
    users = []
    response['msg'] = f'''
    Your requested book {book_title} has been found on the bookshelf!
    Here is a list of all the users that own the book.
    If the book is currently available for borrowing from that user,
    we put a true beside their name.
    {BOOKS_IN_SERVER[book_title]}
    '''


  else:
    response['msg'] = "sorry we do not have your requested book."
  return jsonify(response)

@app.route("/borrow_request", methods=['GET']) 
def borrow_request():
  response = {'msg': ""}

  data = json.loads(request.data)

'''
  When the chat rooms are set up, here i would call the method to connect the two users.

  Perhaps have something here that calls the my_request method passing in the username of the user requested. 
  This sends a borrow request to the requested where they can accept or decline the request.
  With this method, I wont need to have my_reuest checking periodically for a new request.
  Because when a request is sent, the method will be called immediately and the request sent.
'''

@app.route("/my_request", methods=['GET']) 
def my_request():

  pass

def save_books_to_server():
  '''
  reusable function that saves the books dictionary type in books_in_server global variable to the books.pkl file on server
  '''
  p_file = open('books.pkl', 'wb')
  pickle.dump(BOOKS_IN_SERVER, p_file)
  p_file.close()

def load_books_from_server():
  '''
  reusable function that loads the books in the books.pkl file to books_in_server global variable as a dictionary type
  '''
  global BOOKS_IN_SERVER

  file = open('books.pkl','rb')
  BOOKS_IN_SERVER = pickle.load(file) # will be load a list of already existing User type objects
  file.close()

def save_users_to_server():
  '''
  reusable function that saves the user objects in users global variable to the users.pkl file on server
  '''
  # Open a file to write bytes
  p_file = open('users.pkl', 'wb')
  # Pickle the list
  print(USERS_IN_SERVER)
  pickle.dump(USERS_IN_SERVER, p_file)
  p_file.close()

def load_users_from_server():
  '''
  reusable function that loads a list of user objects to users global variable from the users.pkl file on server
  '''
  global USERS_IN_SERVER
  file = open('users.pkl','rb')
  USERS_IN_SERVER = pickle.load(file) # will be load a list of already existing User type objects
  print(USERS_IN_SERVER)
  file.close()

def password_validity(password):
  repsonse_message = ""
  l, u, p, d = 0, 0, 0, 0
  if (len(password) >= 8):
    for i in password:
      # counting lowercase alphabets
      if (i.islower()):
        l+=1
      # counting uppercase alphabets
      if (i.isupper()):
        u+=1

      # counting digits
      if (i.isdigit()):
        d+=1

      # counting the mentioned special characters
      if(i=='@'or i=='$' or i=='_'):
        p+=1

    if l<1:
      response_message = 'Your password needs at least 1 lowercase alphabet'
    elif u<1:
      response_message = 'Your password needs at least 1 uppercase alphabet'
    elif d<1:
      response_message = 'Your password needs at least 1 digit'
    elif p<1:
      response_message = 'Your password needs at least 1 of these special characters: "@$_"'
  else:
    response_message = "Your password needs to be at lest 8 characters long"
  if l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password):
    response_message = 'pass'
  return response_message

