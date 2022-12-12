import jwt
import uuid

from datetime import datetime, timedelta

from app_db import db

from models import TokenEntity

SECRET = "anhhgrgbvjsafgj124rsfkbg"
TOKEN_PAIR = {}

def generate_auth_tokens(user_id, user_name):
    jwt_token = create_jwt_token(user_name)
    refresh_token = uuid.uuid1().hex
    token = TokenEntity(user_id = user_id, jwt_token = jwt_token, refresh_token = refresh_token, is_active = True)
    db.session.add(token)
    db.session.commit()
    return token

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