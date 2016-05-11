import random

from sofabase import SofaBase, Model
from sofabase.fields import *


sofa = SofaBase('couchbase://localhost/')


class User(Model):
    __bucket__ = 'users'

    username = TextField(is_key=True)
    something = TextField(max_length=50)
    password = PasswordField()


username = 'asdfasdf%s' % random.randint(1, 10000)
password = '%s' % random.randint(1, 20000)
print(username)
u = User(username=username, something='asdfasdfasdfasdf', password=password)
sofa.add(u)
print(sofa.get(User(username=username)))
sofa.set(User(username=username, something='test'))
print(sofa.get(User(username=username)))
sofa.delete(User(username=username))

