from graphene import (
    relay,
    ObjectType,
    String,
    InputObjectType,
    Field,
    ID,
)
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphql_relay import from_global_id
from .models import User
from graphql import GraphQLError

USER_FILTER_FIELDS = {"username": ["exact", "icontains"]}


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = USER_FILTER_FIELDS
        interfaces = [
            relay.Node,
        ]

    full_name = String()
    created_on_timestamp = String()
    updated_on_timestamp = String()

    def resolve_full_name(self, info):
        return f"{self.first_name} {self.last_name}"

    def resolve_created_on_timestamp(self, info):
        return self.created_on.strftime("%A %d %b")

    def resolve_updated_on_timestamp(self, info):
        return self.updated_on.strftime("%A %d %b %H:%M:%S")


class UpdateUserInput(InputObjectType):
    id = ID(required=True)
    first_name = String()
    last_name = String()


class UpdateUserMutation(relay.ClientIDMutation):
    class Input:
        user_data = UpdateUserInput(required=True)

    user = Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, user_data):
        current_user = info.context.user.is_authenticated
        user = User.objects.get(pk=from_global_id(user_data.id)[1])

        if (
            current_user is False
            or not current_user.is_staff
            or current_user.id != user.id
        ):
            return GraphQLError("No permissions.")

        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name

        user.save()

        return UpdateUserMutation(user=user)


class UserQuery(ObjectType):
    users = DjangoConnectionField(UserNode)
    user = relay.Node.Field(UserNode)


class UserMutation(ObjectType):
    update_user = UpdateUserMutation.Field()