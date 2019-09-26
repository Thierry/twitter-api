from datetime import datetime

from app import db

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280), nullable=False, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"<Tweet #{self.id}>"
