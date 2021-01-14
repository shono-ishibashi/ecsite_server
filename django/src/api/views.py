from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
from django.db import models as django_models
from django import core
import requests

from . import models
from . import serializers

import json
import datetime


class HelloWorld(APIView):
    """
    クラスベースのAPIViewです。
    """

    def get(self, request, format=None):
        return Response({"message": "Hello World!! this is django container"},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        return Response({"message": request_data["message"]},
                        status=status.HTTP_201_CREATED)


@api_view(['GET'])
def request_test(request):
    """テスト用のview function

    Args:
        request (object): djangoのrequestオブジェクト

    Returns:
        Response: テスト用のjson
    """
    url = 'http://nginx:80/auth/'
    response = requests.get(url=url)
    data = response.content
    print(data)
    return Response({'res': data}, status=status.HTTP_200_OK)


# TODO: (ishibashi) 動作確認用のため、後で削除
class QueryTest(generics.ListAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.TestSerializer

# TODO: (fujisawa) 開発時order内確認用　後に削除予定


class ViewOrder(generics.ListAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class ViewUser(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


@api_view(['GET', 'POST'])
def cart(request):
    if request.method == 'GET':
        # TODO: もしorderがなかったときの処理を追加
        # status=0 と userで検索
        order = models.Order.objects.get(status=0)

        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # order_data = models.Order.objects.get(status=0)
        # order = {
        #     'id': str(order_data.id),
        #     'user': str(order_data.user),
        #     'status': str(order_data.status),
        #     'total_price': str(order_data.total_price),
        #     'order_date': str(order_data.order_date),
        #     'destination_name': str(order_data.destination_name),
        #     'destination_email': str(order_data.destination_email),
        #     'destination_zipcode': str(order_data.destination_zipcode),
        #     'destination_address': str(order_data.destination_address),
        #     'destination_tel': str(order_data.destination_tel),
        #     'delivery_time': str(order_data.delivery_time),
        #     'payment_method': str(order_data.payment_method)
        #     'order_item': str(order_data.order_item)
        # }
        # order['order_item'] = []
        # order_item_data = models.OrderItem.objects.filter(order=order_data.id)
        # order_item_data_list = list(order_item_data.values())
        # for orderItem in order_item_data_list:
        #     item_data = models.Item.objects.get(id=orderItem['item'])
        #     item = {
        #         'id': str(item_data.id),
        #         'name': str(item_data.name),
        #         'description': str(item_data.description),
        #         'price_m': str(item_data.price_m),
        #         'price_l': str(item_data.price_l),
        #         'image_path': str(item_data.image_path),
        #         'deleted': str(item_data.deleted)
        #     }
        #     del orderItem['item']
        #     orderItem['item'] = item
        #     order['order_item'].append(orderItem)
        # orders.orderItems = []
        # orderItems = [models.OrderItem.objects.all(
        # ).prefetch_related('order').first()]
        # orderItems = [orders.orderitems.all()]

        # try:
        # orderItems = models.OrderItem.objects.filter(
        #     order__exact=orders).all()
        # orderItems = []
        # orderitems = models.OrderItem.objects.filter(order=orders.id)
        # for orderItem in orderitems:
        #     orderToppings = models.OrderTopping.objects.filter(
        #         order_item=orderItem.id)
        # orderItem.order_topping = orderToppings
        # orders.orderItem = orderitems
        # orderDate = orders.order_date.strftime('%Y/%m/%d')
        # orders.order_date = orderDate
        # deliveryTime = orders.delivery_time.strftime(
        #     '%Y-%m-%d %H:%M:%S')
        # orders.delivery_time = deliveryTime
        # orderId = orders.id
        # orderItems = []
        # orderItems.append(models.OrderItem.objects.get(order=orderId))
        # for orderItem in orderItems:
        #     orderToppings = models.OrderTopping.objects.get(
        #         order_item=orderItem.id)
        #     orderItem.orderTopping = orderToppings
        # order = str(orders)
        # order = models.Order()
        # order.user = orders.user
        # order.status = orders.status
        # order.total_price = orders.total_price
        # order.order_date = json.dumps(
        #     orders.order_data, default=json_serial)
        # # order.order_date = str(orders.order_data)
        # order.destination_name = orders.destination_name
        # order.destination_email = orders.destination_email
        # order.destination_zipcode = orders.destination_zipcode
        # order.destination_address = orders.destination_address
        # order.destination_tel = orders.destination_tel
        # order.delivery_time = json.dumps(
        #     orders.delivery_time, default=json_serial)
        # order.delivery_time = str(orders.delivery_time)
        # order.payment_method = orders.payment_method
        # order = json.dumps(orders.to_dict(), default=json_serial)
        # order = simplejson.dumps(
        #     orders.to_dict(), default=encode, indent=4, ensure_ascii=False)

        # json_order = json.dumps(order, indent=4, ensure_ascii=False)
        # orderItem = core.serializers.serialize("json", orders.orderItem)
        # orderItem = core.serializers.serialize("json", orderItems)

        # except orders.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # except DoesNotExist as e:
        # return Response({'message': e})

    elif request.method == 'POST':
        request_data = request.data
        serializer = serializers.OrderItemSerializer()
        return Response(status=status.HTTP_200_OK)
