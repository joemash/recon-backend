from rest_framework import serializers

from src.account.models.user import User
from src.common.utils.error_codes import ErrorCodes


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(ErrorCodes.EMAIL_EXISTS.value)
        return data


class RegistrationResponseSerializer(serializers.Serializer):
    user_id = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255)
    new_password = serializers.CharField(max_length=255)
