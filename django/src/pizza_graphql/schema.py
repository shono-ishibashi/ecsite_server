import graphene
from graphene_django import DjangoObjectType
from ..api.models import Item


class Item(DjangoObjectType):
    class Meta:
        model = Item


class Query(graphene.ObjectType):
    items = graphene.List(Item)
