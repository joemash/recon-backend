import pytest
from django.urls import reverse
from rest_framework import status

from src.account.models.user import User
from src.common.utils.error_codes import ErrorCodes

pytestmark = pytest.mark.django_db


class TestLoginUserView:
    def setup_method(self):
        self.payload = {
            "email": "mail@mail.com",
            "password": "abc@123",
            "fcm_token": "",
            "is_mobile_platform": False,
        }
        self.url = reverse("v1:login-list")

    def test_a_user_can_login_successfully(self, unauthenticated_client, user):
        assert User.objects.count() == 1
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["token"]["access_token"]

    def test_when_a_user_uses_wrong_credentials_then_an_error_is_returned(
        self, unauthenticated_client, user
    ):
        assert User.objects.count() == 1
        self.payload["password"] = "invalid"
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == ErrorCodes.INCORRECT_LOGIN_CREDENTIALS.value

    def test_when_a_user_submits_missing_data_then_an_error_is_returned(
        self, unauthenticated_client, user
    ):
        assert User.objects.count() == 1
        self.payload["email"] = ""
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "email: This field may not be blank."
