from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"search", views.UserSearchViewSet)


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("", include(router.urls)),
    path('send_request/<int:pk>/', views.FriendRequestViewSet.as_view({'post': 'send_request'}), name='send_request'),
    path('accept_request/<int:pk>/', views.FriendRequestViewSet.as_view({'post': 'accept_request'}), name='accept_request'),
    path('reject_request/<int:pk>/', views.FriendRequestViewSet.as_view({'post': 'reject_request'}), name='reject_request'),
    path('friends/', views.UserViewSet.as_view({'get': 'friends'}), name='friends'),
    path('pending_requests/', views.UserViewSet.as_view({'get': 'pending_requests'}), name='pending_requests'),
]
