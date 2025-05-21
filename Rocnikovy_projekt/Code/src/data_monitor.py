import os.path

from .data_batch_file import DataBatchFile
from .enums import FileType
import threading

# DataMonitor class
class DataMonitor:
    def __init__(self, data_name: str, monitored_folder: str,
                 data_description: str, monitored_metrics, monitored_column_metrics, file_format: str, db_manager, column):
        self.folder = monitored_folder
        self.processed_files = set()
        self.data_name = data_name
        self.data_description = data_description
        self.batch_files = {}
        self.monitored_metrics = monitored_metrics
        self.monitored_column_metrics = monitored_column_metrics
        self.file_format = self.process_file_format(file_format)
        self.db_manager = db_manager

        self.column = column
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

    @staticmethod
    def process_file_format(file: str):
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
            new_files = []

            for file in os.listdir(self.folder):
                if not self.processed_files.__contains__(file):

                    file_format_part = file.rfind('.')
                    
                    if self.process_file_format(file[file_format_part + 1:]) != self.file_format:
                        continue

                    file = file[:file_format_part]
                    file_key = (file, self.column)
                    if file_key not in self.processed_files:        
                        self.processed_files.add(file_key)
                        new_files.append(file)
            return new_files

        else:
            return []

    def start_monitoring(self):
        input_files = self._new_files()
        new_batch_map = {}

        for file in input_files:
            batch_file = DataBatchFile(file + os.path.join("/", self.folder),
                                       self.column, self.file_format, self.db_manager)

            batch_file.compute_monitored_metrics(self.monitored_metrics, self.monitored_column_metrics)
            if self.column not in new_batch_map:
                new_batch_map[self.column] = []
            new_batch_map[self.column].append(batch_file)




        with self.condition:

            for key, batch_list in new_batch_map.items():
                if key not in self.batch_files:
                    self.batch_files[key] = []
                self.batch_files[key].extend(batch_list)

            for key, batch_list in self.batch_files.items():
                for batch_file in batch_list:
                    batch_file.compute_monitored_metrics(self.monitored_metrics, self.monitored_column_metrics)

            if self.batch_files:
                self.condition.notify_all()
