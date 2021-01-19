from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests

from . import serializers
from .models import Order, User


# auth_url = 'http://nginx:80/auth/'


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


@api_view(['GET', 'POST', 'PUT'])
def cart(request):
    """カート機能のAPI

    Args:
        request(object): djangoのrequestオブジェクト 

    Returns:
        Response: ステータスコード
    """
    # token = request.META.get('HTTP_AUTHORIZATION')
    # headers = {"Authorization": token}
    # response = request.get(auth_url + "user/?format=json", headers=headers)
    # if response.status_code == 401:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=2)
            order = Order.objects.get(user=user, status=0)
            serializer = serializers.OrderSerializer(order)
            serializer.data['user']['password'] = "********"
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            empty_order = []
            return Response(empty_order, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        request_data = request.data
        serializer = serializers.OrderSerializer(data=request_data)
        if serializer.is_valid():
            user_id = 2
            serializer.create(request_data, user_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        request_data = request.data
        serializer = serializers.OrderSerializer(data=request_data)
        if serializer.is_valid():
            user_id = 2
            serializer.update(request_data, user_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_cart(request, order_item_id):
    """カート内アイテム削除用のAPI
    Args: 
        request(object): djangoのrequestオブジェクト,
        order_item_id: 削除したいオーダーアイテムのid

    Returns:
        Response: ステータスコード
    """
    # token = request.META.get('HTTP_AUTHORIZATION')
    # headers = {"Authorization": token}
    # response = request.get(auth_url + "user/?format=json", headers=headers)
    serializer = serializers.OrderSerializer()
    user = 2
    serializer.delete(order_item_id, user)
    return Response(status=status.HTTP_200_OK)
