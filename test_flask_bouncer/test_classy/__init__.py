from flask import Flask, url_for
from flask_bouncer import Bouncer, bounce
from test_flask_bouncer.models import Article, User
from test_flask_bouncer.helpers import user_set
from bouncer.constants import *
from .view_classes import ArticleView

from nose.tools import *

app = Flask("classy")
bouncer = Bouncer(app)
ArticleView.register(app)

# Which classy views do you want to lock down, you can pass multiple
bouncer.bounce(ArticleView)

@bouncer.authorization_method
def define_authorization(user, abilities):

    if user.is_admin:
        # self.can_manage(ALL)
        abilities.append(MANAGE, ALL)
    else:
        abilities.append([READ, CREATE], Article)
        abilities.append(EDIT, Article, author_id=user.id)

client = app.test_client()

jonathan = User(name='jonathan', admin=True)
nancy = User(name='jonathan', admin=False)

def test_index():

    # Admin should be able to view all articles
    with user_set(app, jonathan):
        resp = client.get("/article/")
        eq_(b"Index", resp.data)

    # Non Admin should be able to view all articles
    with user_set(app, nancy):
        resp = client.get("/article/")
        eq_(b"Index", resp.data)

def test_post():
    # Admin should be able to create articles
    with user_set(app, jonathan):
        resp = client.post("/article/")
        eq_(b"Post", resp.data)

    # Basic Users should be able to create articles
    with user_set(app, nancy):
        resp = client.post("/article/")
        eq_(b"Post", resp.data)


def test_delete():
    # Admin should be able to delete articles
    with user_set(app, jonathan):
        resp = client.delete("/article/1234")
        eq_(b"Delete 1234", resp.data)

    # Non Admins should NOT be able to delete articles
    with user_set(app, nancy):
        resp = client.delete("/article/1234")
        eq_(resp.status_code, 401)

# def test_get():
#     resp = client.get("/article/1234")
#     eq_(b"Get 1234", resp.data)
#
# def test_put():
#     resp = client.put("/article/1234")
#     eq_(b"Put 1234", resp.data)
#
# def test_patch():
#     resp = client.patch("/article/1234")
#     eq_(b"Patch 1234", resp.data)

# def test_custom_method():
#     resp = client.get("/article/custom_method/")
#     eq_(b"Custom Method", resp.data)
#
# def test_custom_method_with_params():
#     resp = client.get("/article/custom_method_with_params/1234/abcd")
#     eq_(b"Custom Method 1234 abcd", resp.data)
#
# def test_routed_method():
#     resp = client.get("/article/routed/")
#     eq_(b"Routed Method", resp.data)
#
# def test_multi_routed_method():
#     resp = client.get("/article/route1/")
#     eq_(b"Multi Routed Method", resp.data)
#
#     resp = client.get("/article/route2/")
#     eq_(b"Multi Routed Method", resp.data)
#
# def test_no_slash():
#     resp = client.get("/article/noslash")
#     eq_(b"No Slash Method", resp.data)
#
#
# def test_custom_http_method():
#     resp = client.post("/article/route3/")
#     eq_(b"Custom HTTP Method", resp.data)









