import logging

import jwt
from django.core import exceptions
from django.db.utils import (
    DatabaseError,
    DataError,
    Error,
    IntegrityError,
    InterfaceError,
    InternalError,
    NotSupportedError,
    OperationalError,
    ProgrammingError,
)
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, MethodNotAllowed, NotAuthenticated, ParseError
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework_simplejwt.exceptions import InvalidToken


from src.common.utils.helpers import format_error_response

LOGGER = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    A custom exception handler for Django REST framework.
    Used to handle raised exceptions that are raised by the app.

    """
    LOGGER.error(
        f"Internal API Error: {exc}",
        extra={"exception": exc, "context": context},
        exc_info=True,
    )
    if isinstance(exc, exceptions.ValidationError):
        try:
            data = exc.message_dict
        except AttributeError:
            data = {"detail": exc.messages}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, (exceptions.PermissionDenied, DRFPermissionDenied)):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, DRFValidationError):
        data, status_code = format_error_response(
            message=exc.detail, status_code=status.HTTP_400_BAD_REQUEST
        )
        return Response(data, status=status_code)

    if isinstance(exc, ParseError):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, MethodNotAllowed):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if isinstance(exc, NotAuthenticated):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, (exceptions.ObjectDoesNotExist, Http404)):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if isinstance(
        exc,
        (
            KeyError,
            IndexError,
        ),
    ):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, exceptions.MultipleObjectsReturned):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_409_CONFLICT)

    if isinstance(exc, exceptions.ImproperlyConfigured):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, InvalidToken):
        data = {"detail": "Token is invalid or expired"}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, AuthenticationFailed):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)

    if isinstance(exc, jwt.ExpiredSignatureError):
        data = {"detail": "The invitation token has expired"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, jwt.InvalidTokenError):
        data = {"detail": "The invitation token is invalid"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(
        exc,
        (
            IntegrityError,
            Error,
            DatabaseError,
            DataError,
            OperationalError,
            InternalError,
            ProgrammingError,
            NotSupportedError,
            InterfaceError,
        ),
    ):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_409_CONFLICT)

    if isinstance(exc, Exception):
        data = {"detail": str(exc)}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = exception_handler(exc, context)
    if not response:
        msg = "Sorry, we are currently having a system issue."
        data = {"detail": msg}
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
