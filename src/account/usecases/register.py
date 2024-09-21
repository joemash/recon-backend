from http import HTTPStatus

from django.db import transaction

from src.account.models.user import User


@transaction.atomic
def register_user(registration_data):
    password = registration_data["password"]
    email = registration_data["email"]
    userdata = {"username": email}
    user = User.objects.create_user(email=email, password=password, **userdata)
    response_data = {"user_id": user.id}
    return response_data, HTTPStatus.CREATED
