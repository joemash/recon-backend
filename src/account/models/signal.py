import logging

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

LOGGER = logging.getLogger(__name__)


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # TODO send via email
    LOGGER.info(f"{reset_password_token.key}")
