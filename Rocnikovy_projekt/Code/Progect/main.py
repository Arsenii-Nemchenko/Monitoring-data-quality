import os.path

from enums import FileType
from data_monitor import DataMonitor
from data_batch_file import DataBatchFile
from metric import RecordCount, EmptyRecordCount, NullRecordCount
from metric_value import MetricValue

def main():
    folder = input("Enter the folder path: ")

    monitor = DataMonitor(folder)
    files = monitor.new_files()

    for file_path in files:
        if file_path.endswith(".csv"):
            file_type = FileType.CSV
        elif file_path.endswith(".json"):
            file_type = FileType.JSON
        elif file_path.endswith(".parquet"):
            file_type = FileType.PARQUET
        else:
            raise RuntimeError(f"Unsupported file type: {file_path}")

        batch_file = DataBatchFile(file_path, file_type)
        data = batch_file.load_data()

        record_count = RecordCount()
        null_objects_json  = NullRecordCount()
        empty_record_count = EmptyRecordCount()

        metric_type = input()
        match metric_type:
            case "records":
                print(f"Number of records in {os.path.basename(file_path)} is {record_count.calculate(data).value}")
            case "null_objects":
                if file_type == FileType.JSON:
                    print(f"Number of null objects in {os.path.basename(file_path)} is {null_objects_json.calculate(data).value}")
                else:
                    continue
            case "empty_records":
                if file_type is not FileType.JSON:
                    print(f"Number of empty records in {os.path.basename(file_path)} is {empty_record_count.calculate(data).value}")
            case _:
                raise RuntimeError(f"Unsupported metric type: {metric_type}")

main()