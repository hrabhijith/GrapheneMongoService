import os
from mongoengine import connect


def init_db():
    uri = os.environ.get('DATABASE_URI')
    name = os.environ.get('DATABASE_NAME')
    connect(name, host=uri, alias='default')
