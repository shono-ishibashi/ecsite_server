from rest_framework import serializers

from . import models


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'
