from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.account.serializers.signup import (
    RegistrationResponseSerializer,
    RegistrationSerializer,
)
from src.account.usecases.register import register_user
from src.common.utils.helpers import format_error_response


class RegisterUserViewSet(viewsets.ViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        result, status_code = register_user(serializer.validated_data)
        user_id = result.get("user_id")
        if not user_id:
            return Response(result, status=status_code)

        serialized_data = RegistrationResponseSerializer(result).data
        return Response(serialized_data, status=status_code)
