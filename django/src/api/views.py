from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from . import serializers
from .models import Order
from django.core.mail import send_mail


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


@api_view(['POST', 'GET'])
def order(request, pk):
    """注文処理のAPI

    Args:
        request (object): djangoのrequestオブジェクト
        pk (int): orderテーブルのプライマリーキー

    Returns:
        Response: ステータスコード
    """
    if request.method == "POST":
        request_data = request.data
        order = Order.objects.get(pk=pk)
        serializer = serializers.OrderSerializer(order, request_data)
        if serializer.is_valid():
            serializer.save()
            destination_email = serializer.data["destination_email"]
            send_confirmation_mail(destination_email)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        # 動作確認でPOSTを投げるため。本番ではGETメソッドは受け取らないのでこの部分は削除予定。
        return Response('order API')

# POSTで送るデータ例
# {
#     "id": 2,
#     "status": 1,
#     "user": 1,
#     "total_price": 1200,
#     "order_data": "2021-01-04",
#     "destination_name": "yuta",
#     "destination_email": "y10@example.com",
#     "destination_zipcode": "000-0000",
#     "destination_address": "5-20-5",
#     "destination_tel": "080-0000-0000",
#     "delivery_time": "2021-01-12T18:14:04.082068+09:00",
#     "payment_method": 2,
# }


def send_confirmation_mail(email_address):
    """注文確定後に宛先Eメールアドレスにメールを送るメソッド

    Args:
        email_address (string): 宛先Eメールアドレス

    Returns:　無し
    """
    subject = "注文確認"
    message = "ご注文ありがとうございます。"
    from_email = 'rakus.ec2021@gmail.com'  # 送信者
    recipient_list = [email_address]  # 宛先リスト
    send_mail(subject, message, from_email, recipient_list)
