from django_filters import FilterSet, OrderingFilter

import graphene
from graphene_django import DjangoObjectType

from api.models import Item, User


class ItemConnection(graphene.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(self, info):
        return len(self.edges)


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
        connection_class = ItemConnection
        interfaces = (graphene.relay.Node,)
