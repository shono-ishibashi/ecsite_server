from rest_framework import serializers

from . import models


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topping
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    order = OrderSerializer()

    class Meta:
        model = models.OrderItem
        fields = '__all__'


class OrderToppingSerializer(serializers.ModelSerializer):
    topping = ToppingSerializer()
    orderItem = OrderItemSerializer()

    class Meta:
        model = models.OrderTopping
        fields = '__all__'
