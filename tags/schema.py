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
from .models import Tag
from graphql_relay import from_global_id
from graphql import GraphQLError
import datetime

from core.utils import filter_by_query_param

TAG_FILTER_FIELDS = {
    "name": ["exact", "icontains"],
    "id": ["exact", "icontains"],
}


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        filter_fields = TAG_FILTER_FIELDS
        interfaces = [relay.Node]

    created_on_timestamp = String()
    updated_on_timestamp = String()

    def resolve_created_on_timestamp(self, info):
        return self.created_on.strftime("%A %d %b")

    def resolve_updated_on_timestamp(self, info):
        return self.updated_on.strftime("%A %d %b %H:%M:%S")


class AddTagInput(InputObjectType):
    name = String(required=True)
    color = String()


class AddTagMutation(relay.ClientIDMutation):
    class Input:
        tag_data = AddTagInput(required=True)

    tag = Field(TagNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, tag_data):
        current_user = info.context.user.is_authenticated

        if current_user is False:
            return GraphQLError("No permissions.")

        tag = Tag(name=tag_data.name, color=tag_data.color)
        tag.save()

        return AddTagMutation(tag=tag)


class TagQuery(ObjectType):
    tags = DjangoFilterConnectionField(TagNode)


class TagMutation(ObjectType):
    add_tag = AddTagMutation.Field()