import factory
from factory.fuzzy import FuzzyText
from ..models import User, UserUtil, Order, Item, Topping, \
    OrderItem, OrderTopping


class UserFactory(factory.django.DjangoModelFactory):
    name = 'test name'
    email = 'example@example.com'
    password = 'testpassword'
    zipcode = '1234567'
    address = 'test address'
    telephone = '0120111111'
    status = '0'

    class Meta:
        model = User
        django_get_or_create = ('email', )


class UserUtilFactory(factory.django.DjangoModelFactory):
    token = 'test token'
    user = factory.RelatedFactory(UserFactory, 'user')

    class Meta:
        model = UserUtil


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.RelatedFactory(UserFactory, 'user')
    status = 0
    total_price = 2000


class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item

    name = FuzzyText(length=12)
    description = FuzzyText()
    price_m = 1500
    price_l = 2000
    image_path = FuzzyText(length=5)
    deleted = False


class ToppingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topping

    name = FuzzyText(length=7)
    price_m = 200
    price_l = 300


class OrderItem(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem


class OrderTopping(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderTopping
