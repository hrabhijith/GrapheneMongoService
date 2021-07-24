from mongoengine import Document
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, ListField, StringField
)


class Selectors(EmbeddedDocument):
    selection_id = StringField()
    value = StringField()


class Selections(Document):
    meta = {'collection': 'selections'}
    name = StringField()
    options = ListField(EmbeddedDocumentField(Selectors))
