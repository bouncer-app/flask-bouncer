from flask import request, g, current_app
from werkzeug.exceptions import Unauthorized
from functools import wraps
from bouncer import Ability


def bounce(action, subject):
    current_user = get_current_user()
    ability = Ability(current_user)
    if ability.cannot(action, subject):
        msg = "{} does not have {} access to {}".format(current_user, action, subject)
        raise Unauthorized(msg)


def get_current_user():
    if hasattr(g, 'current_user'):
        return g.current_user
    else:
        raise Exception("Excepting current_user on flask's g")


class Condition(object):

    def __init__(self, action, subject):
        self.action = action
        self.subject = subject

    def test(self):
        bounce(self.action, self.subject)


def requires(action, subject):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            Condition(action, subject).test()
            return f(*args, **kwargs)
        return decorated_function
    return decorator

class Bouncer(object):
    """Thie class is used to control the Abilities Integration to one or more Flask applications"""

    def __init__(self, app):
        self.app = app
        app.bouncer = self

        self.authorization_method_callback = None

    def bounce(self, *classy_routes):
        if self.flask_classy_classes is None:
            self.flask_classy_classes = list()
        self.flask_classy_classes.extend(classy_routes)


    def authorization_method(self, callback):
        """
        the callback for defining user abilities
        """
        self.authorization_method_callback = callback
        Ability.set_authorization_method(self.authorization_method_callback)
        return callback