from flask import Flask, request, jsonify
import json, pickle
import book
from user import User

app = Flask(__name__)

users = []

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
  response = {"msg": "Hello bookworm!\n Enter (1) to Login or (2) to Sign Up and access the Bookshelf..."}
  return jsonify(response)
  

@app.route("/login", methods=['POST'])
def login():
  response = {'msg': ""}
  data = json.loads(request.data)
  if "username" not in data:
    response['msg'] = "Enter username"
  if "password" not in data:
    response['msg'] = "Enter password"
  # todo: verify username in database, if not, ask them to sign in
  # todo: check if user has an account with those credentials in database
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

  # if "username" not in data:
  #   response['msg'] = "Enter username"
  #   return jsonify(response)
  # if "password" not in data:
  #   response['msg'] = "Enter password"
  #   return jsonify(response)

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
  
  # todo: verify password appropriate complexity and neither username nor password is empty string
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

  response['msg'] = f"welcome to the Bookshelf {username}"
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