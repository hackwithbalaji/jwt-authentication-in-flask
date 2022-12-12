import jwt
import uuid

from flask import jsonify, request
from flask_restful import Resource
from datetime import datetime, timedelta

from db import db

from Models import UserEntity, TokenEntity


users = [
    {
        'name' : 'balaji',
        'password' : 123
    }
]

SECRET = "anhhgrgbvjsafgj124rsfkbg"
TOKEN_PAIR = {}

def verify_user(data):
    user = UserEntity.query.filter_by(name = data['name']).first()
    if user and data['password'] == user.password:
        return (True, user)
    return (False, user)

def update_token_pair(token):
    token.is_active = False;
    db.session.add(token)
    db.session.commit()
    user_name = jwt.decode(token.jwt_token, SECRET, algorithms=['HS256'])['user_name']
    return generate_auth_tokens(token.user_id, user_name)

def verify_token_pair(tokens):
    token = TokenEntity.query.filter_by(jwt_token = tokens['jwt_token']).first()
    if token and token.refresh_token == tokens['refresh_token'] and token.is_active == True:
        return (True, token)
    return (False, token)

def create_jwt_token(user_name):
    return jwt.encode({
        'user_name' : user_name,
        'exp' : datetime.utcnow() + timedelta(minutes=15)
    }, SECRET)

def generate_auth_tokens(user_id, user_name):
    jwt_token = create_jwt_token(user_name)
    refresh_token = uuid.uuid1().hex
    token = TokenEntity(user_id = user_id, jwt_token = jwt_token, refresh_token = refresh_token, is_active = True)
    db.session.add(token)
    db.session.commit()
    return token
    
class Signup(Resource):
    def post(self):
        user_input = request.get_json()
        user = UserEntity(**user_input)
        db.session.add(user)
        db.session.commit()
        return user.serialize(), 201

class Login(Resource):
    def post(self):
        user_credentials = request.get_json()
        user = verify_user(user_credentials)
        if user[0]:
            token = generate_auth_tokens(user[1].id, user_credentials['name'])
            return token.serialize(), 200
        return jsonify({'message' : 'Login Failed'})

class User(Resource):
    def get(self, id):
        user = UserEntity.query.get(id)
        if user:
            return jsonify(user.serialize())
        return {"message" : "User not found"}, 404

class RefreshToken(Resource):
    def post(self):
        request_data = request.get_json()
        token = verify_token_pair(request_data)
        if token[0]:
            token = update_token_pair(token[1])
            return token.serialize(), 200
        return "Unauthorized", 401