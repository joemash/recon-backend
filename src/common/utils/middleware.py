import logging

from django.utils.deprecation import MiddlewareMixin

from src.common.models.organisation import Organisation


LOGGER = logging.getLogger(__name__)


class OrganisationIDMiddleware(MiddlewareMixin):
    """
    Extract the current Organisation-ID from the request
    headers and attach it to the request object.
    """

    def process_request(self, request):
        organisation_id = request.headers.get("Organisation-ID")
        if not organisation_id:
            request.organisation_id = None

        request.organisation_id = organisation_id
        try:
            request.organisation = Organisation.objects.get(id=organisation_id)
        except Organisation.DoesNotExist:
            LOGGER.info(f"organisation id {organisation_id} not found", exc_info=True)
            request.organisation = None
