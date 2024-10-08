from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from src.common.utils.helpers import format_error_response
from src.common.views.base import BaseViewSet
from src.recon.models import ReconciiationStatuses, ReconciliationResult
from src.recon.serializers import (
    ReconciliationResponseSerializer,
    ReconciliationSerializer,
    ReconciliationUploadSerializer,
)
from src.recon.utils import CSVReconciler


class ReconciliationViewSet(BaseViewSet):
    queryset = ReconciliationResult.objects.all()
    serializer_class = ReconciliationSerializer
    http_method_names = ["get", "post", "options"]

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def reconcile(self, request):
        serializer = ReconciliationUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        attachment_data = {
            "source_file": validated_data["target_file"],
            "target_file": validated_data["source_file"],
        }
        attachment = self.queryset.create(**attachment_data)

        source_path = attachment.source_file.file.name
        target_path = attachment.target_file.file.name

        csv_reconciler = CSVReconciler(source_path, target_path)
        result = csv_reconciler.reconcile()

        errors = result.get("errors")
        if errors:
            data, status_code = format_error_response(
                message=errors,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
            return Response(data, status=status_code)

        attachment.result = result
        attachment.status = ReconciiationStatuses.PROCESSED
        attachment.save()

        data = {
            "id": attachment.id,
            "created": attachment.created_at,
            "status": attachment.status.capitalize(),
            "results": result
        }
        serializer_response = ReconciliationResponseSerializer(data)
        return Response(serializer_response.data, status=status.HTTP_201_CREATED)
