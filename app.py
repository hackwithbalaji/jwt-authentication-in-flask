from flask import Flask, jsonify, request
from flask_restful import Api

from routes import Routes
from user import users
from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api = Api(app)
Routes(api)

@app.route("/")
def home():
    return "Home page"
