from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import CustomUser
from .serializers import UserRegistrationSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerializer
        return UserRegistrationSerializer  # TODO Change for new serializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]