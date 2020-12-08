from graphene import (
    relay,
    Field,
    ObjectType,
    InputObjectType,
    String,
    ID,
)
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from .models import Like
from graphql_relay import from_global_id, to_global_id
from graphql import GraphQLError
import datetime

from core.utils import filter_by_query_param

LIKE_FILTER_FIELDS = {
    "name": ["exact", "icontains"],
    "id": ["exact", "icontains"],
}


class LikeNode(DjangoObjectType):
    class Meta:
        model = Like
        filter_fields = LIKE_FILTER_FIELDS
        interfaces = [relay.Node]

    created_on_timestamp = String()
    updated_on_timestamp = String()

    def resolve_created_on_timestamp(self, info):
        return self.created_on.strftime("%A %d %b")

    def resolve_updated_on_timestamp(self, info):
        return self.updated_on.strftime("%A %d %b %H:%M:%S")


class AddLikeTypeInput(InputObjectType):
    name = String(required=True)
    icon = String()


class AddLikeTypeMutation(relay.ClientIDMutation):
    class Input:
        like_data = AddLikeTypeInput(required=True)

    like = Field(LikeNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, like_data):
        current_user = info.context.user.is_authenticated

        if current_user is False or not current_user.is_staff:
            return GraphQLError("No permissions.")

        like = Like(name=like_data.name, icon=like_data.icon)
        like.save()

        return AddLikeTypeMutation(like=like)


class RemoveLikeTypeInput(InputObjectType):
    id = ID()


class RemoveLikeTypeMutation(relay.ClientIDMutation):
    class Input:
        like_data = RemoveLikeTypeInput(required=True)

    message = String()
    id = ID()

    @classmethod
    def mutate_and_get_payload(cls, root, info, like_data):
        current_user = info.context.user.is_authenticated

        if current_user is False or not current_user.is_staff:
            return GraphQLError("No permissions.")

        like = Like(id=like_data.id)
        like.remove()

        return RemoveLikeTypeMutation(message="success", id=like_data.id)


class LikeQuery(ObjectType):
    likes = DjangoFilterConnectionField(LikeNode)


class LikeMutation(ObjectType):
    add_like_type = AddLikeTypeMutation.Field()
    remove_like_type = RemoveLikeTypeMutation.Field()
    likes = relay.Node.Field(LikeNode)