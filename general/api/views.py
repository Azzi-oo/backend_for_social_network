from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from general.api.serializers import UserRegistrationSerializer, UserListSerilizer
from general.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserViewSet(
    CreateModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserRegistrationSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        return UserListSerilizer
    
    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()