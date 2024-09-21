from django.db import models

from src.common.models.abstract import AbstractBase


def upload_to(instance, filename):
    return f"{instance.created.strftime('%Y/%m/%d')}/{instance.id}_{filename}"


class ReconciliationResult(AbstractBase):
    source_file = models.FileField(upload_to=upload_to)
    target_file = models.FileField(upload_to=upload_to)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
