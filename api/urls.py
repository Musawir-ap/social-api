from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"search", views.UserSearchViewSet)
# router.register(r"", views.UserSearchViewSet)


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("", include(router.urls)),
    path('send_request/<int:pk>/', views.FriendRequestViewSet.as_view({'post': 'send_request'}), name='send_request'),
]
