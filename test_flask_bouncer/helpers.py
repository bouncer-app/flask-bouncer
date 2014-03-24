from contextlib import contextmanager
from flask import appcontext_pushed, g

# http://flask.pocoo.org/docs/testing/
@contextmanager
def user_set(app, user):
    def handler(sender, **kwargs):
        g.current_user = user
    with appcontext_pushed.connected_to(handler, app):
        yield
