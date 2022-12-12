from flask import jsonify, request
from flask_restful import Resource

from app_db import db

from models import UserEntity
from app_user import verify_user
from app_tokens import generate_auth_tokens, verify_token_pair, update_token_pair

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

class RefreshToken(Resource):
    def post(self):
        request_data = request.get_json()
        token = verify_token_pair(request_data)
        if token[0]:
            token = update_token_pair(token[1])
            return token.serialize(), 200
        return "Unauthorized", 401