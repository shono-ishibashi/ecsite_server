from django.db import models
import factory
from factory.helpers import create


from ..models import User, UserUtil


class UserFactory(factory.django.DjangoModelFactory):
    name = 'test name'
    email = 'example@example.com'
    password = 'testpassword'
    zipcode = '1234567'
    address = 'test address'
    telephone = '0120111111'
    status = '1'

    class Meta:
        model = User
        django_get_or_create = ('email', )


class UserUtilFactory(factory.django.DjangoModelFactory):
    token = 'test token'
    user = factory.RelatedFactory(UserFactory, 'user')

    class Meta:
        model = UserUtil


user = UserFactory()
