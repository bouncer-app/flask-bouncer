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
        they.can(EDIT, Article, author_id=user.id)

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

* Check out [bouncer](https://github.com/jtushman/bouncer) with more details about defining Abilities
* flask-bouncer looks for `current_user` stored in flask's [g](http://flask.pocoo.org/docs/api/#flask.g)

More docs coming soon ...

# Roadmap
* flask-classy support
* blueprint support

## Questions / Issues
Feel free to ping me on twitter: [@tushman](http://twitter.com/tushman) or add issues or PRs at [https://github.com/jtushman/bouncer](https://github.com/jtushman/state_machine)
