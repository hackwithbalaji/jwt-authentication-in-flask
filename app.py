import jwt
import uuid

from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_restful import Api

from routes import Routes
from user import users

app = Flask(__name__)
api = Api(app)
Routes(api)

SECRET = "anhhgrgbvjsafgj124rsfkbg"
TOKEN_PAIR = {}

def verify_user(data):
    for user in users:
        if user['uname'] == data['uname'] and user['password'] == data['password']:
            return True
    return False

def add_token_pair(jwt_token, refresh_token):
    TOKEN_PAIR[jwt_token] = refresh_token

def update_token_pair(tokens):
    del TOKEN_PAIR[tokens['access_token']]
    user_name = jwt.decode(tokens['access_token'], SECRET, algorithms=['HS256'])['user_name']
    return generate_auth_tokens(user_name)

def verify_token_pair(tokens):
    try:
        if(TOKEN_PAIR[tokens['access_token']] == tokens['refresh_token']):
            return True
        return False
    except KeyError:
        return False

def create_jwt_token(user_name):
    return jwt.encode({
        'user_name' : user_name,
        'exp' : datetime.utcnow() + timedelta(minutes=15)
    }, SECRET)

def generate_auth_tokens(user_name):
    jwt_token = create_jwt_token(user_name)
    refresh_token = uuid.uuid1().hex
    add_token_pair(jwt_token, refresh_token)
    return (jwt_token, refresh_token)

@app.route("/")
def home():
    return "Home page"

@app.route('/login', methods=['POST'])
def login():
    """
        Method to login user
    """
    user_credentials = request.get_json()
    if verify_user(user_credentials):
        token = generate_auth_tokens(user_credentials['uname'])
        print(TOKEN_PAIR)
        return jsonify(
            {
                'message' : 'Login Success',
                'access_token' : token[0],
                'refresh_token' : token[1]
            }
        )
    print(TOKEN_PAIR)
    return jsonify({'message' : 'Login Failed'})

@app.route('/refresh-token', methods=['POST'])
def refresh_token():
    """
        Method to Refresh jwt token
    """
    request_data = request.get_json()
    if verify_token_pair(request_data):
        token = update_token_pair(request_data)
        print(TOKEN_PAIR)
        return jsonify(
            {
                'access_token' : token[0],
                'refresh_token' : token[1]
            }
        )
    print(TOKEN_PAIR)
    return "Unauthorized", 401
