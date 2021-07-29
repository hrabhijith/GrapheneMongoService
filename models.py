from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, ListField, StringField
)


# ORM class for embedded document in "Selections" collection in MongoDB
class Selectors(EmbeddedDocument):
    selection_id = StringField()
    value = StringField()


# ORM class for documents in "Selections" collection in MongoDB
class Selections(Document):
    meta = {'collection': 'selections'}

    name = StringField()
    options = ListField(EmbeddedDocumentField(Selectors))
