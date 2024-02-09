from rest_framework import generics, viewsets
from rest_framework.response import Response
from account.permissions import IsStaff
from .serializer import (
    RegisterSerializer,
    UserSerializer,
    UserSerializerRegisterResponse,
)
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterUserApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "success": True,
                "data": UserSerializerRegisterResponse(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


class UserApi(viewsets.ModelViewSet):
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = (IsStaff,)

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
