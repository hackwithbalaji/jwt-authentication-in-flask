from user import User

class Routes():
    def __init__(self, api):
        api.add_resource(User, "/api/users")