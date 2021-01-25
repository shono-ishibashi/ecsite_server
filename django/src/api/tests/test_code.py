from django.test import TestCase
from .factory_boy_config import UserFactory, ItemFactory, ToppingFactory

from api.models import Order
from api import views
from api.tests import test_user_utils
# Create your tests here.

# TODO: 後で消す


class Test(TestCase):
    """Djangoのテストの動作確認のテスト
    """

    def test(self):
        self.assertEqual(1, 1)

    def test_add_and_get_cart(self):
        """
        正しいデータをPOSTして、それを正しくGETできるか
        """
        user = UserFactory()

        test_mock = test_user_utils.create_mock(user.pk)
        views.fetch_login_user = test_mock
        cart_url = "/django/cart/"
        ItemFactory()
        ToppingFactory()
        order_item_data = {
            "order_item": {
                "item": 1,
                "order_toppings": [
                    {
                        "topping": 1
                    }
                ],
                "quantity": 1,
                "size": "M"
            },
            "status": 0,
            "total_price": 1690
        }
        headers = {"AUTHORIZATION": 'test_token'}
        response = self.client.post(
            cart_url, data=order_item_data, content_type='application/json',
            headers=headers)
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(pk=1)
        self.assertEqual(order.total_price, 1690)

    def test_add_cart_fail(self):
        """
        正しくないデータをPOSTして400が返ってくるか
        """
        user = UserFactory()

        test_mock = test_user_utils.create_mock(user.pk)
        views.fetch_login_user = test_mock
        cart_url = "/django/cart/"
        ItemFactory()
        ToppingFactory()
        order_item_data = {
            "order_item": {
                "item": 1,
                "order_toppings": [
                    {
                        "topping": 1
                    }
                ],
                "quantity": 1,
                "size": "M"
            },
            "status": 0,
        }
        headers = {"AUTHORIZATION": 'test_token'}
        response = self.client.post(
            cart_url, data=order_item_data, content_type='application/json',
            headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_update_cart(self):
        """
        カート内のデータを正しく更新できるか
        """
        user = UserFactory()

        test_mock = test_user_utils.create_mock(user.pk)
        views.fetch_login_user = test_mock
        cart_url = "/django/cart/"
        ItemFactory()
        ToppingFactory()
        order_item_post_data = {
            "order_item": {
                "item": 1,
                "order_toppings": [
                    {
                        "topping": 1
                    }
                ],
                "quantity": 1,
                "size": "M"
            },
            "status": 0,
            "total_price": 1690
        }
        order_item_put_data = {
            "order_items": [
                {
                    "id": 1,
                    "item": 1,
                    "order_toppings": [
                        {
                            "topping": 2
                        }
                    ],
                    "quantity": 1,
                    "size": "M"
                }
            ],
            "status": 0,
            "total_price": 1490
        }
        headers = {"AUTHORIZATION": 'test_token'}
        response = self.client.post(
            cart_url, data=order_item_post_data,
            content_type='application/json', headers=headers
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.put(
            cart_url, data=order_item_put_data,
            content_type='application/json', headers=headers
        )
        self.assertEqual(response.status_code, 200)
