from graphene_federation import build_schema

from authentification.schema import AuthMutation
from posts.schema import PostQuery, PostMutation
from users.schema import UserQuery, UserMutation
from likes.schema import LikeQuery, LikeMutation
from tags.schema import TagQuery, TagMutation


class Query(PostQuery, UserQuery, LikeQuery, TagQuery):
    pass


class Mutation(
    PostMutation, UserMutation, LikeMutation, TagMutation, AuthMutation
):
    pass


schema = build_schema(Query, mutation=Mutation)
