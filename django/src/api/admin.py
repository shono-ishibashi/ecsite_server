from django.contrib import admin

from .models import User, Item, Topping, Order, OrderItem, OrderTopping

# Register your models here.
my_models = [User, Item, Topping, Order, OrderItem, OrderTopping]
admin.site.register(my_models)
