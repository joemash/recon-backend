from enum import Enum


class ErrorCodes(Enum):
    EMAIL_EXISTS = "Email already exists."
    INCORRECT_LOGIN_CREDENTIALS = (
        "No active account found with the given credentials"
    )
    WRONG_PASSWORD = "Your current password is wrong."
