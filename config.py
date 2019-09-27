import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    GIT_CONSUMER_KEY = os.environ['GIT_CONSUMER_KEY']
    GIT_CONSUMER_SECRET = os.environ['GIT_CONSUMER_SECRET']

