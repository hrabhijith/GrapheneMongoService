import graphene
from graphene.relay import Node
from graphene.types.scalars import String
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
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
    #node = Node.Field()
    # allListings = MongoengineConnectionField(Listings)

    allSelections = graphene.List(Selections, token=graphene.String())
    selectionsByName = graphene.List(Selections, name=graphene.String())

    @query_jwt_required
    def resolve_allSelections(self, info):
        return list(SelectionsModel.objects.all())

    @query_jwt_required
    def resolve_selectionsByName(self, info, name):
        return list(SelectionsModel.objects.filter(name=name).all())


# class CreateData(graphene.Mutation):
#     class Arguments(object):
#         name = graphene.String()
#         access = graphene.String()
#         token = graphene.String()

#     ok = graphene.Boolean()
#     data = graphene.Field(Selections)

#     @classmethod
#     @mutation_jwt_required
#     def mutate(root, info, name, access):
#         data = SelectionsModel(name=name, access=access)
#         data.save()
#         ok = True
#         return CreateData(data=data, ok=ok)


class MyMutations(graphene.ObjectType):
    # create_data = CreateData.Field()
    login = AuthMutation.Field()
    refresh = RefreshMutation.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Selections])
