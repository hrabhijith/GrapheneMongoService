import os
from mongoengine import connect


def init_db():
    uri = os.environ.get('DATABASE_URI')
    connect(host=uri)
