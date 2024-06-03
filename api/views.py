from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle

from .models import FriendRequest, User
from .serializers import UserSerializer, FriendRequestSerializer


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data["password"])
        user.email = request.data["email"].lower()
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email").lower()
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class UserSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_query = self.request.query_params.get("q", "")
        if "@" in search_query:
            return User.objects.filter(email__iexact=search_query)
        else:
            return User.objects.filter(username__icontains=search_query)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "No users found"}, status=status.HTTP_404_NOT_FOUND
            )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FriendRequestRateThrottle(UserRateThrottle):
    rate = '3/min'


class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    # throttle_classes = [FriendRequestRateThrottle]
    permission_classes = [IsAuthenticated]
    
    def get_throttles(self):
        if self.action == 'send_request':
            self.throttle_classes = [FriendRequestRateThrottle]
        return super().get_throttles()

    @action(detail=True, methods=['POST'])
    def send_request(self, request, pk=None):
        if request.user.pk == pk:
            return Response({'error': 'Cannot send friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)

        receiver = User.objects.get(pk=pk)
        friend_request, created = FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver)
        if created:
             return Response({'status': f'Friend request sent to {friend_request.receiver.email}'}, status=status.HTTP_200_OK   )
        else:
             return Response({'status': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            
    @action(detail=True, methods=['POST'])
    def accept_request(self, request, pk=None):
        try:
            sender = User.objects.get(pk=pk)
            friend_request = FriendRequest.objects.get(sender=sender, receiver=request.user, status='sent')
            friend_request.status = 'accepted'
            friend_request.save()
            friend_request.sender.friends.add(friend_request.receiver)
            return Response({'status': f'{sender.email}\'s friend request accepted'}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['POST'])
    def reject_request(self, request, pk=None):
        try:
            sender = User.objects.get(pk=pk)
            friend_request = FriendRequest.objects.get(sender=sender, receiver=request.user, status='sent')
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({'status': f'{sender.email}\'s Friend request rejected'}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
        

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def friends(self, request, pk=None):
        friends = request.user.friends.all()
        if friends.exists():
            serializer = UserSerializer(friends, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No friends found'}, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['get'])
    def pending_requests(self, request, pk=None):
        pending_requests = FriendRequest.objects.filter(receiver=request.user, status='sent')
        if pending_requests.exists():
            serializer = FriendRequestSerializer(pending_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No pending friend requests'}, status=status.HTTP_200_OK)