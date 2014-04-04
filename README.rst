flask-bouncer
=============

Flask declarative authorization leveraging `bouncer`_

|Build Status|

**flask-bouncer** is an authorization library for Flask which restricts
what resources a given user is allowed to access. All the permissions
are defined in a **single location**.

Enough chit-chat – show me the code …

Installation
------------

.. code:: bash

    pip install flask-bouncer

Usage
-----

.. code:: python

    from flask.ext.bouncer import requires, ensure, Bouncer
    app = Flask()
    bouncer = Bouncer(app)

    # Define your authorization in one place and in english ...
    @bouncer.authorization_method
    def define_authorization(user, they):
        if user.is_admin:
            they.can(MANAGE, ALL)
        else:
            they.can(READ, ('Article', 'BlogPost'))
            they.can(EDIT, 'Article', lambda a: a.author_id == user.id)

    # Then decorate your routes with your conditions.
    # If it fails it will return a 401
    @app.route("/articles")
    @requires(READ, Article)
    def articles_index():
        return "A bunch of articles"

    @app.route("/topsecret")
    @requires(READ, TopSecretFile)
    def topsecret_index():
        return "A bunch of top secret stuff that only admins should see"

-  When you are dealing with a specific resource, then use the
   ``ensure`` method

.. code:: python

    from flask.ext.bouncer import requires, ensure
    @app.route("/articles/<article_id>")
    @requires(READ, Article)
    def show_article(article_id):
        article = Article.find_by_id(article_id)

        # can the current user 'read' the article, if not it will throw a 401
        ensure(READ,article)
        return render_template('article.html', article=article)

-  Check out `bouncer`_ with more details about defining Abilities
-  flask-bouncer by default looks for ``current_user`` or ``user``
   stored in flask’s `g`_

Flask-Classy Support
--------------------

I ❤ `Flask-Classy`_ Like a lot. Flask-Classy is an extension that adds
class-based REST views to Flask.

1) Define you View similarly as you would with flask-classy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from flask.ext.classy import FlaskView
    from yourapp.models import Article

    class ArticleView(FlaskView)

        # an additional class attribute that you need to add for flask-bouncer
        __target_model__ = Article

        def index(self)
            return "Index"

        def get(self, obj_id):
            return "Get "

        # ... methods for post, delete (and even put, and patch if you so like

2) Register the View with flask and bouncer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    # in your application.py or the like

    app = Flask("classy")
    bouncer = Bouncer(app)
    ArticleView.register(app)

    # Which classy views do you want to lock down, you can pass multiple
    bouncer.monitor(ArticleView)

.. _bouncer: https://github.com/jtushman/bouncer
.. _g: http://flask.pocoo.org/docs/api/#flask.g
.. _Flask-Classy: https://pythonhosted.org/Flask-Classy/

.. |Build Status| image:: https://travis-ci.org/jtushman/flask-bouncer.svg?branch=master
:target: https://travis-ci.org/jtushman/flask-bouncer

Then voila – flask-bouncer will implicitly add the following conditions
to the routes:

-  You need ‘READ’ privileges for ‘index’,‘show’ and ‘get’
-  You need ‘CREATE’ privileges for ‘new’,‘put’ and ‘post’
-  You need ‘UPDATE’ privileges for ‘edit’ and ‘patch’

If you want to over-write the default requirements, just add the
``@requires`` decorator to the function

Configuration
-------------

current\_user
~~~~~~~~~~~~~

By default flask-bouncer will inspect ``g`` for user or current\_user.
You can add your custom loader by decorating a function with
``@bouncer.user_loader``

Other Features:
---------------

-  Plays nice with `flask-login`_
-  Plays nice with blueprints
-  Plays nice with `flask-classy`_

Notes:
------

-  This library focusing only on **Authorization**, we leave
   **Authentication** to other libraries such as `flask-login`_.

Thank You!
----------

-  Ryan Bates, and his excellent CanCan ruby library which this the
   inspiration for this library

Questions / Issues
------------------

Feel free to ping me on twitter: `@tushman`_
or add issues or PRs at `https://github.com/jtushman/bouncer`_

.. _flask-login: http://flask-login.readthedocs.org/en/latest/
.. _flask-classy: https://pythonhosted.org/Flask-Classy/
.. _`https://github.com/jtushman/bouncer`: https://github.com/jtushman/flask-bouncer
.. _@tushman: http://twitter.com/tushman


.. toctree::
   :maxdepth: 2
