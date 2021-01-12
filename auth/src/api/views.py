from datetime import datetime, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers
from .auth_utils import hash_password, generate_token


class HelloWorld(APIView):
    """
    クラスベースのAPIViewです。
    """

    def get(self, request, format=None):
        return Response({"message": "Hello! this is auth container"},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_data = request.data
        return Response({"message": request_data["message"]},
                        status=status.HTTP_201_CREATED)


class RegisterUser(APIView):
    """
    クラスベースのAPIViewです。
    """

    def post(self, request, format=None):
        user_serializer = serializers.UserSerializer(data=request.data)
        # validationエラーがあれば、400を返す。
        if user_serializer.is_valid():
            data = request.data
            # passwordをハッシュ化
            data['password'] = hash_password(data['password'])
            user_serializer = serializers.UserSerializer(data=data)
            # save()を呼び出すために再度is_valid()を呼び出す
            user_serializer.is_valid()
            user_serializer.save()
            return Response({'message': 'success creating user'})

        return Response({'message': 'BAD REQUEST',
                         "errors": user_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request, format=None):
        data = request.data
        try:
            user = models.User.objects.get(
                password=hash_password(data['password']),
                email=data['email'])
        except models.User.DoesNotExist:
            return Response({'message': 'ユーザーが存在しないかパスワードが間違っています'},
                            status=status.HTTP_400_BAD_REQUEST)

        user_util = models.UserUtil()
        user_util.user = user
        user_util.token = generate_token()
        user_util.save()

        return Response({'token': user_util.token})


class FetchUser(APIView):
    def get(self, request, format=None):
        token = request.META.get('HTTP_AUTHORIZATION')
        try:
            user_util = models.UserUtil.objects.get(token=token)
        except models.UserUtil.DoesNotExist:
            return Response({'is_login': False, 'token': token},
                            status=status.HTTP_401_UNAUTHORIZED)

        # 有効期限を10分に設定
        is_valid_date = user_util.created_at > datetime.now().astimezone() - \
            timedelta(minutes=10)
        # TODO: (ishibashi)　エラーの条件分岐
        if is_valid_date:
            user = models.User.objects.get(user__token=token)
            user_serializer = serializers.UserSerializer(user)
            return Response({'user': user_serializer.data},
                            status=status.HTTP_200_OK)

        # 有効期限切れ
        return Response({'is_login': False, 'token': token},
                        status=status.HTTP_401_UNAUTHORIZED)
