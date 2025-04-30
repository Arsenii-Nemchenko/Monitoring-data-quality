from src.data_monitor import DataMonitor
from src.metric import *

class MetricFactory:
    def __init__(self):
        self.metrics = {"RecordCount": [RecordCount(), RecordCountJson()],
                        "EmptyRecordCount": [EmptyRecordCount(), EmptyObjectCount()],
                        "NullObjectCount": [NullObjectCount()],
                        "DuplicateCount": [DuplicateRecordCount()],
                        "NullValuesCountColumn": [NullValuesCountColumn(), NullValuesCountJson()],
                        "DefinedPathCount": [DefinedPathCount()],
                        "UniqueCount": [UniqueValuesCount(), UniqueValuesCountJson()],
                        "AverageValue": [AverageValue(), AverageValueJson()]}

    def get(self, name, file_type):
        file_type = DataMonitor.process_file_format(file_type)
        for metric in self.metrics.get(name):
            if metric.accept(file_type):
                return metric
