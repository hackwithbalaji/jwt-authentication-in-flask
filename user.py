from flask import jsonify
from flask_restful import Resource

users = [
    {
        'uname' : 'balaji',
        'password' : 123
    }
]

class User(Resource):
    def get(self):
        user_details = {"users":[]}
        for user in users:
            user_details["users"].append({"name" : user["uname"]})
        return jsonify(users)