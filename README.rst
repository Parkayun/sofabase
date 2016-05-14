sofabase
========


Couchbase Object Mapper (This is under development)


Installation
~~~~~~~~~~~~

Should install via Github.

.. sourcecode:: bash

   ~ $ pip install git+https://github.com/Parkayun/sofabse.git


Quick start
~~~~~~~~~~~


.. sourcecode:: python

   from datetime import datetime
   from sofabase import SofaBase, Model
   from sofabse.fields import TextField, PasswordField


   db = SofaBase('couchbase://localhost/')


   class User(Model):
       __bucket__ = 'users'
       
       username = TextField(is_key=True)
       something = TextField(max_length=50)
       password = PasswordField()
       created_at = DateTimeField(default=datetime.now)


   user = User(username='tester', something='hello world', password='tester')
   
   # Create
   db.add(user)

   # Read
   print(db.get(User(username='tester')))
   
   # Update
   user.something.value = 'world hello'
   db.set(user)
   
   # Delete
   db.delete(user)

