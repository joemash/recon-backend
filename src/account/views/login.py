from django.contrib.auth import get_user_model, login
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.account.serializers.login import LoginSerializer
from src.account.serializers.token import UserLoginResponseSerializer
from src.account.usecases.login import authenticate_user
from src.common.utils.helpers import format_error_response

UserModel = get_user_model()


class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        data, status_code = authenticate_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )

        user = data.get("user")
        if not isinstance(user, UserModel):
            return Response(data, status=status_code)

        login(request, user)

        serialized_data = UserLoginResponseSerializer(data).data
        return Response(serialized_data, status=status_code)
