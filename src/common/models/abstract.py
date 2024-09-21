import uuid

from django.db import models
from django.utils import timezone


class AbstractBase(models.Model):
    """Base class for most models in the application."""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, null=False)
    created_by = models.UUIDField(blank=True, null=True)
    updated = models.DateTimeField(default=timezone.now)
    updated_by = models.UUIDField(blank=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ("-updated", "-created")
