import pytest
from django.urls import reverse
from rest_framework import status

from src.account.models.user import User
from src.common.utils.error_codes import ErrorCodes

pytestmark = pytest.mark.django_db


class TestRegisterUserView:
    def setup_method(self):
        self.payload = {
            "email": "zakayo@gmail.com",
            "password": "recon@403",
        }
        self.url = reverse("v1:register-list")

    def test_can_register_user_successfully(self, unauthenticated_client):
        assert User.objects.count() == 0

        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.get(email="zakayo@gmail.com")
        assert User.objects.count() == 1

    def test_when_creating_the_same_user_then_it_returns_an_error(
        self, unauthenticated_client
    ):
        assert User.objects.count() == 0

        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1

        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["detail"] == f"non_field_errors: {ErrorCodes.EMAIL_EXISTS.value}"
        )
        assert User.objects.count() == 1

    def test_when_email_is_missing_then_an_error_is_returned(
        self, unauthenticated_client
    ):
        assert User.objects.count() == 0

        self.payload.pop("email")
        response = unauthenticated_client.post(self.url, self.payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "email: This field is required."
        assert User.objects.count() == 0
