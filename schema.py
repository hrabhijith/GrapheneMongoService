from flask_graphql_auth.decorators import mutation_header_jwt_refresh_token_required, mutation_header_jwt_required, query_header_jwt_required
import graphene
from graphene.types import json
from graphene.types.scalars import String
from graphene_mongo import MongoengineObjectType
from database import init_db
from models import Users as UsersModel, User as UserModel
from models import Filters as FiltersModel, Factors as FactorsModel
from models import FilterType as FilterTypeModel, FilterInfo as FilterInfoModel, Description as DescriptionModel
from models import Errors as ErrorsModel, ErrorInfo as ErrorInfoModel, Quality as QualityModel, Subjects as SubjectsModel
# from models import Selectors as SelectorsModel
from flask_graphql_auth import (
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
    query_jwt_required,
    mutation_jwt_refresh_token_required,
    mutation_jwt_required,
)

# MongoEngine class to typecast GraphQL Queries for embedded document
# class Selectors(MongoengineObjectType):

#     class Meta:
#         model = SelectorsModel


# MongoEngine class to typecast GraphQL Mutations for embedded document
# class InputSelectors(graphene.InputObjectType):

#     class Meta:
#         model = SelectorsModel


class User(MongoengineObjectType):
    class Meta:
        model = UserModel
    

# MongoEngine class to typecast GraphQL Mutations and Queries for document
class Users(MongoengineObjectType):

    class Meta:
        model = UsersModel


class Description(MongoengineObjectType):
    class Meta:
        model = DescriptionModel


class FilterInfo(MongoengineObjectType):
    class Meta:
        model = FilterInfoModel


class FilterType(MongoengineObjectType):
    class Meta:
        model = FilterTypeModel


class Filters(MongoengineObjectType):

    class Meta:
        model = FiltersModel


class ErrorInfo(MongoengineObjectType):

    class Meta:
        model = ErrorInfoModel


class Errors(MongoengineObjectType):

    class Meta:
        model = ErrorsModel


class Subjects(MongoengineObjectType):
    class Meta:
        model = SubjectsModel


class Quality(MongoengineObjectType):

    class Meta:
        model = QualityModel


class Factors(MongoengineObjectType):

    class Meta:
        model = FactorsModel


# Mutation class for login authentication
# Accepts: Username and Password
# Returns: Auth token and Refresh token
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


# Mutation class for refresh token generation
# Accepts: Refresh token
# Returns: New Auth token
class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_header_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(
            new_token=create_access_token(identity=current_user),
        )


# Query class for all results and results by name (Requires Auth Header)
# allSelections
# Returns: All documents from selections collection from MongoDB
# selectionsByName
# Accepts: Name of the document
# Returns: Only those documents which matches 'name'
class Query(graphene.ObjectType):

    allUsers = graphene.List(Users, token=graphene.String())
    # selectionsByName = graphene.List(Selections, name=graphene.String())

    @query_jwt_required
    def resolve_allUsers(self, info):
        return list(UsersModel.objects.all())

    # @query_header_jwt_required
    # def resolve_selectionsByName(self, info, name):
    #     return list(SelectionsModel.objects.filter(name=name).all())


# Mutation class to create new document in selections collection
# in MongoDB (Requires Auth Header)
# Accepts: name, options [List of embedded documents]
# Returns: Ok flag, All documents from selections collection from MongoDB
# class CreateData(graphene.Mutation):
#     class Arguments(object):
#         name = graphene.String()
#         options = graphene.List(InputSelectors)

#     ok = graphene.Boolean()
#     data = graphene.Field(Selections)

#     @mutation_header_jwt_required
#     def mutate(root, info, name, options):
#         data = SelectionsModel(name=name, options=options)
#         data.save()
#         ok = True
#         return CreateData(data=data, ok=ok)


# # Mutation class to update/add to existing embedded document in selections collection
# # in MongoDB (Requires Auth Header)
# # Accepts: name, options [New List of embedded documents]
# # Returns: Ok flag, All documents from selections collection from MongoDB
# class UpdateData(graphene.Mutation):
#     class Arguments(object):
#         name = graphene.String()
#         options = graphene.List(InputSelectors)

#     ok = graphene.Boolean()
#     data = graphene.Field(Selections)

#     @mutation_header_jwt_required
#     def mutate(root, info, name, options):
#         currentSelection = SelectionsModel.objects.get(name=name)
#         for item in options:
#             temp = SelectorsModel(
#                 selection_id=item['selection_id'], value=item['value'])
#             currentSelection.options.append(temp)

#         currentSelection.save()
#         ok = True
#         return UpdateData(data=currentSelection, ok=ok)


# # Mutation class to delete an existing embedded document using selection_id
# # (Requires Auth Header)
# # Accepts: name, selection_id [Id of the embedded document to be deleted]
# # Returns: Ok flag, All documents from selections collection from MongoDB
# class DeleteData(graphene.Mutation):
#     class Arguments(object):
#         name = graphene.String()
#         selection_id = graphene.String()

#     ok = graphene.Boolean()
#     data = graphene.Field(Selections)

#     @mutation_header_jwt_required
#     def mutate(root, info, name, selection_id):
#         currentSelection = SelectionsModel.objects.get(name=name)

#         for item in currentSelection.options:
#             if item.selection_id == selection_id:
#                 currentSelection.options.remove(item)
#                 currentSelection.save()

#         ok = True
#         return DeleteData(data=currentSelection, ok=ok)


# All mutations are implemented as Graphene object type
class MyMutations(graphene.ObjectType):
    # delete_data = DeleteData.Field()
    # update_data = UpdateData.Field()
    # create_data = CreateData.Field()
    login = AuthMutation.Field()
    refresh = RefreshMutation.Field()


# Intiates Graphene (GraphQL) schema
schema = graphene.Schema(query=Query, mutation=MyMutations, types=[Users])
