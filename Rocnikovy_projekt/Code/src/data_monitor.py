import os.path

from .data_batch_file import DataBatchFile
from .enums import FileType


# DataMonitor class
#Column metrics have to be included in monitored_metrics
class DataMonitor:
    def __init__(self, data_name: str, monitored_folder: str,
                 data_description: str, monitored_metrics, monitored_column_metrics, file_format: str, db_manager, column):
        self.folder = monitored_folder
        self.processed_files = set()
        self.data_name = data_name
        self.data_description = data_description
        self.batch_files = []
        self.monitored_metrics = monitored_metrics
        self.monitored_column_metrics = monitored_column_metrics
        self.file_format = self._process_file_format(file_format)
        self.db_manager = db_manager

        self.column = column

    def _process_file_format(self, file: str):
        if file == 'json':
            return FileType.JSON
        elif file == 'csv':
            return FileType.CSV
        elif file == 'parquet':
            return FileType.PARQUET
        else:
            raise ValueError(f"Unsupported file format: {file}")

    def _new_files(self):
        if os.path.exists(self.folder):
            all_files = [file for file in os.listdir(self.folder)]


            new_files = []
            for file in all_files:
                if not self.processed_files.__contains__(file):
                    self.processed_files.add(file)
                    file_format_part = file.rfind('.')
                    if not self._process_file_format(file[file_format_part + 1:]) == self.file_format:
                        continue

                    file = file[:file_format_part]

                    new_files.append(file + os.path.join("/", self.folder))
            return new_files

        else:
            return []


    def start_monitoring(self):
        input_files = self._new_files()
        for file in input_files:
            batch_file = DataBatchFile(file, self.monitored_metrics,
                                       self.monitored_column_metrics,
                                       self.column, self.file_format, self.db_manager)

            batch_file.compute_monitored_metrics()
            self.batch_files.append(batch_file)
