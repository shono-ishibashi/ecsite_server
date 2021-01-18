from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.HelloWorld.as_view()),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user/', views.FetchUser.as_view(), name='user'),

]
