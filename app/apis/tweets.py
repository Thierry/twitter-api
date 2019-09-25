from flask_restplus import Namespace, Resource, fields
from app.db import tweet_repository

api = Namespace('tweets')


tweet_model = api.model('Tweet', {
    'text': fields.String,
    'id': fields.Integer,
    'created_at': fields.DateTime
})

@api.route('/<int:id>')
class TweetResource(Resource):
    @api.marshal_with(tweet_model)
    def get(self, id):
        tweet = tweet_repository.get(id)
        if tweet is None:
            api.abort(404, "Tweet not found")
        else:
            return tweet
