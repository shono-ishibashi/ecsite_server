from graphene_django.rest_framework.mutation import SerializerMutation
import graphene
from graphene_django import DjangoObjectType

# TODO もどす
from api.models import User
from api.serializers import UserSearilizer


class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)


class UserSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSearilizer
