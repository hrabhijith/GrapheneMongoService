from mongoengine import connect


def init_db():
    connect('qualiexplore01', host='mongodb+srv://hrabhijith:GoxB1i0NwXX0aIVM@cluster0.3tp3t.mongodb.net/?retryWrites=true&w=majority', alias='default')
