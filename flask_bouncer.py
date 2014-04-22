#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import wraps

from flask import request, g, current_app, _app_ctx_stack as stack
from werkzeug.local import LocalProxy
from werkzeug.exceptions import Unauthorized
from bouncer import Ability
from bouncer.constants import *


# Convenient references
_bouncer = LocalProxy(lambda: current_app.extensions['bouncer'])


def ensure(action, subject):
    request._authorized = True
    current_user = _bouncer.get_current_user()
    ability = Ability(current_user)
    ability.authorization_method = _bouncer.get_authorization_method()
    ability.aliased_actions = _bouncer.alias_actions
    if ability.cannot(action, subject):
        msg = "{0} does not have {1} access to {2}".format(current_user, action, subject)
        raise Unauthorized(msg)

# alais
bounce = ensure


class Condition(object):

    def __init__(self, action, subject):
        self.action = action
        self.subject = subject

    def test(self):
        ensure(self.action, self.subject)


def requires(action, subject):
    def decorator(f):
        f._explict_rule_set = True

        @wraps(f)
        def decorated_function(*args, **kwargs):
            Condition(action, subject).test()
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def skip_authorization(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request._authorized = True
        return f(*args, **kwargs)
    return decorated_function


class Bouncer(object):

    """This class is used to control the Abilities Integration to one or more Flask applications"""

    special_methods = ["get", "put", "patch", "post", "delete", "index"]

    def __init__(self, app=None, **kwargs):

        self.authorization_method_callback = None
        self._alias_actions = self.default_alias_actions()
        self._authorization_method = None
        self.flask_classy_classes = list()
        self.explict_rules = list()
        self.get_current_user = self.default_user_loader

        self.app = None

        if app is not None:
            self.init_app(app, **kwargs)

    def get_app(self, reference_app=None):
        """Helper method that implements the logic to look up an application."""

        if reference_app is not None:
            return reference_app

        if self.app is not None:
            return self.app

        ctx = stack.top

        if ctx is not None:
            return ctx.app

        raise RuntimeError('Application not registered on Bouncer'
                           ' instance and no application bound'
                           ' to current context')

    def init_app(self, app, **kwargs):
        """ Initializes the Flask-Bouncer extension for the specified application.

        :param app: The application.
        """
        self.app = app

        self._init_extension()

        self.app.before_request(self.check_implicit_rules)

        if kwargs.get('ensure_authorization', False):
            self.app.after_request(self.check_authorization)

    def _init_extension(self):
        if not hasattr(self.app, 'extensions'):
            self.app.extensions = dict()

        self.app.extensions['bouncer'] = self

    def check_authorization(self, response):
        """checks that an authorization call has been made during the request"""
        if not hasattr(request, '_authorized'):
            raise Unauthorized
        elif not request._authorized:
            raise Unauthorized
        return response

    def check_implicit_rules(self):
        """ if you are using flask classy are using the standard index,new,put,post, etc ... type routes, we will
            automatically check the permissions for you
        """
        if not self.request_is_managed_by_flask_classy():
            return

        if self.method_is_explictly_overwritten():
            return

        class_name, action = request.endpoint.split(':')
        clazz = [classy_class for classy_class in self.flask_classy_classes if classy_class.__name__ == class_name][0]
        Condition(action, clazz.__target_model__).test()

    def method_is_explictly_overwritten(self):
        view_func = current_app.view_functions[request.endpoint]
        return hasattr(view_func, '_explict_rule_set') and view_func._explict_rule_set is True

    def request_is_managed_by_flask_classy(self):
        if request.endpoint is None:
            return False
        if ':' not in request.endpoint:
            return False
        class_name, action = request.endpoint.split(':')
        return any(class_name == classy_class.__name__ for classy_class in self.flask_classy_classes) \
            and action in self.special_methods

    def default_user_loader(self):
        if hasattr(g, 'current_user'):
            return g.current_user
        elif hasattr(g, 'user'):
            return g.user
        else:
            raise Exception("Excepting current_user on flask's g")

    def user_loader(self, value):
        """
        Use this method decorator to overwrite the default user loader
        """
        self.get_current_user = value
        return value

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

    def monitor(self, *classy_routes):
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
