from flask import Flask, request, jsonify
from collections import defaultdict
import json

app = Flask(__name__)
app.data = defaultdict(int)

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])

def welcome():
  return "<p>Welcome to The Bookshelf!</p>"


