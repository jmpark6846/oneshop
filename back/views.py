from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from accounts.models import User
from back.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]