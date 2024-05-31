from django.urls import re_path

from . import views

urlpatterns = [
    re_path('register', views.RegisterView.as_view(), name='register'),
    re_path('login', views.LoginView.as_view(), name='login'),
]