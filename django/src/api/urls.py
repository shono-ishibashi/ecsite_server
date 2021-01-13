from django.urls import path
from django.contrib import admin


from . import views


urlpatterns = [
    path('test/', views.request_test),
    path('admin/', admin.site.urls, name='admin'),
    path('order/<int:pk>', views.order)
]
