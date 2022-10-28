from flask import Flask, request, jsonify
from collections import defaultdict
import json

app = Flask(__name__)
app.data = defaultdict(int)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
  # todo: ask user to log in or sign up
  return "<p>Welcome to The Bookshelf!</p>"

@app.route("/login", methods=['POST'])
def login():
  # todo: check if user has an account with those credentials in database
  pass

@app.route("/signup", methods=['POST'])
def signup():
  # todo: check if that username isn't taken
  # todo: add username and password to database
  pass


