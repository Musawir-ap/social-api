from django.urls import include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'search', views.UserSearchViewSet)


urlpatterns = [
    re_path('register', views.RegisterView.as_view(), name='register'),
    re_path('login', views.LoginView.as_view(), name='login'),
    re_path('', include(router.urls)),
]
