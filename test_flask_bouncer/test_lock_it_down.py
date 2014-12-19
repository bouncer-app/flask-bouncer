from flask import Flask
from flask_bouncer import Bouncer, requires, skip_authorization, ensure
from werkzeug.exceptions import Forbidden
from bouncer.constants import *
from nose.tools import *
from .models import Article, User
from .helpers import user_set

@raises(Forbidden)
def test_lock_it_down_raise_exception():

    app = Flask("test_lock_it_down_raise_exception")
    app.debug = True
    bouncer = Bouncer(app, ensure_authorization=True)

    @bouncer.authorization_method
    def define_authorization(user, they):
        they.can('browse', Article)

    # Non decorated route -- should raise an Forbidden
    @app.route("/articles")
    def articles_index():
        return "A bunch of articles"

    client = app.test_client()

    jonathan = User(name='jonathan', admin=False)
    with user_set(app, jonathan):
        resp = client.get('/articles')


def test_ensure_and_requires_while_locked_down():

    app = Flask("test_ensure_and_requires_while_locked_down")
    app.debug = True
    bouncer = Bouncer(app, ensure_authorization=True)


    @bouncer.authorization_method
    def define_authorization(user, they):
        they.can(READ, Article)
        they.can(EDIT, Article, author_id=user.id)

    @app.route("/articles")
    @requires(READ, Article)
    def articles_index():
        return "A bunch of articles"

    @app.route("/article/<int:post_id>", methods=['POST'])
    def edit_post(post_id):

        # Find an article form a db -- faking for testing
        jonathan = User(name='jonathan', admin=False, id=1)
        article = Article(author_id=jonathan.id)

        # bounce them out if they do not have access
        ensure(EDIT, article)
        # edit the post
        return "successfully edited post"

    client = app.test_client()

    jonathan = User(name='jonathan', admin=False, id=1)
    with user_set(app, jonathan):
        resp = client.get('/articles')
        eq_(b"A bunch of articles", resp.data)

        resp = client.post('/article/1')
        eq_(b"successfully edited post", resp.data)


def test_bypass_route():

    app = Flask("test_lock_it_down_raise_exception")
    app.debug = True
    bouncer = Bouncer(app, ensure_authorization=True)

    @bouncer.authorization_method
    def define_authorization(user, they):
        they.can('browse', Article)

    # Non decorated route -- should raise an Forbidden
    @app.route("/articles")
    @skip_authorization
    def articles_index():
        return "A bunch of articles"

    client = app.test_client()

    jonathan = User(name='jonathan', admin=False)
    with user_set(app, jonathan):
        resp = client.get('/articles')
        eq_(b"A bunch of articles", resp.data)
