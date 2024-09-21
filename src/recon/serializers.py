import magic
from rest_framework import serializers


class ReconciliationResponseSerializer(serializers.Serializer):
    reconciled = serializers.ListField(child=serializers.DictField())
    missing_in_target = serializers.ListField(child=serializers.DictField())
    missing_in_source = serializers.ListField(child=serializers.DictField())
    discrepancies = serializers.ListField(child=serializers.DictField())


def validate_csv(data):
    mime_type = magic.from_buffer(data.read(1024), mime=True)
    if mime_type not in ["text/csv", "text/plain"]:
        raise serializers.ValidationError("Not a CSV file")


class ReconciliationUploadSerializer(serializers.Serializer):
    source_file = serializers.FileField(validators=[validate_csv])
    target_file = serializers.FileField(validators=[validate_csv])
