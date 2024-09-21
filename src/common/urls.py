from rest_framework.routers import DefaultRouter

from src.common.views.industries import IndustryViewSet
from src.common.views.organisation import (
    OrganisationAttachmentViewSet,
    OrganisationCreateViewSet,
    OrganisationSimpleAttachmentViewSet,
    OrganisationViewSet,
)
from src.common.views.profile import (
    IndividualViewSet,
    UserProfileAttachmentViewSet,
    UserProfileViewSet,
)

profiles_router = DefaultRouter()
profiles_router.register(r"profile", UserProfileViewSet)
profiles_router.register(r"person", IndividualViewSet)
profiles_router.register(r"attachments", UserProfileAttachmentViewSet)

organisation_router = DefaultRouter()
organisation_router.register(r"organisation", OrganisationViewSet)
organisation_router.register(
    r"create", OrganisationCreateViewSet, basename="organisation_create"
)
organisation_router.register(r"attachments", OrganisationAttachmentViewSet)
organisation_router.register(
    r"attachment-simple",
    OrganisationSimpleAttachmentViewSet,
    basename="attchment_simple",
)

industry_router = DefaultRouter()
industry_router.register(r"industry", IndustryViewSet, basename="industries")
