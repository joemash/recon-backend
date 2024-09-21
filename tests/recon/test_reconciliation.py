import pytest
import csv

from src.recon.utils import (
    CSVFileReader,
    CSVReconciler,
    DataNormalizer,
    ReconciliationEngine,
    RecordComparator,
)


@pytest.fixture
def data_normalizer():
    return DataNormalizer()


@pytest.fixture
def record_comparator():
    return RecordComparator()


@pytest.fixture
def csv_file_reader(data_normalizer):
    return CSVFileReader(data_normalizer)


@pytest.fixture
def reconciliation_engine(record_comparator):
    return ReconciliationEngine(record_comparator)


@pytest.fixture
def csv_reconciler(csv_file_reader, reconciliation_engine):
    return CSVReconciler(
        "source.csv", "target.csv", csv_file_reader, reconciliation_engine
    )


def test_data_normalizer():
    normalizer = DataNormalizer()
    assert normalizer.normalize_value("123") == 123
    assert normalizer.normalize_value("123.45") == 123.45
    assert normalizer.normalize_value("2022-01-01") == "2022-01-01"
    assert normalizer.normalize_value("hello") == "hello"


def test_record_comparator():
    comparator = RecordComparator()
    source_record = {"ID": 1, "Name": "John Doe", "Date": "2023-01-01", "Amount": 100}
    target_record = {"ID": 1, "Name": "John Doe", "Date": "2023-01-01", "Amount": 100}
    common_columns = ["ID", "Name", "Date", "Amount"]
    discrepancies = comparator.compare_records(
        source_record, target_record, common_columns
    )
    assert discrepancies == {}


