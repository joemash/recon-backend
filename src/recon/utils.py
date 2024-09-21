import csv
import re
from typing import List, Dict, Any, Tuple, Protocol


class FileReader(Protocol):
    """
    Defines the contract for file readers (Standard CSV, Pandas, etc.)
    """

    def read(self, file_path: str) -> Tuple[List[Dict[str, Any]], List[str], str]:
        pass


class DataNormalizer:
    @staticmethod
    def normalize_value(value: str) -> Any:
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            if re.match(r"\d{4}-\d{2}-\d{2}", value.strip()):
                return value.strip()
        return value.strip()


class RecordComparator:
    @staticmethod
    def compare_records(
        source_record: Dict[str, Any],
        target_record: Dict[str, Any],
        common_columns: List[str],
    ) -> Dict[str, Dict[str, Any]]:
        discrepancies = {}
        for key in common_columns:
            if source_record.get(key) != target_record.get(key):
                discrepancies[key] = {
                    "source": source_record.get(key),
                    "target": target_record.get(key),
                }
        return discrepancies


class CSVFileReader:
    """Reads CSV files using standard CSV library."""

    def __init__(self, normalizer: DataNormalizer):
        self.normalizer = normalizer

    def read(self, file_path: str) -> Tuple[List[Dict[str, Any]], List[str], str]:
        """
        Read the CSV file and return the data, column headers, and error message if applicable.
        """
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file, delimiter=",")
                if reader.fieldnames:
                    fieldnames = reader.fieldnames
                    data = [self.normalize_record(row) for row in reader]
                    return data, fieldnames, ""
                else:
                    return [], [], f"File {file_path} is empty or has no data."
        except FileNotFoundError:
            return [], [], f"File {file_path} not found."

    def normalize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            key: self.normalizer.normalize_value(value) for key, value in record.items()
        }


class ReconciliationEngine:
    """Handles the core reconciliation logic."""

    def __init__(self, comparator: RecordComparator):
        self.comparator = comparator

    def reconcile(
        self,
        source_data: List[Dict[str, Any]],
        target_data: List[Dict[str, Any]],
        common_columns: List[str],
    ) -> Dict[str, Any]:
        source_dict = {record["ID"]: record for record in source_data}
        target_dict = {record["ID"]: record for record in target_data}

        reconciled, missing_in_target, missing_in_source, discrepancies = [], [], [], []

        for id, source_record in source_dict.items():
            if id in target_dict:
                target_record = target_dict[id]
                diff = self.comparator.compare_records(
                    source_record, target_record, common_columns
                )
                if diff:
                    discrepancies.append(
                        {
                            "source": source_record,
                            "target": target_record,
                            "fields_with_discrepancies": diff,
                        }
                    )
                else:
                    reconciled.append(
                        {"source": source_record, "target": target_record}
                    )
            else:
                missing_in_target.append(
                    {**source_record, "source": True, "target": None}
                )

        for id, target_record in target_dict.items():
            if id not in source_dict:
                missing_in_source.append(
                    {**target_record, "source": None, "target": True}
                )

        return {
            "reconciled": reconciled,
            "missing_in_target": missing_in_target,
            "missing_in_source": missing_in_source,
            "discrepancies": discrepancies,
        }


class CSVReconciler:
    """Facade to handle file reading and reconciliation."""

    def __init__(
        self,
        source_file: str,
        target_file: str,
        file_reader: CSVFileReader = None,
        reconciler: ReconciliationEngine = None,
    ):
        self.source_file = source_file
        self.target_file = target_file
        self.normalizer = DataNormalizer()
        self.comparator = RecordComparator()
        self.file_reader = (
            file_reader if file_reader is not None else CSVFileReader(self.normalizer)
        )
        self.reconciler = (
            reconciler
            if reconciler is not None
            else ReconciliationEngine(self.comparator)
        )

    def reconcile(self) -> Dict[str, Any]:
        source_data, source_columns, source_error = self.file_reader.read(
            self.source_file
        )
        target_data, target_columns, target_error = self.file_reader.read(
            self.target_file
        )

        errors = []
        if source_error:
            errors.append(source_error)
        if target_error:
            errors.append(target_error)

        common_columns = set(source_columns).intersection(set(target_columns))
        if not common_columns:
            errors.append("No common columns found between source and target files.")

        if not source_data or not target_data:
            errors.append("No data present in the files.")

        if errors:
            return {"errors": errors}

        return self.reconciler.reconcile(source_data, target_data, common_columns)
