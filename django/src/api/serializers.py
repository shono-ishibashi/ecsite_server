from rest_framework import serializers
# from drf_writable_nested import WritableNestedModelSerializer

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


class OrderToppingSerializer(serializers.ModelSerializer):
    topping = ToppingSerializer(read_only=True)
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
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)

    def create(self, validated_data, user_id):
        user = models.User.objects.get(pk=user_id)
        order = models.Order.objects.create(
            user=user, status=validated_data['status'],
            total_price=validated_data['total_price'])
        for order_item in validated_data['order_items']:
            item = models.Item.objects.get(pk=order_item['item'])
            order_item_obj = models.OrderItem.objects.\
                create(item=item,
                       order=order,
                       quantity=order_item['quantity'],
                       size=order_item['size'])
            for order_topping in order_item['order_toppings']:
                topping = models.Topping.objects.get(
                    pk=order_topping['topping'])
                models.OrderTopping.objects.create(
                    topping=topping, order_item=order_item_obj)
        return order

    class Meta:
        model = models.Order
        fields = '__all__'
