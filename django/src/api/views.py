import requests

from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    data = response.json()
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
def cart(request):
    """カート機能のAPI

    Args:
        request(object): djangoのrequestオブジェクト

    Returns:
        Response: ステータスコード
    """
    token = request.META.get('HTTP_AUTHORIZATION')
    headers = {"Authorization": token}
    response = requests.get(auth_url + "user/?format=json", headers=headers)
    if response.status_code == 401:
        # トークンによる認証が失敗すると401_Unauthorizedを返す
        return Response({"message": "ユーザー認証に失敗しました"},
                        status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=response.json()["user"]["id"])
            order = Order.objects.get(user=user, status=0)
            serializer = serializers.CartSerializer(order)
            serializer.data['user']['password'] = "********"
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            # user idがログインユーザーのidでstatusが0のオーダーがなければ空の配列を返す
            empty_order = []
            return Response(empty_order, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        request_data = request.data
        serializer = serializers.CartSerializer(data=request_data)
        if serializer.is_valid():
            user_id = response.json()["user"]["id"]
            serializer.create(request_data, user_id)
            return Response(status=status.HTTP_200_OK)
        else:
            # POSTしてきたデータがバリデーションに引っかかった場合400_Bad_Requestを返す
            return Response({"message": "データの形式が正しくありません"},
                            {"errors": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        request_data = request.data
        serializer = serializers.CartSerializer(data=request_data)
        if serializer.is_valid():
            user_id = response.json()["user"]["id"]
            serializer.update(request_data, user_id)
            return Response(status=status.HTTP_200_OK)
        else:
            # POSTしてきたデータがバリデーションに引っかかった場合400_Bad_Requestを返す
            return Response(
                {"message": "データの形式が正しくありません"},
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
    token = request.META.get('HTTP_AUTHORIZATION')
    headers = {"Authorization": token}
    response = requests.get(auth_url + "user/?format=json", headers=headers)
    if response.status_code == 401:
        # トークンによる認証が失敗すると401_Unauthorizedを返す
        return Response({"message": "ユーザー認証に失敗しました"},
                        status=status.HTTP_401_UNAUTHORIZED)
    serializer = serializers.CartSerializer()
    user = response.json()["user"]["id"]
    serializer.delete(order_item_id, user)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def order(request):
    """注文処理のAPI

    Args:
        request (object): djangoのrequestオブジェクト

    Returns:
        Response: ステータスコード
    """
    token = request.META.get('HTTP_AUTHORIZATION')
    response = fetch_login_user(token)

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


def fetch_login_user(token):
    headers = {"Authorization": token}
    response = requests.get(auth_url + "user/", headers=headers)
    return response
