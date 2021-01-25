from django.urls import path
from django.contrib import admin


from . import views


urlpatterns = [
    path('test/', views.request_test, name='test'),
    path('admin/', admin.site.urls, name='admin'),
    path('order/', views.order, name='order'),
    path('cart/', views.cart),
    path('delete_cart/<int:order_item_id>/', views.delete_cart)
]
