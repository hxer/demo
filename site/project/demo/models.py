#from django.db import models
from mongoengine import *


# Create your models here.
class Post(Document):
    # required=True will be check when fetch the post data
    title = StringField(max_length=120, required=True)
    author = StringField(max_length=30)
    content = StringField(max_length=500, required=True)
    # DateTimeField(default=datetime.datetime.now)      #default is good for lazy
    last_update = DateTimeField(required=True)
