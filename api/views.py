from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated

class UserSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('q', '')
        if '@' in search_query:  # Search by email
            return User.objects.filter(email__iexact=search_query)
        else:  # Search by name
            return User.objects.filter(username__icontains=search_query)