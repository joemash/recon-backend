from rest_framework import status
from rest_framework.response import Response

from src.account.serializers.signup import ChangePasswordSerializer
from src.account.usecases.change_password import change_password
from src.common.utils.helpers import format_error_response
from src.common.views.base import BaseViewSet


class ChangePasswordViewSet(BaseViewSet):
    serializer_class = ChangePasswordSerializer
    http_method_names = ["post", "options"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            data, status_code = format_error_response(
                message=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        result, status_code = change_password(request.user, **serializer.validated_data)
        if not result.get("user"):
            return Response(result, status=status_code)

        return Response({}, status=status_code)
