from db import db

class TokenEntity(db.Model):
    __tablename__ = "Token"
    
    id = db.Column(db.Integer,primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    jwt_token = db.Column(db.String(100))
    refresh_token = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def serialize(self):
        return {
            "id" : self.id,
            "user_id" : self.user_id,
            "jwt_token" : self.jwt_token,
            "refresh_token" : self.refresh_token
        }
