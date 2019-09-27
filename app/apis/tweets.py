from flask_restplus import Namespace, Resource, fields
from flask import request
from app.models import Tweet, User
from app import db

api = Namespace('tweets')

tweet_model = api.model('Tweet', {
    'text': fields.String,
    'id': fields.Integer,
    'created_at': fields.DateTime,
    'user': fields.String
})

new_tweet_model = api.model('Tweet', {
    'text': fields.String
})

def get_api_key_user():
    auth_header = request.headers.get('Authorization')
    if auth_header == None or "TWITTER-APIKEY " not in auth_header:
        return None
    api_key = auth_header.split(' ')[1]

    print(f"api_key : {api_key}", flush = True)
    user = User.get_by_api_key(api_key)
    return user

@api.route("") # /tweets
class TweetListResource(Resource):
    @api.marshal_with(tweet_model)
    @api.expect(new_tweet_model, validate = True)
    def post(self):
        try:
            text = api.payload["text"]
        except:
            return "", 400
        user = get_api_key_user()
        if user == None:
            return "Wrong api key or no api key provided", 401
        tweet = Tweet(text)
        tweet.user = user
        db.session.add(tweet)
        db.session.commit()
        return tweet, 201

    @api.marshal_with(tweet_model)
    def get(self):
        tweets = db.session.query(Tweet).all()
        return tweets

@api.route('/<int:id>') # /tweets/{id}
@api.response(404, 'Tweet not found')
class TweetResource(Resource):
    @api.marshal_with(tweet_model)
    def get(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet is None:
            api.abort(404, "Tweet not found")
        else:
            return tweet

    def delete(self,id):
        tweet = db.session.query(Tweet).get(id)
        if tweet == None:
            api.abort(404, "Tweet not found")
        user = get_api_key_user()
        if tweet.user != user:
            return "NOT YOUR TWEET (or forgot api_key?)", 401
        db.session.delete(tweet)
        db.session.commit()
        return "",204

    @api.marshal_with(tweet_model)
    @api.expect(new_tweet_model, validate = True)
    def patch(self, id):
        tweet = db.session.query(Tweet).get(id)
        user = get_api_key_user()
        if tweet == None:
            api.abort(404, "Tweet not found")
        try:
            tweet.text = api.payload["text"]
            if tweet.user != user:
                return "NOT YOUR TWEET (or forgot api_key?)", 401
        except:
            return "", 400
        db.session.commit()
        return tweet
