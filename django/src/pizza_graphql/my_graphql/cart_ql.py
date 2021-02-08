import json

from graphene_django import DjangoObjectType
import graphene
from graphene.relay.node import from_global_id
import graphql

import auth_utils
from api.models import Order, OrderItem, OrderTopping, Topping, User
from api.serializers import CartSerializer
from pizza_graphql.my_graphql.auth_ql import UserType
from pizza_graphql.my_graphql.item_ql import ItemType
from pizza_graphql.my_graphql.topping_ql import ToppingType


############################
# types and connections
############################
class OrderToppingType(DjangoObjectType):
    topping = graphene.Field(type=ToppingType, required=False)

    class Meta:
        model = OrderTopping
        fields = ("topping",)
        interfaces = (graphene.relay.Node,)


class OrderToppingConnection(graphene.relay.Connection):
    class Meta:
        node = OrderToppingType


class OrderItemType(DjangoObjectType):
    item = graphene.Field(type=ItemType, required=False)
    quantity = graphene.Int(required=False)
    size = graphene.String(required=False)
    sub_total_price = graphene.Int(required=False)
    order_toppings = graphene.relay.ConnectionField(OrderToppingConnection, required=False)

    class Meta:
        model = OrderItem
        fields = ("item", "quantity", "size",
                  "order_toppings", "sub_total_price")
        interfaces = (graphene.relay.Node,)

    def resolve_sub_total_price(self, info):
        """OrderItemの値段を計算数メソッド
        """
        topping_price_m = 200
        topping_price_l = 300
        order_item: OrderItem = OrderItem.objects.get(pk=self.id)
        order_toppings: OrderTopping = \
            OrderTopping.objects.filter(order_item=order_item)
        print(order_toppings)
        if order_item.size == "M":
            order_item_price = order_item.quantity * (
                    order_item.item.price_m + topping_price_m
                    * len(order_toppings))
        else:
            order_item_price = order_item.quantity * (
                    order_item.item.price_l + topping_price_l
                    * len(order_toppings))

        return order_item_price


class OrderItemConnection(graphene.relay.Connection):
    class Meta:
        node = OrderItemType


class OrderType(DjangoObjectType):
    user = graphene.Field(type=UserType, required=False)
    status = graphene.Int(required=False)
    total_price = graphene.Int(required=False)
    order_date = graphene.Date(required=False)
    destination_name = graphene.String(required=False)
    destination_email = graphene.String(required=False)
    destination_zipcode = graphene.String(required=False)
    destination_address = graphene.String(required=False)
    destination_tel = graphene.String(required=False)
    delivery_time = graphene.DateTime(required=False)
    payment_method = graphene.Int(required=False)
    order_items = graphene.relay.ConnectionField(OrderItemConnection, required=False)

    class Meta:
        model = Order
        fields = ("user",
                  "status",
                  "total_price",
                  "order_date",
                  "destination_name",
                  "destination_email",
                  "destination_zipcode",
                  "destination_address",
                  "destination_tel",
                  "delivery_time",
                  "payment_method",
                  "order_items"
                  )
        interfaces = (graphene.relay.Node,)


############################
# input
############################

class OrderToppingInput(graphene.InputObjectType):
    topping = graphene.ID()


class OrderItemInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    item = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    size = graphene.String(required=True)
    order_toppings = graphene.List(OrderToppingInput, required=True)


############################
# mutate class
############################
class AddCart(graphene.Mutation):
    class Arguments:
        order_item = OrderItemInput(required=True)
        status = graphene.Int(required=True)
        total_price = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        print("kwargs", kwargs)
        # 更新するために入力された値を格納するdict
        payload = decode_order_item_id(kwargs)

        token = info.context.META.get('HTTP_AUTHORIZATION')
        response = auth_utils.fetch_login_user(token)
        if response.status_code == 401:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="認証時にエラーが発生しました。",
                    extensions={"code": error_code.get("401")})
        login_user_id = response.json()['user']['id']
        User.objects.get(pk=login_user_id)
        serializer = CartSerializer(data=payload)
        if serializer.is_valid():
            order = serializer.create(payload, login_user_id)
            return AddCart(order=order)
        else:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="データの形式が正しくありません。",
                    extensions={"code": error_code.get("400")})


class UpdateCart(graphene.Mutation):
    class Arguments:
        order_items = graphene.List(OrderItemInput, required=True)
        status = graphene.Int(required=True)
        total_price = graphene.Int(required=True)

    order = graphene.Field(OrderType)

    @classmethod
    def mutate(cls, root, info, **kwargs):

        print("##################")
        print(kwargs)
        print("##################")

        payload = decode_order_items_id(kwargs)

        token = info.context.META.get('HTTP_AUTHORIZATION')
        response = auth_utils.fetch_login_user(token)
        if response.status_code == 401:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="認証時にエラーが発生しました。",
                    extensions={"code": error_code.get("401")})
        login_user_id = response.json()['user']['id']
        User.objects.get(pk=login_user_id)
        serializer = CartSerializer(data=payload)
        if serializer.is_valid():
            order = serializer.update(payload, login_user_id)
            return UpdateCart(order=order)
        else:
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="データの形式が正しくありません。",
                    extensions={"code": error_code.get("400")})


class DeleteCart(graphene.Mutation):
    class Arguments:
        order_item_id = graphene.ID(required=True)

    order = graphene.Field(OrderType)

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
        serializer = CartSerializer()

        decoded_order_item_id = from_global_id(kwargs["order_item_id"])[1]

        order = serializer.delete(decoded_order_item_id, user)
        return DeleteCart(order=order)


def decode_order_item_id(encoded_order: dict) -> dict:
    """ relayで生成されるID型のidをDBのidの型(int)に変更するメソッド
    """
    # 更新するために入力された値を格納するdict
    payload = {
        "order_item": {
            "item": '',
            "order_toppings": [
                {
                    "topping": ""
                }
            ],
            "size": "",
            "quantity": None
        },
        "total_price": None
    }

    # payloadに変数を格納
    payload.update(encoded_order)

    payload["order_item"]["item"] = \
        from_global_id(payload["order_item"]["item"])[1]

    order_topping_id_list = list()
    for order_topping in encoded_order["order_item"]["order_toppings"]:
        order_topping_id_list.append(
            {"topping": from_global_id(order_topping["topping"])[1]}
        )

    payload["order_item"]["order_toppings"] = order_topping_id_list

    return payload


def decode_order_items_id(encoded_order: dict) -> dict:
    """ relayで生成されるID型のidをDBのidの型(int)に変更するメソッド
    """
    # 更新するために入力された値を格納するdict
    payload = encoded_order.copy()

    for i in range(len(payload["order_items"])):
        payload["order_items"][i]["id"] = \
            from_global_id(payload["order_items"][i]["id"])[1]
        payload["order_items"][i]["item"] = \
            from_global_id(payload["order_items"][i]["item"])[1]

        for j in range(len(payload["order_items"][i]["order_toppings"])):
            payload["order_items"][i]["order_toppings"][j] = \
                {
                    "topping":
                        from_global_id(payload["order_items"][i]["order_toppings"][j]["topping"])[1]
                }

    print(payload)

    return payload
