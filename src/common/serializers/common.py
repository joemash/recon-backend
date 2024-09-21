import magic
from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        pass


class AttachmentsUploadSerializer(serializers.Serializer):
    attachment = serializers.FileField()

    def validate(self, data):
        data = super().validate(data)
        attachment = data["attachment"]
        allowed_mime_types = {"application/pdf", "image/png", "image/jpeg"}
        attachment_mime_type = magic.from_buffer(attachment.read(1023), mime=True)
        if attachment_mime_type not in allowed_mime_types:
            raise serializers.ValidationError(
                "Invalid attachment uploaded. Attachment can either be a PDF, "
                "PNG or JPEG."
            )

        data["content_type"] = attachment_mime_type
        return data
