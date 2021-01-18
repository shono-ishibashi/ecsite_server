from django.test import TestCase
from django.urls import reverse

from api.models import User, UserUtil
from .factory_boy_config import UserFactory, UserUtilFactory

# Create your tests here.


class AuthTestCase(TestCase):
    def setUp(self):
        self.user_util = UserUtil()

    def test_register_TC1(self):
        url = reverse("api:register")
        data = {
            "name": "test name",
            "email": "test2@email.com",
            "password": "testtest",
            "zipcode": "test",
            "address": "test",
            "telephone": "test",
            "status": "0"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        result_user = User.objects.get(email=data['email'])
        self.assertEqual(data['name'], result_user.name)
        self.assertEqual(data['email'], result_user.email)
        self.assertEqual(data['zipcode'], result_user.zipcode)
        self.assertEqual(data['address'], result_user.address)
        self.assertEqual(data['telephone'], result_user.telephone)
        self.assertEqual(data['status'], result_user.status)

    def test_register_TC2(self):
        url = reverse("api:register")
        data = {
            "email": "test2@email.com",
            "password": "testtest",
            "zipcode": "test",
            "address": "test",
            "telephone": "test",
            "status": "0"
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        url = reverse("api:register")
        data = {
            "name": "test name",
            "email": "test2@email.com",
            "password": "testtest",
            "zipcode": "test",
            "address": "test",
            "telephone": "test",
            "status": "0"
        }
        self.client.post(url, data=data)

        login_url = reverse("api:login")
        login_data = {
            "email": "test2@email.com",
            "password": "testtest",
        }
        response = self.client.post(login_url, login_data)

        self.assertEqual(response.status_code, 201)

    def test_login_failure(self):
        url = reverse("api:register")
        data = {
            "name": "test name",
            "email": "test2@email.com",
            "password": "testtest",
            "zipcode": "test",
            "address": "test",
            "telephone": "test",
            "status": "0"
        }
        self.client.post(url, data=data)

        login_url = reverse("api:login")
        login_data = {
            "email": "test2@email.com",
            "password": "testtest_f",
        }
        response = self.client.post(login_url, login_data)

        self.assertEqual(response.status_code, 401)
