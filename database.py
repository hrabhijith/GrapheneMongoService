import os
from mongoengine import connect

def init_db():
    # client = MongoClient('mongodb+srv://hrabhijith:oAYFYclC5PXnRhkA@cluster0.3tp3t.mongodb.net/qualiexplore02?retryWrites=true&w=majority')
    # return client
    
    # uri = os.environ.get('DATABASE_URI')
    # name = os.environ.get('DATABASE_NAME')
    connect(host="mongodb+srv://hrabhijith:oAYFYclC5PXnRhkA@cluster0.3tp3t.mongodb.net/qualiexplore02?retryWrites=true&w=majority")
