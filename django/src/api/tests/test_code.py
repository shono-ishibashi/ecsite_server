from django.test import TestCase
from .factory_boy_config import UserFactory, UserFactory02
from api.models import UserUtil, Order, User
from unittest import mock
import requests
import json
from api import views
# Create your tests here.

# orderメソッド内でリクエストを送るauthのfetch_userメソッドをモック化


# TODO: 後で消す
mock_res = requests.Response()

mock_res.status_code = 201
user = {
    "user": {
        "id": "1"
    }
}
user = json.dumps(user).encode('utf-8')
mock_res._content = user
my_mock = mock.MagicMock(return_value=mock_res)


class DjangoTestCase(TestCase):


    """
    Djangoのテストの動作確認のテスト
    """

    # 上で作ったモックを適用

    # @mock.patch('api.views.fetch_login_user',
    #             mock.Mock(return_value=mock_res))
    def test_order_right_order_data(self):
        my_mock = mock.MagicMock(return_value=mock_res)
        views.fetch_login_user = my_mock
        order_url = "/django/order/"
        UserFactory()
        order_data = {
            "id": 1,
            "status": 1,
            "total_price": 100,
            "order_date": "2021-01-04",
            "destination_name": "テスト太郎",
            "destination_email": "test@example.com",
            "destination_zipcode": "0000000",
            "destination_address": "テスト県テスト市テスト町1-11-1",
            "destination_tel": "042-111-1111",
            "delivery_time": "2021-01-12 13:02:09",
            "payment_method": 1,
            "user": 1
        }
        count = User.objects.all().count()
        self.assertEqual(count, 1)
        headers = {"AUTHORIZATION": 'test_token'}
        response = self.client.post(
            order_url, data=order_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(pk=1)
        self.assertEqual(order.destination_name, "テスト太郎")
        my_mock.assert_not_called()

    # @mock.patch('api.views.fetch_login_user',
    #             mock.Mock(return_value=mock_res))
    # def test_order_TC2(self):
    #     my_mock = mock.MagicMock(return_value=mock_res)
    #     views.fetch_login_user = my_mock
    #     UserFactory()
    #     order_url = "/django/order/"
    #     count = User.objects.all().count()
    #     self.assertEqual(count, 1)
    #     order_data = {
    #         "id": 1,
    #         "status": 1,
    #         "total_price": 100,
    #         "order_date": "2021-01-04",
    #         "destination_name": "テスト太郎",
    #         "destination_email": "test@example.com",
    #         "destination_zipcode": "0000000",
    #         "destination_address": "テスト県テスト市テスト町1-11-1",
    #         "destination_tel": "042-111-1111",
    #         "delivery_time": "2021-01-12 13:02:09",
    #         "payment_method": 1,
    #         "user": 1
    #     }
    #     headers = {"AUTHORIZATION": 'test_token'}
    #     response = self.client.post(
    #         order_url, data=order_data, headers=headers)
    #     self.assertEqual(response.status_code, 200)
    #     order = Order.objects.get(pk=1)
    #     self.assertEqual(order.destination_address, "テスト県テスト市テスト町1-11-1")
