from django.db.transaction import atomic

from src.common.models.attachment import Attachments
from src.common.models.profile import (
    UserProfile,
    UserProfileAttachment,
    UserProfileStatus,
)


@atomic
def create_profile_attachment(validated_data, user):
    default_data = {"created_by": user.id, "updated_by": user.id}

    attachment = Attachments.objects.create(
        content_type=validated_data["content_type"],
        uploaded_file=validated_data["attachment"],
        title=validated_data["attachment"].name,
        size=validated_data["attachment"].size,
        description=validated_data.get("description"),
        **default_data
    )

    profile_attachment_data = {
        "profile": validated_data.get("profile"),
        "attachment": attachment,
        "attachment_type": validated_data.get("attachment_type"),
    }
    profile_attachment_data.update(default_data)
    return UserProfileAttachment.objects.create(**profile_attachment_data)


@atomic
def handle_professional_details(user, individual, valid_data):
    professional_details = valid_data["profession_details"]
    profile_defaults = {
        "user": user,
        "individual": individual,
        "status": UserProfileStatus.PROFESSIONAL_DETAILS,
        "profession_details": professional_details,
    }

    profile, _ = UserProfile.objects.update_or_create(
        profession_name=valid_data["profession_name"], defaults=profile_defaults
    )
    return profile
