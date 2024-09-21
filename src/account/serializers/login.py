from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
