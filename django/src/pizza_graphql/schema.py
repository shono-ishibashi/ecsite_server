from datetime import datetime, timedelta

from django.db.models import Q
import graphene
import graphql
from graphene_django.filter import DjangoFilterConnectionField

import auth_utils
from api.models import User, UserUtil, Order
from pizza_graphql.my_graphql import item_ql, auth_ql, order_history_ql


class Query(graphene.ObjectType):
    # 商品一覧を取得
    items = DjangoFilterConnectionField(
        item_ql.ItemType, filterset_class=item_ql.ItemFilter)
    # idで商品を取得
    item = graphene.relay.Node.Field(item_ql.ItemType)

    user = graphene.Field(auth_ql.UserType)
    register_user = graphene.Field(auth_ql.UserType)
    order_history = DjangoFilterConnectionField(
        order_history_ql.OrderHistoryType,
        filterset_class=order_history_ql.OrderFilter)

    # 注文履歴
    # def resolve_order_history(self, info):
    #     token = info.context.META.get('HTTP_AUTHORIZATION')
    #     response = auth_utils.fetch_login_user(token)

    #     if response.status_code == 401:
    #         raise graphql.error.located_error.GraphQLError(
    #             message="認証時にエラーが発生しました。")

    #     login_user_id = response.json()['user']['id']
    #     order_history = Order.objects \
    #         .filter(Q(user_id=login_user_id), ~Q(status=0)) \
    #         .all()

    #     return order_history

    def resolve_user(self, info):
        """[summary]

        Args:
            info ([type]): [description]

        Raises:
            graphql.error.located_error.GraphQLError: トークンがヘッダーにないエラー
            graphql.error.located_error.GraphQLError: 認証時のエラー

        Returns:
            objects: ログイン中のユーザー
        """
        token = info.context.META.get('HTTP_AUTHORIZATION')
        if token is None:
            raise graphql.error.located_error.GraphQLError(
                message="No token in request headers")

        try:
            user_util = UserUtil.objects.get(token=token)
        except UserUtil.DoesNotExist:
            raise graphql.error.located_error.GraphQLError(
                message="認証に失敗しました。")

        is_valid_date = user_util.created_at > datetime.now().astimezone() - \
            timedelta(minutes=59)

        if is_valid_date:
            user = User.objects.get(util=user_util)
            return user

        UserUtil.objects.filter(token=token).delete()
        raise graphql.error.located_error.GraphQLLocatedError(
            message="トークンの有効期限切れです。")


class Mutation(graphene.ObjectType):
    register_user = auth_ql.UserSerializerMutation.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
