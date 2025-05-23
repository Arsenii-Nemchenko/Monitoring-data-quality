import datetime

import pandas as pd

import json
import re

from .database_manager import DBManager
from .enums import FileType


class DataBatchFile:
    def __init__(self, file, column, file_type:FileType, db_manager: DBManager):
        self.column = column
        self.file_type = file_type
        self.name, self.time_stamp, self.path = self._parse_filename(file)
        self.read = datetime.datetime.now()
        self.db_manager = db_manager
        self.computed_metrics = set()
        self.computed_column_metrics = set()

    def _parse_filename(self, input_string: str):
        timestamp_pattern = r"\d{14}"
        timestamp_match = re.search(timestamp_pattern, input_string)

        if not timestamp_match:
            raise ValueError("No valid timestamp found!")

        timestamp_start = timestamp_match.start()
        timestamp_end = timestamp_match.end()
        time_stamp = input_string[timestamp_start:timestamp_end]

        name = input_string[:timestamp_start]
        path = input_string[timestamp_end:] + "\\" + input_string[:timestamp_end] + "." + self.file_type.value.lower()
        if not path:
            raise ValueError("No valid path found!")

        return name, time_stamp, path

    def _get_parsed_data(self, metric_name: str):
        match self.file_type.value:
            case 'JSON':
                with open(self.path, 'r') as file:
                    data = json.load(file)
                    if metric_name == "DuplicateCount":
                        data = pd.json_normalize(data)

                return data
            case 'CSV':
                return pd.read_csv(self.path)
            case 'Parquet':
                return pd.read_parquet(self.path)
            case _:
                raise ValueError("Unsupported file type!")

    def compute_monitored_metrics(self, all_metrics, all_column_metrics):
        new_metrics = set(all_metrics) - self.computed_metrics
        new_col_metrics = set(all_column_metrics) - self.computed_column_metrics

        if new_metrics or new_col_metrics:
            self._compute(new_metrics, new_col_metrics)

        self.computed_metrics.update(new_metrics)
        self.computed_column_metrics.update(new_col_metrics)

    def _compute(self, metrics_to_compute, column_metrics_to_compute):
        for metric in metrics_to_compute:
            if not metric.accept(self.file_type) or bool(self.get_metric_value(metric.name)):
                continue
            else:
                result = metric.calculate(self._get_parsed_data(metric.name))
                self.db_manager.save(self.name, self.file_type.value, result.metric_name, str(self.time_stamp), result.value)

        for metric in column_metrics_to_compute:
            if not metric.accept(self.file_type) or bool(self.get_metric_value(metric.name)):
                continue
            else:
                result = metric.calculate(self._get_parsed_data(metric.name), column=self.column)
                self.db_manager.save(self.name, self.file_type.value, result.metric_name, str(self.time_stamp), result.value, column=self.column)


    def get_metric_value(self, metric_name):
        if any(metric_name==metric.name for metric in self.computed_metrics):
            return self.db_manager.get_value(self.name, metric_name, self.file_type.value, self.time_stamp)
        if any(metric_name == metric.name for metric in self.computed_column_metrics):
            return self.db_manager.get_value(self.name, metric_name, self.file_type.value, self.time_stamp, self.column)
        return None