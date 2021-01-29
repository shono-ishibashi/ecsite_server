import json

from django.db.models import Q
from django_filters import FilterSet, OrderingFilter
import graphene
import graphql
from graphene_django import DjangoObjectType

import auth_utils
# TODO もどす
from api.models import Order


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
        }

    order_by = OrderingFilter(
        fields=(
            ('order_date', 'order_date'), ('id', 'id'),
        )
    )


class OrderHistoryType(DjangoObjectType):
    """
    ログイン中のユーザーの注文履歴を取得
    """

    class Meta:
        model = Order
        interfaces = (graphene.relay.Node,)

    @classmethod
    def get_queryset(cls, queryset, info):
        token = info.context.META.get('HTTP_AUTHORIZATION')
        response = auth_utils.fetch_login_user(token)
        if response.status_code == 401:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="認証時にエラーが発生しました。", extensions={"code": error_code.get("401")})

        login_user_id = response.json()['user']['id']
        return queryset.filter(Q(user_id=login_user_id), ~Q(status=0))
