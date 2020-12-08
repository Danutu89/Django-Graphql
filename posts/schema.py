from graphene import (
    relay,
    Field,
    ObjectType,
    InputObjectType,
    String,
    ID,
    List,
    Int,
)
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField
from .models import Post, Like
from graphql_relay import from_global_id, to_global_id
import graphene_django_optimizer as gql_optimizer
import datetime
from users.schema import UserNode
from tags.schema import TagNode
from tags.models import Tag
from likes.schema import LikeNode

from graphql import GraphQLError

from core.utils import filter_by_query_param

POST_FILTER_FIELDS = {
    "title": ["exact", "icontains"],
    "id": ["exact", "icontains"],
    "tags__id": ["exact", "icontains"],
}

LIKE_FILTER_FIELDS = {
    "type_id": ["exact"],
}


class PostLikeNode(DjangoObjectType):
    class Meta:
        model = Like
        filter_fields = LIKE_FILTER_FIELDS
        interfaces = (relay.Node,)

    created_on_timestamp = String()

    def resolve_created_on_timestamp(self, info):
        return self.created_on.strftime("%A %d %b %H:%M:%S")


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = POST_FILTER_FIELDS
        interfaces = [relay.Node]

    created_on_timestamp = String()
    updated_on_timestamp = String()
    likes = DjangoFilterConnectionField(PostLikeNode)
    tags = DjangoFilterConnectionField(TagNode)

    def resolve_likes(self, info, **kwargs):
        return gql_optimizer.query(
            Like.objects.filter(post_id=self.id).all(), info
        )

    def resolve_tags(self, info):
        return gql_optimizer.query(self.tags.all(), info)

    def resolve_created_on_timestamp(self, info):
        return self.created_on.strftime("%A %d %b")

    def resolve_updated_on_timestamp(self, info):
        return self.updated_on.strftime("%A %d %b %H:%M:%S")


class UpdatePostInput(InputObjectType):
    title = String()
    body = String()
    id = ID(required=True)


class AddPostInput(InputObjectType):
    title = String(required=True)
    body = String(required=True)


class AddPostLikeInput(InputObjectType):
    post_id = ID(required=True)
    like_id = ID(required=True)


class UpdatePostMutation(relay.ClientIDMutation):
    class Input:
        post_data = UpdatePostInput(required=True)
        tags_list = List(ID, required=False)

    post = Field(PostNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, post_data, tags_list):
        current_user = info.context.user.is_authenticated

        if current_user is False:
            return GraphQLError("No permissions.")

        pure_tags_ids = [from_global_id(x)[1] for x in tags_list]
        tags = Tag.objects.filter(pk__in=pure_tags_ids).all()

        post = Post.objects.get(pk=from_global_id(post_data.id)[1])

        if post_data.body:
            post.body = post_data.body
        if post_data.title:
            post.title = post_data.title

        if len(tags_list) > 0:
            post.tags.set(tags)

        post.save()

        return UpdatePostMutation(post=post)


class PostLikeMutation(relay.ClientIDMutation):
    class Input:
        like_data = AddPostLikeInput(required=True)

    message = String()
    id = ID()
    count = Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, like_data):
        current_user = info.context.user.is_authenticated

        if current_user is False:
            return GraphQLError("No permissions.")

        post = Post.objects.get(pk=from_global_id(like_data.post_id)[1])

        like = post.likes.filter(like__author_id=current_user.id).first()

        message = None

        if like is not None:
            id = like.id
            post.likes_count -= 1
            post.likes.remove(like)
            message = "deleted"
        else:
            post.likes.add(
                from_global_id(like_data.like_id)[1],
                through_defaults={
                    "author_id": 1,
                },
            )
            like = Like.objects.filter(
                post_id=post.id,
                author_id=current_user.id,
                type_id=from_global_id(like_data.like_id)[1],
            ).first()
            post.likes_count += 1
            message = "added"
            id = like.id

        post.save()

        return PostLikeMutation(
            message=message,
            count=post.likes_count,
            id=to_global_id(id=id, type="PostLike"),
        )


class AddPostMutation(relay.ClientIDMutation):
    class Input:
        post_data = AddPostInput(required=True)
        tags_list = List(ID, required=True)

    post = Field(PostNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, post_data, tags_list):
        current_user = info.context.user.is_authenticated

        if current_user is False:
            return GraphQLError("No permissions.")

        pure_tags_ids = [from_global_id(x)[1] for x in tags_list]
        tags = Tag.objects.filter(pk__in=pure_tags_ids).all()

        post = Post(
            title=post_data.title,
            body=post_data.body,
            author_id=current_user.id,
            tags_count=len(tags_list),
        )

        post.save()

        post.tags.set(tags)

        post.save()

        return AddPostMutation(post=post)


class PostQuery(ObjectType):
    posts = DjangoFilterConnectionField(PostNode)


class PostMutation(ObjectType):
    update_post = UpdatePostMutation.Field()
    add_post = AddPostMutation.Field()
    add_post_like = PostLikeMutation.Field()
