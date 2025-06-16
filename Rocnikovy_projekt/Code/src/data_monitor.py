import os.path

from PyQt5.QtCore import pyqtSignal, QMutex, QWaitCondition, QMutexLocker, QThread

from .data_batch_file import DataBatchFile
from .enums import FileType

# DataMonitor class
class DataMonitor(QThread):
    invalid_json_path = pyqtSignal()
    data_ready = pyqtSignal()

    def __init__(self, data_name: str, monitored_folder: str,
                 data_description: str, monitored_metrics, monitored_column_metrics,
                 file_format: str, db_manager, column, interval):
        super().__init__()
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
        self.interval = interval

        # Part for Qt synchronization
        self.mutex = QMutex()
        self.calculation_mutex = QMutex()
        self.reset_mutex = QMutex()
        self.data_condition = QWaitCondition()
        self.calculation_condition = QWaitCondition()
        self._stop_flag = False
        self._initial_data_ready = False
        self._calculation_in_progress = False

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
                try:
                    if not self.processed_files.__contains__(file):

                        file_format_part = file.rfind('.')

                        if self.process_file_format(file[file_format_part + 1:]) != self.file_format:
                            continue

                        file = file[:file_format_part]
                        file_key = (file, self.column)
                        if file_key not in self.processed_files:
                            self.processed_files.add(file_key)
                            new_files.append(file)
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
            return new_files

        else:
            return []

    def set_arguments(self, monitored_regular, monitored_column, column, interval):
        with QMutexLocker(self.reset_mutex):
            self.monitored_metrics = monitored_regular
            self.monitored_column_metrics = monitored_column
            self.column = column
            self.interval = interval
            self._initial_data_ready = False
            self._stop_flag = False
            self.data_condition.wakeOne()
            with QMutexLocker(self.mutex):
                self.data_condition.wakeAll()

    def stop(self):
        with QMutexLocker(self.mutex):
            self._stop_flag = True
            self.data_condition.wakeAll()
            self.calculation_condition.wakeAll()

    def is_initial_data_ready(self):
        return self._initial_data_ready

    def wait_for_calculation(self):
        with QMutexLocker(self.mutex):
            while self._calculation_in_progress and not self._stop_flag:
                self.calculation_condition.wait(self.mutex, 200)

    def signal_calculation_start(self):
        with QMutexLocker(self.mutex):
            self._calculation_in_progress = True

    def signal_calculation_end(self):
        self._calculation_in_progress = False
        self.calculation_condition.wakeAll()

    def run(self):
        while True:
            try:
                with QMutexLocker(self.reset_mutex):

                    input_files = self._new_files()
                    self.start_monitoring(input_files)

                    with QMutexLocker(self.mutex):
                        if self._stop_flag:
                            break
                        # Wait with timeout but release mutex during wait
                        self.data_condition.wait(self.mutex, (self.interval * 1000))

                    self.wait_for_calculation()

            except Exception as e:
                print(f"Monitoring error: {str(e)}")

    def start_monitoring(self, input_files):
        new_batch_map = {}

        for file in input_files:
            try:
                is_invalid = False
                file_path = file + os.path.join("/", self.folder)
                batch_file = DataBatchFile(file_path, self.column, self.file_format, self.db_manager)

                batch_file.compute_monitored_metrics(
                    self.monitored_metrics,
                    self.monitored_column_metrics
                )

                if self.column not in new_batch_map:
                    new_batch_map[self.column] = []
                new_batch_map[self.column].append(batch_file)
            except Exception as e:
                print(f"Error processing file {file}: {e}")
                self.invalid_json_path.emit()
                is_invalid = True
            if is_invalid:
                break

        with QMutexLocker(self.mutex):
            for key, batch_list in new_batch_map.items():
                if key not in self.batch_files:
                    self.batch_files[key] = []
                self.batch_files[key].extend(batch_list)

            for key, batch_list in self.batch_files.items():
                for batch_file in batch_list:
                    try:
                        batch_file.compute_monitored_metrics(
                            self.monitored_metrics,
                            self.monitored_column_metrics
                        )
                    except KeyError as k:
                        print(f"Error key error: {e}")
                        if self.file_format == FileType.JSON:
                            self.invalid_json_path.emit()
                        break
                    except Exception as e:
                        print(f"Error recomputing metrics: {e}")
                        break

            if not self._initial_data_ready:
                self._initial_data_ready = True

            self.data_condition.wakeAll()
            self.data_ready.emit()

    def get_batch_files(self, column):
        return self.batch_files.get(column, []).copy()
