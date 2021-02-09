import json

import graphene
from graphene_django import DjangoObjectType
from graphene_django.rest_framework.mutation import SerializerMutation
import graphql

from api.models import User
from api.serializers import UserSearilizer
import auth_utils
from pizza_graphql.my_graphql.forms import UserForm


class UserType(DjangoObjectType):
    name = graphene.String(required=False)
    email = graphene.String(required=False)
    zipcode = graphene.String(required=False)
    address = graphene.String(required=False)
    telephone = graphene.String(required=False)

    class Meta:
        model = User
        fields = ("name", "email", "zipcode", "address", "telephone")
        interfaces = (graphene.relay.Node,)


class UserSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSearilizer


class UserRegisterInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    zipcode = graphene.String(required=True)
    address = graphene.String(required=True)
    telephone = graphene.String(required=True)


class UserMutation(graphene.Mutation):
    class Arguments:
        user_data = UserRegisterInput(required=True)

    user = graphene.Field(lambda: UserType)

    def mutate(root, info, **kwargs):
        user_data = kwargs.get("user_data")
        try:
            User.objects.get(email=user_data.get('email'))
            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="入力されたメールアドレスは既に使用されています。",
                    extensions={"code": error_code.get("400")})
        except User.DoesNotExist:
            password = auth_utils.hash_password(user_data.get("password"))
            user_data["password"] = password

            user_form: UserForm = UserForm(
                data=user_data
            )

            if user_form.is_valid():
                user_form.save()
                user_form_data = user_form.cleaned_data
                print(user_form.cleaned_data)
                user = User()
                user.name = user_form_data.get("name")
                user.email = user_form_data.get("email")
                user.zipcode = user_form_data.get("zipcode")
                user.address = user_form_data.get("address")
                user.telephone = user_form_data.get("telephone")
                return UserMutation(user)

            with open("./pizza_graphql/error_code.json", 'r') as json_file:
                error_code = json.load(json_file)
                raise graphql.error.located_error.GraphQLError(
                    message="入力された値が不正です。",
                    extensions={"code": error_code.get("400"),
                                "errors": user_form.errors})
