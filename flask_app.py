from flask import Flask, request, jsonify, session
import json, pickle
from book import Book
from user import User
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

users = []

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
  file = open('users.pkl','rb')
  users = pickle.load(file) # will be load a list of already existing User type objects
  file.close()
  
  for indx in len(users):
    person = users[indx]
    if person.username == user_obj.username:
      users.pop(indx)
      users.insert(user_obj)
  pass

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
  response = {"msg": "Hello bookworm!\n Enter (1) to Login or (2) to Sign Up and access the Bookshelf..."}
  # TODO: enable user to navigate to log in or sign up. If user is signed in, go directly to a book request page.
  return jsonify(response)

@app.route("/booksearch", methods=['GET'])
@login_required
def booksearch(book_title):
  pass

@app.route("/logout", methods=['POST'])
@login_required
def logout():
  logout_user()
  pass

@app.route("/login", methods=['POST'])
def login():
  data = json.loads(request.data)
  response = {'msg': ""} # the response given back to user

  username = data["username"]
  password = data["password"]

  file = open('users.pkl','rb')
  users = pickle.load(file) # will be load a list of already existing User type objects
  file.close()
  
  for person in users:
    if person.username == username:
      if person.login_check_password(password):
        login_user(person)
        response['msg'] = f"welcome back, {current_user.username}"
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
  file = open('users.pkl','rb')
  users = pickle.load(file) # will be load a list of already existing User type objects
  file.close()
  
  for person in users:
    if person.username == username:
      response['msg'] = "username taken, choose another one"
      return jsonify(response)
  
  # todo: verify that username isnt and empty string
  # verify password appropriate complexity
  complex_password = password_validity(password)
  if complex_password == False:
    response['msg'] = "Your password is not complex enough"
    return jsonify(response)

  new_user = User(username, password)
  users.append(new_user)
  # Open a file to write bytes
  p_file = open('users.pkl', 'wb')
  # Pickle the list
  pickle.dump(users, p_file)
  p_file.close()
  login_user(new_user)
  response['msg'] = f"welcome to the Bookshelf {current_user}"
  return jsonify(response)

@app.route("/my_books", methods=['GET','POST'])
@login_required
def my_books():
  '''
  input json: contains "option" -> "view", "add", "delete","delete all" are only valid inputs
  if option is "delete" or "add": input json contains "titles" - a list of titles to be deleted or added
  '''
  response = {'msg': ""} #response given back to the client

  data = json.loads(request.data)
  option = data['option']
  if option not in ["view", "add", "delete","delete all"]:
    response['msg'] = "invalid option"
    return response
  me = load_user(current_user.username)

  if option == "view":
    book_titles = [item.title for item in me.books_in_possession]
    response['msg'] = book_titles
  
  if option == "delete":
    # TODO: fill in here
    titles = data['titles']
    for title in titles:
      me.delete_book(title)
    save_user(me)
    response['msg'] = "your updated books:" + str(me.books_in_possession)
  
  if option == "add":
    # TODO: fill in here
    titles = data['titles']
    for title in titles:
      me.add_book(Book(title))
    save_user(me)
    response['msg'] = "your updated books:" + str(me.books_in_possession)
  
  if option == "delete all":
    me.books_in_possession = None
    save_user(me)
    response['msg'] = "your updated books:" + str(me.books_in_possession)
    
  return jsonify(response)

@app.route("/bookrequest", methods=['GET']) #why is this a post and not a get --> I changed it to a get, you're right
def bookrequest(): ## NOT TESTED
  response = {'msg': ""} #response given back to the client

  data = json.loads(request.data)

  '''
  COMMENTED this out because it will probably cause an error
  #check if user provided a book title to check 
  if "book title" not in data:
    response['msg'] = "Please provide a book title"
  '''
  #check if book requested is in the bookshelf and let the user know if we have the book or not.
  file = open('books.pkl','rb') # Why are we opening in rb and not r? is it a pkl thing?
  books = pickle.load(file) # will load a dictionary containing books on the bookshelf
  file.close()

  book_title = data['book_title'].lower()
  if book_title in books:
    response['msg'] = f'''
    Your requested book {book_title} has been found on the bookshelf!
    You will be put in contact with the owner of the book shortly.
    '''
  else:
    response['msg'] = f"sorry we do not have your requested book."
  return jsonify(response)

def password_validity(password):
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
  return (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password))