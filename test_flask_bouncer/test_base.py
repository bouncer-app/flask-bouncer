from nose.tools import eq_

from flask import Flask
from flask_bouncer import Bouncer


def test_base_registration():

    app = Flask(__name__)
    bouncer = Bouncer(app)

    eq_(bouncer.get_app(), app)


def test_delayed_init():
    app = Flask(__name__)
    bouncer = Bouncer()
    bouncer.init_app(app)

    eq_(bouncer.get_app(), app)



