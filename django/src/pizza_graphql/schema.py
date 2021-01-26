from datetime import datetime, timedelta

import graphene
import graphql
from graphene_django.filter import DjangoFilterConnectionField

from api.models import User, UserUtil
from pizza_graphql.my_graphql import item_ql, auth_ql


class Query(graphene.ObjectType):
    # 商品一覧を取得
    items = DjangoFilterConnectionField(
        item_ql.ItemType, filterset_class=item_ql.ItemFilter)
    # idで商品を取得
    item = graphene.relay.Node.Field(item_ql.ItemType)

    user = graphene.Field(auth_ql.UserType)
    register_user = graphene.Field(auth_ql.UserType)

    # 注文履歴
    def resolve_order_history(self, info):
        token = info.context.META.get('HTTP_AUTHORIZATION')

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
