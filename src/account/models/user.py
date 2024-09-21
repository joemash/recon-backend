import logging

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

LOGGER = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):

    def change_password(self, user, current_password, password):
        user = self.get(id=user.id)
        if not user.check_password(current_password):
            return None

        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_verified = True
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        user = self.create_user(email=email, password=password, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    This represents a logged in user into the system.
    """

    email = models.EmailField(_("email address"), unique=True, db_index=True)
    is_suspended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
