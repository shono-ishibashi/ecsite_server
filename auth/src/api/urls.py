from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.HelloWorld.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('user/', views.FetchUser.as_view()),

]
