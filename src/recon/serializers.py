import magic
from rest_framework import serializers

from src.common.serializers.common import BaseModelSerializer
from src.recon.models import ReconciliationResult


class ReconciliationSerializer(BaseModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.status.capitalize()

    class Meta:
        model = ReconciliationResult
        exclude = [
            "created",
            "updated",
            "active",
            "created_by",
            "updated_by",
            "deleted_at",
            "source_file",
            "target_file",
        ]


class ReconciliationResultSerializer(serializers.Serializer):
    reconciled = serializers.ListField(child=serializers.DictField())
    missing_in_target = serializers.ListField(child=serializers.DictField())
    missing_in_source = serializers.ListField(child=serializers.DictField())
    discrepancies = serializers.ListField(child=serializers.DictField())


class ReconciliationResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    created = serializers.DateTimeField(required=True, format="%Y-%m-%d")
    results = ReconciliationResultSerializer()


def validate_csv(data):
    mime_type = magic.from_buffer(data.read(1024), mime=True)
    if mime_type not in ["text/csv", "text/plain"]:
        raise serializers.ValidationError("Not a CSV file")


class ReconciliationUploadSerializer(serializers.Serializer):
    source_file = serializers.FileField(validators=[validate_csv])
    target_file = serializers.FileField(validators=[validate_csv])
