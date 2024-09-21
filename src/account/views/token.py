from rest_framework_simplejwt.views import TokenRefreshView

from src.account.serializers.token import CustomTokenRefreshSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer
