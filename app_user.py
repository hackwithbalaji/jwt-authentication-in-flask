from flask import jsonify
from flask_restful import Resource

from models import UserEntity

def verify_user(data):
    user = UserEntity.query.filter_by(name = data['name']).first()
    if user and data['password'] == user.password:
        return (True, user)
    return (False, user)

class User(Resource):
    def get(self, id):
        user = UserEntity.query.get(id)
        if user:
            return jsonify(user.serialize())
        return {"message" : "User not found"}, 404

