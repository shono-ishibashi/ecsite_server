from django.urls import path
from django.contrib import admin


from . import views


urlpatterns = [
    path('test/', views.request_test),
    path('admin/', admin.site.urls, name='admin'),
    path('order/', views.order)
    # path('order_test/<int:user_id>', views.get_order)
]
