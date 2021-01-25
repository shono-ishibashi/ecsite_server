from rest_framework import serializers
# from drf_writable_nested import WritableNestedModelSerializer

from . import models


class UserSearilizer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'


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
        try:
            order = models.Order.objects.get(user=user, status=0)
        except models.Order.DoesNotExist:
            # user idがログイン中のユーザーidでstatusが0のorderがない場合は新規作成
            order = models.Order.objects.create(
                user=user, status=validated_data['status'],
                total_price=validated_data['total_price'])

        order_item = validated_data['order_item']
        print(type(order_item['item']))
        item = models.Item.objects.get(pk=order_item['item'])
        # order_item情報を作成
        order_item_obj = models.OrderItem.objects.\
            create(item=item,
                   order=order,
                   quantity=order_item['quantity'],
                   size=order_item['size'])
        for order_topping in order_item['order_toppings']:
            # toppingを追加
            topping = models.Topping.objects.get(
                pk=order_topping['topping'])
            models.OrderTopping.objects.create(
                topping=topping, order_item=order_item_obj)
        return order

    def update(self, validated_data, user_id):
        user = models.User.objects.get(pk=user_id)
        # user idがログイン中のユーザーでstatusが0のorderを取得
        order = models.Order.objects.get(
            user=user, status=0
        )

        for order_item in validated_data['order_items']:
            # 任意のorder_itemを取得し、更新
            order_item_obj = models.OrderItem.objects.get(pk=order_item['id'])
            order_item_obj.quantity = order_item['quantity']
            order_item_obj.size = order_item['size']
            order_item_obj.save()
            models.OrderTopping.objects.filter(
                order_item=order_item_obj).delete()
            for order_topping in order_item['order_toppings']:
                # 取得したorder_itemのtoppingを更新
                topping = models.Topping.objects.get(
                    pk=order_topping['topping'])
                models.OrderTopping.objects.create(
                    topping=topping, order_item=order_item_obj)

        # orderの合計金額を更新
        order.total_price = validated_data['total_price']
        order.save()
        return order

    def delete(self, order_item_id, user):
        # pkがorder_item_idのorder_itemを取得
        order_item = models.OrderItem.objects.get(pk=order_item_id)
        # 取得したorder_itemのtoppingを削除
        models.OrderTopping.objects.filter(order_item=order_item).delete()
        # order_itemを削除
        order_item.delete()
        # user idがログイン中のユーザーでstatusが0のorderを取得
        order = models.Order.objects.get(user=user, status=0)
        order_items = models.OrderItem.objects.filter(order=order)
        # order内のorder_itemがなければorderごと削除
        if len(order_items) == 0:
            order.delete()

    class Meta:
        model = models.Order
        fields = '__all__'
