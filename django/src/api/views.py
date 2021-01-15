from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from . import serializers
from .models import Order, User


auth_url = 'http://nginx:80/auth/'


@api_view(['GET'])
def request_test(request):
    """テスト用のview function

    Args:
        request (object): djangoのrequestオブジェクト

    Returns:
        Response: テスト用のjson
    """
    auth_url = 'http://nginx:80/auth/'
    response = requests.get(url=auth_url)
    data = response.content
    print(data)
    return Response({'res': data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def order(request):
    """注文処理のAPI

    Args:
        request (object): djangoのrequestオブジェクト

    Returns:
        Response: ステータスコード
    """
    token = request.META.get('HTTP_AUTHORIZATION')
    headers = {"Authorization": token}
    response = requests.get(auth_url + "user/?format=json", headers=headers)
    if response.status_code == 401:
        # トークンによる認証が失敗すると401_Unauthorizedを返す
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    try:
        user = User.objects.get(pk=response.json()["user"]["id"])
        order = Order.objects.get(user=user, status=0)
    except Order.DoesNotExist:
        # user_idがログインユーザーのidでかつstatusが0のorderレコードが無ければ404_Not_Foundを返す
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_data = request.data
    serializer = serializers.OrderSerializer(
        order,
        request_data,
        partial=True)
    if serializer.is_valid():
        serializer.save()
        send_confirmation_mail(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # POSTしてきたデータがバリデーションに引っかかった場合400_Bad_Requestを返す
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


def send_confirmation_mail(order_info):
    """注文確定後に宛先Eメールアドレスにメールを送るメソッド

    Args:
        order_info (object): 注文完了時にorderメソッドから渡される注文情報

    Returns:　無し
    """
    subject = "ご注文ありがとうございます。"
    message = "ご注文ありがとうございます。"
    html_message = render_to_string(
        'confirm_mail_template.html',
        {'context': order_info})
    from_email = 'rakus.ec2021@gmail.com'  # 送信者
    recipient_list = [order_info["destination_email"]]  # 宛先リスト
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        html_message=html_message
    )
