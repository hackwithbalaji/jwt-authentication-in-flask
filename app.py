import jwt

from datetime import datetime, timedelta
from flask import Flask, jsonify, request

app = Flask(__name__)

SECRET = "anhhgrgbvjsafgj124rsfkbg"
users = [
    {
        'uname' : 'balaji',
        'password' : 123
    }
]

def verify_user(data):
    for user in users:
        if user['uname'] == data['uname'] and user['password'] == data['password']:
            return True
    return False

def create_jwt_token(data):
    return jwt.encode({
        'user_name' : data['uname'],
        'exp' : datetime.utcnow() + timedelta(minutes=15)
    }, SECRET)

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

        return jsonify(
            {
                'message' : 'Login Success',
                'token' : create_jwt_token(user_credentials)
            }
        )
    
    return jsonify({'message' : 'Login Failed'})

    


app.run(port = 5000)