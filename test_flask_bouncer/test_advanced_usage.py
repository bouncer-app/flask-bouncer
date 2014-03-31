from flask import Flask
from flask_bouncer import Bouncer, ensure, requires
from bouncer.constants import *
from nose.tools import *
from .models import Article, TopSecretFile, User
from .helpers import user_set

def test_non_standard_names():

    app = Flask("advanced")
    app.debug = True
    bouncer = Bouncer(app)

    bouncer.alias_actions = {
        'browse': 'read'
    }

    @bouncer.authorization_method
    def define_authorization(user, they):
        they.can('browse', Article)

    @app.route("/articles")
    @requires('browse', Article)
    def articles_index():
        return "A bunch of articles"

    client = app.test_client()

    jonathan = User(name='jonathan', admin=False)
    with user_set(app, jonathan):
        resp = client.get('/articles')
        eq_(b"A bunch of articles", resp.data)


def test_action_aliases():

    app = Flask("aliases")
    app.debug = True
    bouncer = Bouncer(app)

    # bouncer.alias_actions = {
    #     'read': 'browse'
    # }

    @bouncer.authorization_method
    def define_authorization(user, they):
        they.can('browse', Article)

    @app.route("/articles")
    @requires('browse', Article)
    def articles_index():
        return "A bunch of articles"

    client = app.test_client()

    jonathan = User(name='jonathan', admin=False)
    with user_set(app, jonathan):
        resp = client.get('/articles')
        eq_(b"A bunch of articles", resp.data)