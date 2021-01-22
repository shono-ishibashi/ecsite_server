# from django.db import models
import factory
from ..models import User, UserUtil, Order


class UserUtilFactory(factory.django.DjangoModelFactory):
    token = 'test_token'

    class Meta:
        model = UserUtil


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    status = '0'
    total_price = 3000


class UserFactory(factory.django.DjangoModelFactory):
    name = 'test_name'
    email = 'example@example.com'
    password = 'testpassword'
    zipcode = '1234567'
    address = 'test address'
    telephone = '0120111111'
    status = '0'

    user = factory.RelatedFactory(OrderFactory, 'user')

    class Meta:
        model = User
        django_get_or_create = ('email',)
