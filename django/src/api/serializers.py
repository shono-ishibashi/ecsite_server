from rest_framework import serializers

from . import models


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
