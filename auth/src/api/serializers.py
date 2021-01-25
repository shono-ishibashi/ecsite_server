from django.core.validators import MinLengthValidator
from rest_framework import serializers, validators

from . import models


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validators.UniqueValidator(
        queryset=models.User.objects.all(), message='メールアドレスが重複しています。')])
    password = serializers.CharField(
        validators=[MinLengthValidator(6, message='パスワードが短いです。')],
        write_only=True)
    status = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = '__all__'

    def __str__(self):
        return self.email
