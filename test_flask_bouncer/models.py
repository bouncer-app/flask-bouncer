from random import randint
class User(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', randint(1, 10000000000))
        self.name = kwargs['name']
        self.admin = kwargs['admin']
        pass

    @property
    def is_admin(self):
        return self.admin

class Article(object):

    def __init__(self, **kwargs):
        self.author_id = kwargs['author_id']


class TopSecretFile(object):
    pass
