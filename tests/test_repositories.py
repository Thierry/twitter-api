from unittest import TestCase
from app.repositories import TweetRepository
from app.models import Tweet

class TestTweetRepository(TestCase):
    def test_instance_variables(self):
        # Create an instance of the `Tweet` class with one argument
        repository = TweetRepository()
        # Check that repository is empty
        self.assertEqual(repository.tweets, list([]))

    def test_add_tweet(self):
        repository = TweetRepository()
        # Check that we can insert a tweet
        repository.add(Tweet("My Tweet"))
        # Check that repository has a new element
        self.assertEqual(len(repository.tweets), 1)

    def test_auto_increment_of_ids(self):
        repository = TweetRepository()
        first_tweet = Tweet("My first tweet")
        repository.add(first_tweet)
        self.assertEqual(first_tweet.id,1)
        second_tweet = Tweet("My second tweet")
        repository.add(second_tweet)
        self.assertEqual(second_tweet.id,2)

    def test_get_tweet(self):
        repository = TweetRepository()
        repository.add(Tweet("First"))
        repository.add(Tweet("Second"))
        tweet = Tweet("Third")
        repository.add(tweet)
        repository.add(Tweet("Fourth"))
        self.assertEqual(repository.get(3), tweet)
        self.assertIsNone(repository.get(5))
