from django.db import models
from django.forms.models import model_to_dict
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(
        max_length=100, unique=True, null=False, blank=False)
    password = models.TextField(null=False, blank=False)
    zipcode = models.CharField(max_length=7, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    telephone = models.CharField(max_length=15, null=False, blank=False)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.TextField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    price_m = models.IntegerField(null=False)
    price_l = models.IntegerField(null=False)
    image_path = models.TextField(null=False)
    deleted = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = 'items'

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.TextField(null=False)
    price_m = models.IntegerField(null=False)
    price_l = models.IntegerField(null=False)

    class Meta:
        db_table = 'toppings'

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(null=False)
    total_price = models.IntegerField(null=False)
    order_date = models.DateField(blank=True, null=True)
    destination_name = models.CharField(max_length=100, blank=True, null=True)
    destination_email = models.CharField(max_length=100, blank=True, null=True)
    destination_zipcode = models.CharField(max_length=7, blank=True, null=True)
    destination_address = models.CharField(
        max_length=200, blank=True, null=True)
    destination_tel = models.CharField(max_length=15, blank=True, null=True)
    delivery_time = models.DateTimeField(blank=True, null=True)
    payment_method = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'orders'


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField()
    size = models.CharField(max_length=1)

    class Meta:
        db_table = 'order_items'


class OrderTopping(models.Model):
    topping = models.ForeignKey(
        Topping, on_delete=models.CASCADE, related_name='order_toppings')
    order_item = models.ForeignKey(
        OrderItem, on_delete=models.CASCADE, related_name='order_toppings')

    class Meta:
        db_table = 'order_toppings'
