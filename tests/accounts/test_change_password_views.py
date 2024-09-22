import pytest
from django.urls import reverse
from rest_framework import status

from src.common.utils.error_codes import ErrorCodes


class TestChangePasswordViews:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self, client):
        self.client = client
        self.url = reverse("v1:change-password-list")

    def test_user_can_successfully_change_their_password(self):
        old_password = "abc@123"
        new_password = "recon@100"
        data = {
            "password": old_password,
            "new_password": new_password,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        # Using the old password should not work
        payload = {
            "email": "mail@mail.com",
            "password": old_password,
        }
        url = reverse("v1:token_obtain_pair")
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == ErrorCodes.INCORRECT_LOGIN_CREDENTIALS.value
        # The new password should work
        payload.update({"password": new_password})
        response = self.client.post(url, payload)
        assert response.status_code == status.HTTP_200_OK

    def test_when_the_current_password_supplied_is_wrong(self):
        old_password = "wrong-pass"
        new_password = "recon@100"
        data = {
            "password": old_password,
            "new_password": new_password,
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Your current password is wrong."

    def test_when_required_params_not_supplied(self):
        data = {
            "password": "mwas",
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "new_password: This field is required."
