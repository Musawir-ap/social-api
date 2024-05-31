from django.urls import re_path

from . import views

urlpatterns = [
    re_path('api', views.UserSearchViewSet.as_view()),
]