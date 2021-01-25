import django_filters
from django_filters import FilterSet, OrderingFilter

import graphene
from graphene_django import DjangoObjectType, DjangoListField

from api.models import Item
from graphene_django.filter import DjangoFilterConnectionField


class ItemFilter(FilterSet):
    class Meta:
        model = Item
        fields = {
            "name": ["icontains"],
        }

    order_by = OrderingFilter(
        fields=(
            ('name', 'name'), ('price_m', 'priceM'),
        )
    )


class ItemNode(DjangoObjectType):
    class Meta:
        model = Item
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'id': ['exact'],
        }
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    # 商品一覧を取得
    items = DjangoFilterConnectionField(ItemNode, filterset_class=ItemFilter)
    # idで商品を取得
    item = graphene.relay.Node.Field(ItemNode)


schema = graphene.Schema(query=Query)
