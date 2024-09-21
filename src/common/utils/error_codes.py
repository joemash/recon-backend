from enum import Enum


class ErrorCodes(Enum):
    EMAIL_EXISTS = "Email already exists."
    INCORRECT_LOGIN_CREDENTIALS = (
        "The email and password combination is invalid or the user is inactive."
    )
    WRONG_PASSWORD = "Your current password is wrong."
