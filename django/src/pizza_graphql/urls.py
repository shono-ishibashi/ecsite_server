from django.urls import path
from django.contrib import admin
from graphene_django.views import GraphQLView

from . import views


urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True)),
    path('admin/', admin.site.urls, name='admin'),
]
