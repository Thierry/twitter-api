from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

db = SQLAlchemy()

from .models import Tweet, User

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'development'

    from config import Config
    app.config.from_object(Config)
    db.init_app(app)
    oauth = OAuth(app)

    github = oauth.remote_app(
        'github',
        consumer_key=app.config['GIT_CONSUMER_KEY'],
        consumer_secret=app.config['GIT_CONSUMER_SECRET'],
        request_token_params={'scope': 'user:email'},
        base_url='https://api.github.com/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://github.com/login/oauth/access_token',
        authorize_url='https://github.com/login/oauth/authorize'
    )

    @app.route('/')
    def index():
        tweets = db.session.query(Tweet).all()
        return render_template('tweet.html', tweets=tweets)


    @app.route('/user')
    def display_user():
        if 'github_token' in session:
            me = github.get('user')
            user = User.get_by_github_id(me.data["id"])
            if not user:
                user = User()
                user.name = me.data["name"]
                user.github_id = me.data["id"]
                user.avatar_url = me.data["avatar_url"]
                user.login = me.data["login"]
                db.session.add(user)
                db.session.commit()
            return str(user)
        return redirect(url_for('login'))

    @app.route('/login')
    def login():
        return github.authorize(callback=url_for('authorized', _external=True))


    @app.route('/logout')
    def logout():
        session.pop('github_token', None)
        return redirect('index')


    @app.route('/login/authorized')
    def authorized():
        resp = github.authorized_response()
        if resp is None or resp.get('access_token') is None:
            return 'Access denied: reason=%s error=%s resp=%s' % (
                request.args['error'],
                request.args['error_description'],
                resp
            )
        session['github_token'] = (resp['access_token'], '')
        me = github.get('user')
        return jsonify(me.data)

    @github.tokengetter
    def get_github_oauth_token():
        return session.get('github_token')

    from .apis.tweets import api as tweets
    api = Api()
    api.add_namespace(tweets)
    api.init_app(app)

    app.config['ERROR_404_HELP'] = False
    return app
