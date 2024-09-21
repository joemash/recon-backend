import os
import pytest
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import TemporaryUploadedFile

from src.recon.models import ReconciliationResult


@pytest.fixture
def source_file():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{}/assets/source.csv".format(cur_dir)
    with open(filename, "rb") as file:
        file_contents = file.read()
        temp_file = TemporaryUploadedFile(
            file.name, len(file_contents), "text/csv", "utf-8"
        )
        temp_file.write(file_contents)
        temp_file.seek(0)  # rewind the file pointer
        return temp_file


@pytest.fixture
def target_file():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    filename = "{}/assets/target.csv".format(cur_dir)
    with open(filename, "rb") as file:
        file_contents = file.read()
        temp_file = TemporaryUploadedFile(
            file.name, len(file_contents), "text/csv", "utf-8"
        )
        temp_file.write(file_contents)
        temp_file.seek(0)  # rewind the file pointer
        return temp_file


def test_reconcile_view(client, source_file, target_file):
    url = reverse("v1:reconciliation-reconcile")

    response = client.post(
        url,
        {"source_file": source_file, "target_file": target_file},
        format="multipart",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert ReconciliationResult.objects.count() == 1
    assert response.data["results"] == {
        "reconciled": [
            {
                "source": {
                    "ID": 1,
                    "Name": "John Doe",
                    "Date": "2023-01-01",
                    "Amount": 100.0,
                },
                "target": {
                    "ID": 1,
                    "Name": "John Doe",
                    "Date": "2023-01-01",
                    "Amount": 100.0,
                },
            }
        ],
        "missing_in_target": [
            {
                "ID": 4,
                "Name": "Emily White",
                "Date": "2023-01-05",
                "Amount": 400.9,
                "source": True,
                "target": None,
            }
        ],
        "missing_in_source": [
            {
                "ID": 3,
                "Name": "Robert Brown",
                "Date": "2023-01-03",
                "Amount": 300.75,
                "source": None,
                "target": True,
            }
        ],
        "discrepancies": [
            {
                "source": {
                    "ID": 2,
                    "Name": "Jane Smith",
                    "Date": "2023-01-04",
                    "Amount": 200.5,
                },
                "target": {
                    "ID": 2,
                    "Name": "Jane Smith",
                    "Date": "2023-01-02",
                    "Amount": 200.5,
                },
                "fields_with_discrepancies": {
                    "Date": {"source": "2023-01-04", "target": "2023-01-02"}
                },
            }
        ],
    }


def test_reconcile_view_missing_files(client):
    url = reverse("v1:reconciliation-reconcile")
    response = client.post(url, {}, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.data.get("detail") == "source_file: No file was submitted. target_file: No file was submitted."
    )


def test_reconcile_view_invalid_files(client, source_file):
    url = reverse("v1:reconciliation-reconcile")
    response = client.post(
        url,
        {"source_file": source_file, "target_file": "invalid file"},
        format="multipart",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        response.data.get("detail") == "target_file: The submitted data was not a file. Check the encoding type on the form."
    )
