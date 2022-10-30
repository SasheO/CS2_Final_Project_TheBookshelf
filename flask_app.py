from flask import Flask, request, jsonify
from collections import defaultdict
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
  return "Hello bookworm!\n Enter (1) to Login or (2) Sign Up to access the Bookshelf..."
  

@app.route("/login", methods=['POST'])
def login():
  data = json.loads(request.data)
  # data should contain username and password. if it doesn't, ask them to log in.
  if "username" not in data:
    return "Invalid login details"
  if "password" not in data:
    return "Invalid login details"
  # todo: verify username in database, if not, ask them to sign in
  # todo: check if user has an account with those credentials in database
  pass

@app.route("/signup", methods=['POST'])
def signup():
  # todo: check if that username isn't taken
  # todo: add username and password to database
  pass


