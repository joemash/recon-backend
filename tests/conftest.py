import pytest

from pytest import fixture
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


from tests.helpers import (
    create_test_user,
)

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def user():
    return create_test_user()


@fixture
def unauthenticated_client():
    """Use this for APIs that don't require an authentication."""
    client = APIClient()
    return client


@pytest.fixture
def client(user):
    """Use this for all APIs that require an ORG header and an authentication."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
    return client
