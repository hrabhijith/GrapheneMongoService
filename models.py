from typing import Dict, Text
from mongoengine import Document
from mongoengine.base.fields import ObjectIdField
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import (
    EmbeddedDocumentField, IntField, ListField, StringField, BooleanField
)


# ORM class for embedded document in "Selections" collection in MongoDB
# class Selectors(EmbeddedDocument):
#     selection_id = StringField()
#     value = StringField()


# # ORM class for documents in "Selections" collection in MongoDB
# class Selections(Document):
#     meta = {'collection': 'selections'}
#     name = StringField()
#     options = ListField(EmbeddedDocumentField(Selectors))


class User(EmbeddedDocument):
    username = StringField()
    password = StringField()


class ErrorInfo(EmbeddedDocument):
    label_ids = ListField(IntField)
    source =  ListField(StringField)
    description = StringField()


class Errors(EmbeddedDocument):
    text = StringField()
    checked = BooleanField()
    value = EmbeddedDocumentField(ErrorInfo)


class Description(EmbeddedDocument):
    description = StringField()


class Subjects(EmbeddedDocument):
    text = StringField()
    checked = BooleanField()
    value = EmbeddedDocumentField(Description)
    children = ListField(EmbeddedDocumentField(Errors))


class Quality(EmbeddedDocument):
    text = StringField()
    checked = BooleanField()
    value = EmbeddedDocumentField(Description)
    children = ListField(EmbeddedDocumentField(Subjects))


class Factors(Document):
    meta = {'collection': 'factors'}
    text = StringField()
    checked = BooleanField()
    value = EmbeddedDocumentField(Description)
    children = ListField(EmbeddedDocumentField(Quality))


class FilterInfo(EmbeddedDocument):
    id = IntField()
    name = StringField()
    checked = BooleanField()


class FilterType(EmbeddedDocument):
    name = StringField()
    labels = ListField(EmbeddedDocumentField(FilterInfo))


class Filters(Document):
    meta = {'collection': 'filters'}
    categories = ListField(EmbeddedDocumentField(FilterType))


class Users(Document):
    meta = {'collection': 'users'}
    users = ListField(EmbeddedDocumentField(User))
