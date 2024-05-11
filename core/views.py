from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .models import User
from .serializers import UserRegistrationSerailizer


class UserViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegistrationSerailizer
        return UserRegistrationSerailizer  # TODO Change for new serializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]