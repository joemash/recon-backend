import pytest

from src.account.models.user import User


pytestmark = pytest.mark.django_db


def create_test_user(
    username="mail@mail.com", email="mail@mail.com", is_active=True, password="abc@123"
):
    user = User.objects.create(username=username, email=email, is_active=is_active)
    user.set_password(password)
    user.save()
    return user

