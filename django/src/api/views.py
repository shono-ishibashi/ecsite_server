from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import generics
import requests

from . import models
from . import serializers


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


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def cart(request):
    """カート機能のAPI

    Args:
        request(object): djangoのrequestオブジェクト 

    Returns:
        Response: ステータスコード
    """
    if request.method == 'GET':
        try:
            user = models.User.objects.get(pk=2)
            order = models.Order.objects.get(user=user, status=0)
            serializer = serializers.OrderSerializer(order)
            serializer.data['user']['password'] = "********"
            return Response(serializer.data, status=status.HTTP_200_OK)
        except models.Order.DoesNotExist:
            empty_order = []
            return Response(empty_order, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        user = models.User.objects.get(pk=2)
        request_data = request.data
        serializer = serializers.OrderSerializer(data=request_data)
        if serializer.is_valid():
            user_id = 2
            serializer.create(request_data, user_id)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)
