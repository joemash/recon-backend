from http import HTTPStatus

from django.db import transaction

from src.account.models.user import User
from src.common.utils.error_codes import ErrorCodes
from src.common.utils.helpers import format_error_response


@transaction.atomic
def change_password(user, **data):
    current_password = data.get("password")
    new_password = data.get("new_password")

    user = User.objects.change_password(user, current_password, new_password)
    if not user:
        return format_error_response(
            message=ErrorCodes.WRONG_PASSWORD.value, status_code=HTTPStatus.BAD_REQUEST
        )
    return {"user": user}, HTTPStatus.OK
