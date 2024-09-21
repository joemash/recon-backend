from enum import Enum


class ErrorCodes(Enum):
    # Organized alphabetically for ease of access when reading and use snake case.
    EMAIL_EXISTS = "Email already exists."
    INCORRECT_LOGIN_CREDENTIALS = (
        "The email and password combination is invalid or the user is inactive."
    )
    INVALID_PHONE_NUMBER = "Phone number provided is invalid."
    INVALID_SCHEDULE_OPTION = "Only one scheduling option should be chosen."
    INVALID_WEEK_DAY = (
        "For EVERY_WEEK_DAY, `week_day` must be between 0 (Monday) and 4 (Friday)."
    )
    MISSING_EMAIL = "Email is required."
    PHONE_NUMBER_EXISTS = "Phone number already exists."
    SKIP_DAY_REQUIRED = "`skip_days` must be provided for SKIP_DAYS option."
    WEEK_DAY_REQUIRED = "`week_day` must be provided for WEEKLY option."
    WRONG_PASSWORD = "Your current password is wrong."
    USER_ALREADY_A_MEMBER = "This user is already a member in this department."
    USER_SIGNUP_NEEDED = "This user does not have an account in the system."
    PROFILE_MISMATCH = "This profile supplied does not belong to this user."
    ORGANISATION_NAME_EXIST = "This organisation name already exists."
    ORGANISATION_EMAIL_EXISTS = "Organisation email already exists."
    ORGANISATION_PHONE_EXISTS = "Organisation phone number already exists."
