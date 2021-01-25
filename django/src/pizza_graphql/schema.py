import graphene
from graphene_django.filter import DjangoFilterConnectionField

from pizza_graphql.my_graphql import item_ql


class Query(graphene.ObjectType):
    # 商品一覧を取得
    items = DjangoFilterConnectionField(item_ql.ItemType, filterset_class=item_ql.ItemFilter)
    # idで商品を取得
    item = graphene.relay.Node.Field(item_ql.ItemType)


schema = graphene.Schema(
    query=Query,
)
