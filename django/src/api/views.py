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
