from django.db import models

from src.common.models.abstract import AbstractBase
from src.common.utils.constants import CONTENT_TYPES


def upload_to(instance, filename):
    return f"{instance.created.strftime('%Y/%m/%d')}/{instance.id}_{filename}"


class Attachments(AbstractBase):
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPES)
    uploaded_file = models.FileField(upload_to=upload_to, max_length=500)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    size = models.IntegerField(
        help_text="The size of the attachment in bytes", null=True, blank=True
    )
    organisation = None

    def __str__(self):
        return self.title
