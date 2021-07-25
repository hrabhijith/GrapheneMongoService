from typing import Dict
import graphene
from graphene.relay import Node
from graphene.types.scalars import String
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from mongoengine.fields import EmbeddedDocumentField
from models import Selections as SelectionsModel
from models import Selectors as SelectorsModel
from flask_graphql_auth import (
    AuthInfoField,
    GraphQLAuth,
    get_jwt_identity,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)


class Selectors(MongoengineObjectType):

    class Meta:
        model = SelectorsModel

class InputSelectors(graphene.InputObjectType):

    selection_id = graphene.String()
    value = graphene.String()


class Selections(MongoengineObjectType):

    class Meta:
        model = SelectionsModel


class AuthMutation(graphene.Mutation):
    class Arguments(object):
        username = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    @classmethod
    def mutate(cls, _, info, username, password):
        return AuthMutation(
            access_token=create_access_token(username),
            refresh_token=create_refresh_token(username),
        )


class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(
            new_token=create_access_token(identity=current_user),
        )


class Query(graphene.ObjectType):

    allSelections = graphene.List(Selections, token=graphene.String())
    selectionsByName = graphene.List(Selections, name=graphene.String())

    @query_jwt_required
    def resolve_allSelections(self, info):
        return list(SelectionsModel.objects.all())

    @query_jwt_required
    def resolve_selectionsByName(self, info, name):
        return list(SelectionsModel.objects.filter(name=name).all())


class CreateData(graphene.Mutation):
    class Arguments(object):
        name = graphene.String()
        options = graphene.List(InputSelectors)
        token = graphene.String()

    ok = graphene.Boolean()
    data = graphene.Field(Selections)

    @mutation_jwt_required
    def mutate(root, info, name, options):
        data = SelectionsModel(name=name, options=options)
        data.save()
        ok = True
        return CreateData(data=data, ok=ok)


class UpdateData(graphene.Mutation):
    class Arguments(object):
        name = graphene.String()
        options = graphene.List(InputSelectors)
        token = graphene.String()

    ok = graphene.Boolean()
    data = graphene.Field(Selections)

    @mutation_jwt_required
    def mutate(root, info, name, options):
        currentSelection =  SelectionsModel.objects.get(name=name)
        for item in options:
            temp = SelectorsModel(selection_id = item['selection_id'], value = item['value'])
            currentSelection.options.append(temp)

        currentSelection.save()
        ok = True
        return UpdateData(data=currentSelection, ok=ok)


class DeleteData(graphene.Mutation):
    class Arguments(object):
        name = graphene.String()
        selection_id = graphene.String()
        token = graphene.String()

    ok = graphene.Boolean()
    data = graphene.Field(Selections)

    @mutation_jwt_required
    def mutate(root, info, name, selection_id):
        currentSelection =  SelectionsModel.objects.get(name=name)
        
        for item in currentSelection.options:
            if item.selection_id == selection_id:
                currentSelection.options.remove(item)
                currentSelection.save()          
        
        ok = True
        return DeleteData(data=currentSelection, ok=ok)

class MyMutations(graphene.ObjectType):
    delete_data = DeleteData.Field()
    update_data = UpdateData.Field()
    create_data = CreateData.Field()
    login = AuthMutation.Field()
    refresh = RefreshMutation.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Selections])
