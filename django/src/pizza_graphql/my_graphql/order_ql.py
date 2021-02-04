import json

from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
import graphene
import graphql


import auth_utils
from api.models import Order, User
from api.serializers import OrderSerializer
from api import views


class OrderType02(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class OrderInput(graphene.InputObjectType):
    status = graphene.Int(required=True)
    order_date = graphene.Date(required=True)
    destination_name = graphene.String(required=True)
    destination_address = graphene.String(required=True)
    destination_zipcode = graphene.String(required=True)
    destination_email = graphene.String(required=True)
    destination_tel = graphene.String(required=True)
    delivery_time = graphene.DateTime(required=True)
    payment_method = graphene.Int(required=True)


class OrderSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = OrderSerializer


class ExecuteOrder(graphene.Mutation):
    class Arguments:
        order = OrderInput(required=True)

    order = graphene.Field(OrderType02)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        token = info.context.META.get('HTTP_AUTHORIZATION')
        response = auth_utils.fetch_login_user(token)
        if response.status_code == 401:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="認証時にエラーが発生しました。",
                    extensions={"code": error_code.get("401")})
        login_user_id = response.json()['user']['id']
        user = User.objects.get(pk=login_user_id)
        cart = Order.objects.get(user=user, status=0)
        order_serializer = OrderSerializer(cart, kwargs["order"], partial=True)
        if order_serializer.is_valid():
            order = order_serializer.save()
            views.send_confirmation_mail(order_serializer.data)
            return ExecuteOrder(order=order)
        else:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="データの形式が正しくありません。",
                    extensions={"code": error_code.get("400")})
