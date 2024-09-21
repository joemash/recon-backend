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


def assertListEqual(a, b):
    assert len(a) == len(b) and sorted(a) == sorted(b)


def sorted_dict_values(d):
    return {k: sorted(v) for k, v in d.items()}
