from flask import request, g, current_app
from werkzeug.exceptions import Unauthorized
from functools import wraps
from bouncer import Ability
from bouncer.constants import *




def ensure(action, subject):
    current_user = get_current_user()
    ability = Ability(current_user)
    ability.authorization_method = current_app.bouncer.get_authorization_method()
    ability.alias_actions = current_app.bouncer.alias_actions
    if ability.cannot(action, subject):
        msg = "{} does not have {} access to {}".format(current_user, action, subject)
        raise Unauthorized(msg)

#alais
bounce = ensure


def get_current_user():
    if hasattr(g, 'current_user'):
        return g.current_user
    elif hasattr(g, 'user'):
        return g.user
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

        self._alias_actions = self.default_alias_actions

        self._authorization_method = None

    @property
    def alias_actions(self):
        return self._alias_actions

    @alias_actions.setter
    def alias_actions(self, value):
        """if you want to override your actions"""
        self._alias_actions = value

    def default_alias_actions(self):
        return {
            READ: [INDEX, SHOW, GET],
            CREATE: [NEW, PUT, POST],
            UPDATE: [EDIT, PATCH]
        }

    def bounce(self, *classy_routes):
        if self.flask_classy_classes is None:
            self.flask_classy_classes = list()
        self.flask_classy_classes.extend(classy_routes)

    def authorization_method(self, value):
        """
        the callback for defining user abilities
        """
        self._authorization_method = value
        return self._authorization_method

    def get_authorization_method(self):
        if self._authorization_method is not None:
            return self._authorization_method
        else:
            raise Exception('Expected authorication method to be set')