from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from src.account.models.user import User
from src.account.serializers.login import UserResponseSerializer


class LoginTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=False, allow_null=True)
    refresh_token = serializers.CharField(required=False, allow_null=True)
    token_type = serializers.CharField()


class UserLoginResponseSerializer(serializers.Serializer):
    user = UserResponseSerializer()
    token = LoginTokenResponseSerializer()


class CustomTokenRefreshResponseSerializer(serializers.Serializer):
    token = serializers.CharField()


class CustomObtainTokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    token_type = serializers.CharField()
    expires_in = serializers.IntegerField()


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs["refresh"])

        user_id = refresh["user_id"]
        user = User.objects.get(id=user_id)

        expiry = timezone.now() + timedelta(
            seconds=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
        )
        access_token = refresh.access_token
        access_token["user_id"] = str(user.id)
        access_token["iat"] = int(timezone.now().timestamp() * 1000)
        access_token["exp"] = expiry

        data["expires_in"] = expiry
        data["expires_at"] = int(
            refresh.access_token.payload["exp"] - timezone.now().timestamp()
        )
        data["access_token"] = str(access_token)
        return {"token": str(access_token)}
