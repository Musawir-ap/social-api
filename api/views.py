from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password'])
        user.email = request.data['email'].lower()
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data})
        
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user) 
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
   
   
class UserSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        if '@' in search_query:
            return User.objects.filter(email__iexact=search_query)
        else:
            return User.objects.filter(username__icontains=search_query)