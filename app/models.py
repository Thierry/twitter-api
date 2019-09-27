from datetime import datetime
from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.event import listens_for
import uuid


class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280), nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="tweets")

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"<Tweet #{self.id}>"

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(280))
    login = db.Column(db.String(280), nullable=False)
    email = db.Column(db.String(280))
    api_key = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    github_id = db.Column(db.Integer, nullable=False)
    avatar_url = db.Column(db.String(280))
    tweets = db.relationship('Tweet', back_populates="user")

    def __repr__(self):
        return f"<User {self.login}>"

    def __str__(self):
        return self.name if self.name else self.login

    def get_by_api_key(api_key):
        return db.session.query(User).filter_by(api_key=api_key).first() if api_key != None else None

    def get_by_github_id(id):
        return db.session.query(User).filter_by(github_id=id).first() if id != None else None

@listens_for(User, 'before_insert')
def generate_api_key(mapper, connect, self):
        if not self.api_key:
            self.api_key = str(uuid.uuid4())
