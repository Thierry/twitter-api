from flask_restplus import reqparse, Namespace, Resource, fields
from app.db import tweet_repository
from app.models import Tweet

api = Namespace('tweets')


tweet_model = api.model('Tweet', {
    'text': fields.String,
    'id': fields.Integer,
    'created_at': fields.DateTime
})

tweet_parser = reqparse.RequestParser()
tweet_parser.add_argument('text', required = True, type=str)

@api.route('/')
class TweetListResource(Resource):
    @api.marshal_with(tweet_model)
    def post(self):
        args = tweet_parser.parse_args()
        if 'text' in args.keys() and args['text'] != '':
            tweet = Tweet(args['text'])
            print(tweet.text)
            tweet_repository.add(tweet)
            return tweet, 201
        else:
            return "", 400

@api.route('/<int:id>')
@api.response(404, 'Tweet not found')
class TweetResource(Resource):
    @api.marshal_with(tweet_model)
    def get(self, id):
        tweet = tweet_repository.get(id)
        if tweet is None:
            api.abort(404, "Tweet not found")
        else:
            return tweet

    def delete(self,id):
        if tweet_repository.get(id) == None:
            api.abort(404, "Tweet not found")
        tweet_repository.delete(id)
        return "",204
