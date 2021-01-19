from django.urls import path
from django.contrib import admin


from . import views


urlpatterns = [
    # path('', views.HelloWorld.as_view()),
    path('test/', views.request_test),
    # path('test/item/', views.QueryTest.as_view()),
    path('admin/', admin.site.urls, name='admin'),
    # path('test/order/', views.ViewOrder.as_view()),
    # path('test/user/', views.ViewUser.as_view()),
    # path('test/user/<int:pk>/', views.ViewUser.as_view()),
    path('cart/', views.cart),
    path('delete_cart/<int:order_item_id>/', views.delete_cart)
]
