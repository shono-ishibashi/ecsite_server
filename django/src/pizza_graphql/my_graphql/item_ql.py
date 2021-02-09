from django_filters import FilterSet, OrderingFilter

import graphene
from graphene_django import DjangoObjectType
from graphene_django.types import ErrorType

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
    name = graphene.String(required=False)
    description = graphene.String(required=False)
    price_m = graphene.Int(required=False)
    price_l = graphene.Int(required=False)
    image_path = graphene.String(required=False)
    deleted = graphene.Boolean(required=False)
    errors = ErrorType()

    class Meta:
        model = Item
        fields = ("name",
                  "description",
                  "price_m",
                  "price_l",
                  "image_path",
                  "deleted",)
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'id': ['exact'],
        }
        connection_class = ItemConnection
        interfaces = (graphene.relay.Node,)
