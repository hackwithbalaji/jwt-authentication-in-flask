from flask import Flask, jsonify, request

app = Flask(__name__)

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
        return jsonify({'message' : 'Login Success'})
    
    return jsonify({'message' : 'Login Failed'})

    


app.run(port = 5000)