def test_csv_file_reader(tmp_path, data_normalizer):
    source_file_path = tmp_path / "source.csv"
    target_file_path = tmp_path / "target.csv"
    with open(source_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Date", "Amount"])
        writer.writerow(["1", "John Doe", "2023-01-01", "100"])
        writer.writerow(["2", "Jane Smith", "2023-01-02", "200.5"])
        writer.writerow(["3", "Robert Brown", "2023-01-03", "300.75"])
    with open(target_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Date", "Amount"])
        writer.writerow(["1", "John Doe", "2023-01-01", "100"])
        writer.writerow(["2", "Jane Smith", "2023-01-04", "200.5"])
        writer.writerow(["4", "Emily White", "2023-01-05", "400.9"])
    csv_file_reader = CSVFileReader(data_normalizer)
    source_data, source_columns, source_error = csv_file_reader.read(
        str(source_file_path)
    )
    target_data, target_columns, target_error = csv_file_reader.read(
        str(target_file_path)
    )
    assert source_data == [
        {"ID": 1, "Name": "John Doe", "Date": "2023-01-01", "Amount": 100},
        {"ID": 2, "Name": "Jane Smith", "Date": "2023-01-02", "Amount": 200.5},
        {"ID": 3, "Name": "Robert Brown", "Date": "2023-01-03", "Amount": 300.75},
    ]
    assert target_data == [
        {"ID": 1, "Name": "John Doe", "Date": "2023-01-01", "Amount": 100},
        {"ID": 2, "Name": "Jane Smith", "Date": "2023-01-04", "Amount": 200.5},
        {"ID": 4, "Name": "Emily White", "Date": "2023-01-05", "Amount": 400.9},
    ]
    assert source_columns == ["ID", "Name", "Date", "Amount"]
    assert target_columns == ["ID", "Name", "Date", "Amount"]
    assert source_error == ""
    assert target_error == ""


def test_reconciliation_engine(record_comparator):
    source_data = [
        {"ID": 1, "Name": "John Doe", "Date": "2023-01-01", "Amount": 100},
        {"ID": 2, "Name": "Jane Smith", "Date": "2023-01-02", "Amount": 200.5},
        {"ID": 3, "Name": "Robert Brown", "Date": "2023-01-03", "Amount": 300.75},
    ]
    target_data = [
        {"ID": 1, "Name": "John Doe", "Date": "2023-01-01", "Amount": 100},
        {"ID": 2, "Name": "Jane Smith", "Date": "2023-01-04", "Amount": 200.5},
        {"ID": 4, "Name": "Emily White", "Date": "2023-01-05", "Amount": 400.9},
    ]
    common_columns = ["ID", "Name", "Date", "Amount"]
    engine = ReconciliationEngine(record_comparator)
    result = engine.reconcile(source_data, target_data, common_columns)
    assert result == {
        "reconciled": [
            {
                "source": {
                    "ID": 1,
                    "Name": "John Doe",
                    "Date": "2023-01-01",
                    "Amount": 100,
                },
                "target": {
                    "ID": 1,
                    "Name": "John Doe",
                    "Date": "2023-01-01",
                    "Amount": 100,
                },
            }
        ],
        "missing_in_target": [
            {
                "ID": 3,
                "Name": "Robert Brown",
                "Date": "2023-01-03",
                "Amount": 300.75,
                "source": True,
                "target": None,
            }
        ],
        "missing_in_source": [
            {
                "ID": 4,
                "Name": "Emily White",
                "Date": "2023-01-05",
                "Amount": 400.9,
                "source": None,
                "target": True,
            }
        ],
        "discrepancies": [
            {
                "source": {
                    "ID": 2,
                    "Name": "Jane Smith",
                    "Date": "2023-01-02",
                    "Amount": 200.5,
                },
                "target": {
                    "ID": 2,
                    "Name": "Jane Smith",
                    "Date": "2023-01-04",
                    "Amount": 200.5,
                },
                "fields_with_discrepancies": {
                    "Date": {"source": "2023-01-02", "target": "2023-01-04"}
                },
            }
        ],
    }


def test_csv_reconciler(csv_reconciler, tmp_path):
    source_file_path = tmp_path / "source.csv"
    target_file_path = tmp_path / "target.csv"
    with open(source_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Date", "Amount"])
        writer.writerow(["1", "John Doe", "2023-01-01", "100"])
        writer.writerow(["2", "Jane Smith", "2023-01-02", "200.5"])
        writer.writerow(["3", "Robert Brown", "2023-01-03", "300.75"])
    with open(target_file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Date", "Amount"])
        writer.writerow(["1", "John Doe", "2023-01-01", "100"])
        writer.writerow(["2", "Jane Smith", "2023-01-04", "200.5"])
        writer.writerow(["4", "Emily White", "2023-01-05", "400.9"])
    csv_reconciler.source_file = str(source_file_path)
    csv_reconciler.target_file = str(target_file_path)
    result = csv_reconciler.reconcile()
    assert result == {
        "reconciled": [
            {
                "source": {
                    "ID": 1,
                    "Name": "John Doe",
                    "Date": "2023-01-01",
                    "Amount": 100,
                },
                "target": {
                    "ID": 1,
                    "Name": "John Doe",
                    "Date": "2023-01-01",
                    "Amount": 100,
                },
            }
        ],
        "missing_in_target": [
            {
                "ID": 3,
                "Name": "Robert Brown",
                "Date": "2023-01-03",
                "Amount": 300.75,
                "source": True,
                "target": None,
            }
        ],
        "missing_in_source": [
            {
                "ID": 4,
                "Name": "Emily White",
                "Date": "2023-01-05",
                "Amount": 400.9,
                "source": None,
                "target": True,
            }
        ],
        "discrepancies": [
            {
                "source": {
                    "ID": 2,
                    "Name": "Jane Smith",
                    "Date": "2023-01-02",
                    "Amount": 200.5,
                },
                "target": {
                    "ID": 2,
                    "Name": "Jane Smith",
                    "Date": "2023-01-04",
                    "Amount": 200.5,
                },
                "fields_with_discrepancies": {
                    "Date": {"source": "2023-01-02", "target": "2023-01-04"}
                },
            }
        ],
    }
