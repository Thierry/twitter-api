from datetime import datetime
from sqlalchemy.event import listen

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280), nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User")

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"<Tweet #{self.id}>"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280), nullable=False)
    email = db.Column(db.String(280))
    api_key = db.Column(db.String(280))

    def __repr__(self):
        return f"<User {self.name}>"

    def get_by_api_key(api_key):
        return db.session.query(User).filter_by(api_key=api_key).first() if api_key != None else None

    def generate_api_key(self):
        if not self.api_key:
            self.apik_key = str(uuid.uuid4())
        return self.apik_key

listen(User, 'before_insert', generate_api_key)
