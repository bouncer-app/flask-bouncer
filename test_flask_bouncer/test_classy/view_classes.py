from flask_classy import FlaskView, route
from test_flask_bouncer.models import Article
from flask_bouncer import requires
from bouncer.constants import *


class ArticleView(FlaskView):

    # Used by Bouncer to know what object you are locking down
    # if not explictly set if will try to deduce it from the class name
    __target_model__ = Article

    def index(self):
        """A docstring for testing that docstrings are set"""
        return "Index"

    def get(self, obj_id):
        return "Get " + obj_id

    def put(self, id):
        return "Put " + id

    def patch(self, id):
        return "Patch " + id

    def post(self):
        return "Post"

    def delete(self, id):
        return "Delete " + id

    @requires(READ, Article)
    def custom_read_method(self):
        return "Custom Method"

    def custom_method_with_params(self, p_one, p_two):
        return "Custom Method %s %s" % (p_one, p_two,)

    @route("/routed/")
    def routed_method(self):
        return "Routed Method"

    @route("/route1/")
    @route("/route2/")
    def multi_routed_method(self):
        return "Multi Routed Method"

    @route("/noslash")
    def no_slash_method(self):
        return "No Slash Method"

    @route("/endpoint/", endpoint="basic_endpoint")
    def custom_endpoint(self):
        return "Custom Endpoint"

    @route("/route3/", methods=['POST'])
    def custom_http_method(self):
        return "Custom HTTP Method"