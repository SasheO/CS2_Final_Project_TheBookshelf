from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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
  if "username" not in data:
    response['msg'] = "Enter username"
  if "password" not in data:
    response['msg'] = "Enter password"
  # todo: verify that username is not take
  # todo: save user to file using pickl?  
  return jsonify(response)