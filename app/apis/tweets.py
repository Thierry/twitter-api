from flask_restplus import reqparse, Namespace, Resource, fields
from app.models import Tweet
from app import db

api = Namespace('tweets')

tweet_model = api.model('Tweet', {
    'text': fields.String,
    'id': fields.Integer,
    'created_at': fields.DateTime
})

@api.route("") # /tweets
class TweetListResource(Resource):
    @api.marshal_with(tweet_model)
    def post(self):
        try:
            text = api.payload["text"]
        except:
            return "", 400
        tweet = Tweet(text)
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
        db.session.delete(tweet)
        db.session.commit()
        return "",204

    @api.marshal_with(tweet_model)
    def patch(self, id):
        tweet = db.session.query(Tweet).get(id)
        if tweet == None:
            api.abort(404, "Tweet not found")
        try:
            tweet.text = api.payload["text"]
        except:
            return "", 400
        db.session.add(tweet)
        db.session.commit()
        return tweet
