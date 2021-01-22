from api.models import Order
from api import views
from django.test import TestCase
from .factory_boy_config import UserFactory


from api.tests import my_test_utils
# Create your tests here.

order_url = "/django/order/"


class DjangoTestCase(TestCase):

    """
    Djangoのテストの動作確認のテスト
    """

    # 上で作ったモックを適用

    def test_order_01_correct_data(self):
        """
        正しい形式のOrderをPOSTして、ステータスコード200が返ってくるか
        """
        user_factory = UserFactory()

        # views.fetch_login_user()のモックを作成するメソッドを呼び出している
        my_mock = my_test_utils.create_mock(user_factory.pk)
        views.fetch_login_user = my_mock

        order_data = {
            "id": user_factory.pk,
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
            "user": user_factory.pk
        }
        headers = {"AUTHORIZATION": 'test_token'}
        response = self.client.post(
            order_url, data=order_data, headers=headers)
        self.assertEqual(response.status_code, 200)

        order = Order.objects.get(pk=user_factory.pk)
        self.assertAlmostEqual(order.destination_name, "テスト太郎")

    def test_order_02_update_order(self):
        """
        正しい形式のOrderをPOSTして、DBのOrderが正しくUPDATEされるか
        """
        user_factory = UserFactory()
        my_mock = my_test_utils.create_mock(user_factory.pk)
        views.fetch_login_user = my_mock

        order_data = {
            "id": user_factory.pk,
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
            "user": user_factory.pk
        }
        headers = {"AUTHORIZATION": 'test_token'}

        # UPDATE前のOrderを取得
        order = Order.objects.get(pk=user_factory.pk)

        self.client.post(order_url, data=order_data, headers=headers)

        # UPDATE後のOrderを取得
        updated_order = Order.objects.get(pk=user_factory.pk)

        self.assertNotEqual(order.status, updated_order.status)
        self.assertEqual(updated_order.status, 1)
        self.assertEqual(updated_order.destination_name, "テスト太郎")
        self.assertEqual(updated_order.destination_email, "test@example.com")
        self.assertEqual(
            updated_order.destination_address,
            "テスト県テスト市テスト町1-11-1")

    def test_order_02_uncorrect_data(self):
        """
        不正な形式のOrderをPOSTして、ステータスコード400が返ってくるか
        """

        user_factory = UserFactory()
        my_mock = my_test_utils.create_mock(user_factory.pk)
        views.fetch_login_user = my_mock

        order_data = {
            "id": user_factory.pk,
            "status": 1,
            "total_price": 100,
            "order_date": "2021-01-04",
            "destination_name": "テスト太郎",
            "destination_email": "test@example.com",
            "destination_zipcode": "0000000",
            "destination_address": "テスト県テスト市テスト町1-11-1",
            "destination_tel": "042-111-1111",
            "delivery_time": "2021-01-12 13:02:09",
            "payment_method": "uncorrect",  # Integer以外の不正な値
            "user": user_factory.pk
        }
        headers = {"AUTHORIZATION": 'test_token'}
        response = self.client.post(
            order_url, data=order_data, headers=headers)
        self.assertEqual(response.status_code, 400)
