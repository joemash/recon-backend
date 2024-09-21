import os

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from src.common.models.attachment import Attachments, upload_to
from src.common.serializers.common import AttachmentsUploadSerializer


class TestAttachmentsModel(TestCase):

    def test_upload_path_is_correctly_set(self):
        att = baker.make(Attachments, title="Shifts Data", _create_files=True)
        path = upload_to(att, "shifts_data.xls")
        created = att.created
        assert path == "{year}/{month}/{day}/{att_id}_{filename}".format(
            year=created.strftime("%Y"),
            month=created.strftime("%m"),
            day=created.strftime("%d"),
            att_id=att.id,
            filename="shifts_data.xls",
        )
        att.uploaded_file.delete(save=False)

    def test_str_representation(self):
        att = baker.make(Attachments, title="User Invites", _create_files=True)
        assert str(att) == "User Invites"
        att.uploaded_file.delete(save=False)


class AttachmentsUploadSerializerTests(TestCase):

    def test_attachment_with_valid_mime_type(self):
        pdf_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets/dummy.pdf")
        )
        with open(pdf_file, "rb") as f:
            pdf = File(f)
            upload_file = SimpleUploadedFile("dummy.pdf", pdf.read())

        data = {"attachment": upload_file}
        ser = AttachmentsUploadSerializer(data=data)
        ser.is_valid(raise_exception=True)
        assert ser.validated_data["content_type"] == "application/pdf"

    def test_attachment_with_invalid_mime_type(self):
        upload_file = SimpleUploadedFile("dummy.pdf", b"Some text")
        data = {"attachment": upload_file}
        ser = AttachmentsUploadSerializer(data=data)
        err_msg = (
            "Invalid attachment uploaded. Attachment can either be a PDF, "
            "PNG or JPEG."
        )
        with self.assertRaisesMessage(ValidationError, err_msg):
            ser.is_valid(raise_exception=True)
