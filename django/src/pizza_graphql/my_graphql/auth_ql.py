from django_filters import FilterSet, OrderingFilter

import graphene
from graphene_django import DjangoObjectType

# TODO もどす
from api.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)
