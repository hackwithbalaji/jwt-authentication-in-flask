import imp
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Home page"

app.run(port = 5000)