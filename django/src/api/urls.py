from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.HelloWorld.as_view()),
    path('test/', views.request_test)
]
