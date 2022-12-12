from app_db import db

class UserEntity(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    name = db.Column(db.String(40))
    password = db.Column(db.String(40))

    def serialize(self):
        return {
            "id" : self.id,
            "name" : self.name,
            "password" : self.password
        }