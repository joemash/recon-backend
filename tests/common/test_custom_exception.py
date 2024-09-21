from http import HTTPStatus

import jwt
from django.core.exceptions import (
    ImproperlyConfigured,
    MultipleObjectsReturned,
    ObjectDoesNotExist,
    ValidationError,
)
from django.db.utils import DatabaseError
from rest_framework import status
from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError as DRFValidationError,
    ParseError,
)
from rest_framework.test import APITestCase
from rest_framework_simplejwt.exceptions import InvalidToken


from src.common.utils.exception_handler import custom_exception_handler


class TestCustomExceptionHandlerTestCase(APITestCase):

    def test_object_not_exist_error_is_handled(self):
        v = ObjectDoesNotExist("object does not exist")
        res = custom_exception_handler(v, {})
        self.assertEqual(res.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(res.status_text, "Not Found")
        self.assertEqual(res.data, {"detail": "object does not exist"})

    def test_a_user_validation_error_for_non_fields_is_handled(self):
        context = {"view": "An API view"}
        v = ValidationError("required field not supplied")
        response = custom_exception_handler(v, context)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.status_text, "Bad Request")
        self.assertEqual(response.data, {"detail": ["required field not supplied"]})

    def test_error_with_field_names_is_handled(self):
        context = {"view": "API view"}
        v = ValidationError({"name": "missing name"})
        response = custom_exception_handler(v, context)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.status_text, "Bad Request")
        self.assertEqual(response.data, {"name": ["missing name"]})

    def test_validation_error_with_field_name_and_arrays_is_handled(self):
        context = {"view": "API view"}
        v = ValidationError({"contacts": ["wrong data", "invalid"]})
        response = custom_exception_handler(v, context)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.status_text, "Bad Request")
        self.assertEqual(response.data, {"contacts": ["wrong data", "invalid"]})

    def test_errors_handled_by_drf(self):
        exc = PermissionDenied("You do not have permission to perform this action.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        self.assertEqual(
            response.data,
            {"detail": "You do not have permission to perform this action."},
        )

    def test_unauthenticated_exception_handler(self):
        exc = NotAuthenticated("unauthenticated.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {"detail": "unauthenticated."},
        )

    def test_random_exception(self):
        exc = Exception("internal server error.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.data,
            {"detail": "internal server error."},
        )

    def test_method_not_allowed(self):
        exc = MethodNotAllowed("post")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            response.data,
            {"detail": 'Method "post" not allowed.'},
        )

    def test_multiple_objects_returned(self):
        exc = MultipleObjectsReturned("returned more than one object.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data,
            {"detail": "returned more than one object."},
        )

    def test_improperly_configured(self):
        exc = ImproperlyConfigured("invalid.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "invalid."},
        )

    def test_invalid_token(self):
        exc = InvalidToken("Token is invalid or expired")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "Token is invalid or expired"},
        )

    def test_expired_invitation_signature_error(self):
        exc = jwt.ExpiredSignatureError("The invitation token has expired")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "The invitation token has expired"},
        )

    def test_invalid_invitation_token(self):
        exc = jwt.InvalidTokenError("The invitation token is invalid")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "The invitation token is invalid"},
        )

    def test_django_database_errors(self):
        exc = DatabaseError("internal server error.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            response.data,
            {"detail": "internal server error."},
        )

    def test_unhandled_exceptions(self):
        context = {"view": "API view"}
        response = custom_exception_handler(None, context)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(
            response.data,
            {"detail": "Sorry, we are currently having a system issue."},
        )

    def test_drf_validation_and_parse_exceptions(self):
        exc = DRFValidationError(
            "email: We couldn't find an account associated with that email."
        )
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        exc = ParseError("unable to parse error.")
        context = {"view": "API view"}
        response = custom_exception_handler(exc, context)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
