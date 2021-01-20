from rest_framework import serializers

from . import models


class UserSearilizer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topping
        fields = '__all__'


class OrderToppingSerializer(serializers.ModelSerializer):
    topping = ToppingSerializer(read_only=True)

    class Meta:
        model = models.OrderTopping
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    order_toppings = OrderToppingSerializer(many=True, read_only=True)

    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSearilizer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
