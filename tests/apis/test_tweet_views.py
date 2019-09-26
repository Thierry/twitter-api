from flask_testing import TestCase
from app import create_app, db
from app.models import Tweet
import json

class TestTweetViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = f"{app.config['SQLALCHEMY_DATABASE_URI']}_test"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_tweet_show(self):
        self.setUp()
        first_tweet = Tweet("First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.get("/tweets/1")
        response_tweet = response.json
        print(response_tweet)
        self.assertEqual(response_tweet["id"], 1)
        self.assertEqual(response_tweet["text"], "First tweet")
        self.assertIsNotNone(response_tweet["created_at"])

    def test_tweet_delete(self):
        self.setUp()
        first_tweet = Tweet("First tweet")
        db.session.add(first_tweet)
        db.session.commit()
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
        db_tweet = db.session.query(Tweet).get(1)
        self.assertEqual(db_tweet.text,"Created via Internet")

    def test_tweet_create_invalid(self):
        self.setUp()
        json_data = json.dumps({
            "texting": "Created via Internet"
        })
        response = self.client.post("/tweets/", data=json_data, content_type='application/json')
        self.assertIn("400",response.status)
        self.assertEqual(len(db.session.query(Tweet).all()), 0)

    def test_tweet_patch_valid(self):
        json_data = json.dumps({
            "text": "Patched via API call"
        })
        self.setUp()
        first_tweet = Tweet("First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        response = self.client.patch("/tweets/1", data=json_data, content_type='application/json')
        self.assertIn("200",response.status)
        response_tweet = response.json
        first_tweet = db.session.query(Tweet).get(1)
        self.assertEqual(response_tweet["text"], "Patched via API call")
        self.assertEqual(first_tweet.text, "Patched via API call")

    def test_tweet_patch_invalid(self):
        self.setUp()
        first_tweet = Tweet("First tweet")
        db.session.add(first_tweet)
        db.session.commit()
        json_data = json.dumps({
            "textdata": "Patched via API call"
        })
        response = self.client.patch("/tweets/1", data=json_data, content_type='application/json')
        self.assertIn("400",response.status)

    def test_tweet_patch_unknown(self):
        self.setUp()
        json_data = json.dumps({
            "textdata": "Patched via API call"
        })
        response = self.client.patch("/tweets/2", data=json_data, content_type='application/json')
        self.assertIn("404",response.status)
