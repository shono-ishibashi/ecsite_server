from django_filters import FilterSet, OrderingFilter

import graphene
from graphene_django import DjangoObjectType


# TODO もどす
from api.models import Topping


class ToppingFilter(FilterSet):
    class Meta:
        model = Topping
        fields = {
            "name": ["icontains"],
        }


class ToppingType(DjangoObjectType):
    class Meta:
        model = Topping
        interfaces = (graphene.relay.Node,)
