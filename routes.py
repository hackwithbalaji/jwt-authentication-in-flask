from user import User, Login, Signup, RefreshToken

class Routes():
    def __init__(self, api):
        api.add_resource(User, "/api/user/<int:id>")
        api.add_resource(Signup, "/api/signup")
        api.add_resource(Login, "/api/login")
        api.add_resource(RefreshToken, "/api/refresh-token")