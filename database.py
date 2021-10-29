import os
from mongoengine import connect


def init_db():
    uri = os.environ.get('DATABASE_URI')
    db = os.environ.get('DATABASE_NAME')
    connect(db=db, host=uri, alias='default')
