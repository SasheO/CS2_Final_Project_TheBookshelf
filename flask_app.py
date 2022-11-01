from flask import Flask, request, jsonify
import json, pickle
import book
from user import User

app = Flask(__name__)

users = []

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
  response = {"msg": "Hello bookworm!\n Enter (1) to Login or (2) Sign Up to access the Bookshelf..."}
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
  response = {'msg': ""}
  data = json.loads(request.data)
  print(data)
  if "username" not in data:
    response['msg'] = "Enter username"
    return jsonify(response)
  if "password" not in data:
    response['msg'] = "Enter password"
    return jsonify(response)
  username = data["username"]
  password = data["password"]

  # verify that username is not taken
  file = open('users.pkl','rb')
  users = pickle.load(file) # will be load a list of already existing User type objects
  file.close()
  
  for user in users:
    if user.username == username:
      response['msg'] = "username taken, choose another one"
      return jsonify(response)
  
  # todo: verify password appropriate complexity

  new_user = User(username, password)
  users.append(new_user)
  # Open a file to write bytes
  p_file = open('users.pkl', 'wb')
  # Pickle the list
  pickle.dump(users, p_file)
  p_file.close()
  response['msg'] = f"welcome to the Bookshelf {username}"
  return jsonify(response)
  