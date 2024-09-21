import logging

from storages.backends.s3boto3 import S3Boto3Storage


LOGGER = logging.getLogger(__name__)


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False
