import datetime

import pandas as pd

import json
import re

from Progect.metric import DuplicateRecordCount
from database_manager import DBManager
from metric import Metric
from enums import FileType


class DataBatchFile:

    def __init__(self, file: str, monitored_metrics, file_type:FileType, db_manager: DBManager):
        self.monitored_metrics = monitored_metrics
        self.file_type = file_type
        self.name, self.time_stamp, self.path = self._parse_input(file)
        self.read = datetime.datetime.now()
        self.db_manager = db_manager

    def _parse_input(self, input_string: str):
        timestamp_pattern = r"\d{14}"
        timestamp_match = re.search(timestamp_pattern, input_string)

        if not timestamp_match:
            raise ValueError("No valid timestamp found!")

        timestamp_start = timestamp_match.start()
        timestamp_end = timestamp_match.end()
        timestamp = input_string[timestamp_start:timestamp_end]

        name = input_string[:timestamp_start]
        path = input_string[timestamp_end:]+ "\\" + input_string[:timestamp_end] + "."+ self.file_type.value.lower()
        if not path:
            raise ValueError("No valid path found!")

        return name, timestamp, path

    def _get_parsed_data(self, metric_name: str):
        match self.file_type.value:
            case 'JSON':
                with open(self.path, 'r') as file:
                    data = json.load(file)
                if metric_name != 'NullObjectCount' and metric_name != 'EmptyObjectCount':
                    data = pd.json_normalize(data)

                return data
            case 'CSV':
                return pd.read_csv(self.path)
            case 'Parquet':
                return pd.read_parquet(self.path)
            case _:
                raise ValueError("Unsupported file type!")

#So far this is the solution to unchangeable monitored metrics.
# It will be fixed after GUI implementation of changing of monitored metrics
    def compute_monitored_metrics(self):
        for metric in self.monitored_metrics:
            if (self.file_type == FileType.JSON and metric.name != 'NullObjectCount'
                    and metric.name !='EmptyObjectCount' and metric.name != 'DuplicateCount'):
                continue
            elif self.file_type != FileType.JSON and (metric.name == 'NullObjectCount' or metric.name == 'EmptyObjectCount'):
                continue
            else:
                result = metric.calculate(self._get_parsed_data(metric.name))
                self.db_manager.save(self.name, self.file_type.value, result.metric_name, str(self.time_stamp), result.value)

    def get_metric_value(self, metric: Metric ):
        return self.db_manager.get_value(self.name, metric.name, self.file_type, self.time_stamp)


