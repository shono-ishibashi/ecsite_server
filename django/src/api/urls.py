from django.urls import path
from django.contrib import admin


from . import views


urlpatterns = [
    path('', views.HelloWorld.as_view()),
    path('test/', views.request_test),
    path('test/item/', views.QueryTest.as_view()),
    path('admin/', admin.site.urls, name='admin')
]
