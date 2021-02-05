from django_filters import FilterSet, OrderingFilter

import graphene
from graphene_django import DjangoObjectType

# TODO もどす
from api.models import Item, User


class ItemFilter(FilterSet):
    class Meta:
        model = Item
        fields = {
            "name": ["icontains"],
        }

    order_by = OrderingFilter(
        fields=(
            ('name', 'name'), ('price_m', 'price_m'),
        )
    )


class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'id': ['exact'],
        }
        interfaces = (graphene.relay.Node,)
