from graphene_django import DjangoObjectType
from api.models import Order, OrderItem, OrderTopping, Topping
from graphene_django.rest_framework.mutation import SerializerMutation
import graphene
import graphql

import auth_utils
from api.models import User
from api.serializers import CartSerializer


class ToppingType(DjangoObjectType):
    class Meta:
        model = Topping
        fields = "__all__"


class OrderToppingType(DjangoObjectType):
    class Meta:
        model = OrderTopping
        fields = "__all__"


class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


class CartSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = CartSerializer


class OrderToppingInput(graphene.InputObjectType):
    topping = graphene.Int()


class OrderItemInput(graphene.InputObjectType):
    id = graphene.Int()
    item = graphene.Int(required=True)
    quantity = graphene.Int(required=True)
    size = graphene.String(required=True)
    order_toppings = graphene.List(OrderToppingInput, required=True)


class AddCart(graphene.Mutation):
    class Arguments:
        order_item = OrderItemInput(required=True)
        status = graphene.Int(required=True)
        total_price = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        token = info.context.META.get('HTTP_AUTHORIZATION')
        response = auth_utils.fetch_login_user(token)
        if response.status_code == 401:
            raise graphql.error.located_error.GraphQLError(
                message="認証時にエラーが発生しました。")
        login_user_id = response.json()['user']['id']
        user = User.objects.get(pk=login_user_id)
        serializer = CartSerializer(data=kwargs)
        if serializer.is_valid():
            serializer.create(kwargs, login_user_id)
            return Order.objects.get(user=user, status=0)


class UpdateCart(graphene.Mutation):
    class Arguments:
        order_items = graphene.List(OrderItemInput, required=True)
        status = graphene.Int(required=True)
        total_price = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        token = info.context.META.get('HTTP_AUTHORIZATION')
        response = auth_utils.fetch_login_user(token)
        if response.status_code == 401:
            raise graphql.error.located_error.GraphQLError(
                message="認証時にエラーが発生しました。")
        login_user_id = response.json()['user']['id']
        user = User.objects.get(pk=login_user_id)
        serializer = CartSerializer(data=kwargs)
        if serializer.is_valid():
            serializer.update(kwargs, login_user_id)
            return Order.objects.get(user=user, status=0)
