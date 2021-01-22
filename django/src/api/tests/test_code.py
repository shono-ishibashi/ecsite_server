from django.test import TestCase
from .factory_boy_config import UserFactory
from api.models import User
from unittest import mock
import requests
import json
from api import views
# Create your tests here.

mock_response = requests.Response()

mock_response.status_code = 201

user = {
    "user": {
        "id": 1
    }
}
user = json.dumps(user).encode('utf-8')
mock_response._content = user
test_mock = mock.MagicMock(return_value=mock_response)
# TODO: 後で消す


class Test(TestCase):
    """Djangoのテストの動作確認のテスト
    """

    def test(self):
        self.assertEqual(1, 1)

    def test_add_cart(self):
        test_mock = mock.MagicMock(return_value=mock_response)
        views.fetch_login_user = test_mock
        cart_url = "/django/cart/"
        UserFactory()
        order_item_data = {
            "order_item": {
                "item": 1,
                "order_toppings": [
                    {
                        "topping": 3
                    }
                ],
                "quantity": 1,
                "size": "M"
            },
            "status": 0,
            "total_price": 1690
        }

        count = User.objects.all().count()
        self.asser
        headers = {"AUTHORIZATION": "test_token"}
        response = self.client.post(
            cart_url, data=order_item_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        # order = Order.objects.get(pk=1)
