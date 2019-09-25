from flask_testing import TestCase
from app import create_app
from app.models import Tweet
from app.db import tweet_repository
import json

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        tweet_repository.clear()

    def test_tweet_show(self):
        self.setUp()
        first_tweet = Tweet("First tweet")
        tweet_repository.add(first_tweet)
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_delete(self):
        self.setUp()
        first_tweet = Tweet("First tweet")
        tweet_repository.add(first_tweet)
        second_tweet = Tweet("Second tweet")
        tweet_repository.add(second_tweet)
        response = self.client.delete("/tweets/1")
        self.assertIn("204",response.status)
        response = self.client.delete("/tweets/1")
        self.assertIn("404",response.status)

    def test_tweet_create_valid(self):
        self.setUp()
        json_data = json.dumps({
            "text": "Created via Internet"
        })
        response = self.client.post("/tweets/", data=json_data, content_type='application/json')
        self.assertIn("201",response.status)
        response_tweet = response.json
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "Created via Internet")
        db_tweet = tweet_repository.get(1)
        self.assertEqual(db_tweet.text,"Created via Internet")

    def test_tweet_create_invalid(self):
        self.setUp()
        json_data = json.dumps({
            "texting": "Created via Internet"
        })
        response = self.client.post("/tweets/", data=json_data, content_type='application/json')
        self.assertIn("400",response.status)
        self.assertEqual(len(tweet_repository.tweets), 0)
