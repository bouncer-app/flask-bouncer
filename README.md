flask-bouncer (ALPHA)
=============

Flask declarative authorization leveraging [bouncer](https://github.com/jtushman/bouncer)

[![Build Status](https://travis-ci.org/jtushman/flask-bouncer.svg?branch=master)](https://travis-ci.org/jtushman/flask-bouncer)

# Installation

```bash
pip install flask-bouncer
```

# Usage

```python
from flask.ext.bouncer import requires, ensure, Bouncer
app = Flask()
bouncer = Bouncer(app)

# Define your authorization in one place and in english ...
@bouncer.authorization_method
def define_authorization(user, they):

    if user.is_admin:
        # self.can_manage(ALL)
        they.can(MANAGE, ALL)
    else:
        they.can(READ, Article)

        def if_author(article):
            return article.author_id = user.id

        they.can(EDIT, Article, if_author)

# Then decorate your routes with your conditions.  If it fails it will throw a 401
@app.route("/articles")
@requires(READ, Article)
def articles_index():
    return "A bunch of articles"

@app.route("/topsecret")
@requires(READ, TopSecretFile)
def topsecret_index():
    return "A bunch of top secret stuff that only admins should see"
```

# When you are dealing with a specific resource, then use the `ensure` method

```python
from flask.ext.bouncer import requires, ensure
@app.route("/articles/<article_id>")
@requires(READ, Article)
def show_article(article_id):
    article = Article.find_by_id(article_id)

    # can the current user 'read' the article, if not it will throw a 401
    ensure(READ,article)
    return render_template('article.html',article=article)
```


* Check out [bouncer](https://github.com/jtushman/bouncer) with more details about defining Abilities
* flask-bouncer looks for `current_user` or `user` stored in flask's [g](http://flask.pocoo.org/docs/api/#flask.g)

Other Features:

* Plays nice with [flask-login](http://flask-login.readthedocs.org/en/latest/)
* Plays nice with blueprints
* Plays nice with [flask-classy](https://pythonhosted.org/Flask-Classy/)

# Roadmap
* flask-classy support
* blueprint support

## Questions / Issues
Feel free to ping me on twitter: [@tushman](http://twitter.com/tushman) or add issues or PRs at [https://github.com/jtushman/bouncer](https://github.com/jtushman/state_machine)
