from django.urls import path
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from pizza_graphql.schema import schema

urlpatterns = [
    path('', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('admin/', admin.site.urls, name='admin'),
]
