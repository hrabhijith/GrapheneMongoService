from os import getenv, name
from mongoengine import connect


def init_db():
    uri = getenv('DATABASE_URI')
    name = getenv('DATABASE_NAME')
    connect(name, host=uri, alias='default')
