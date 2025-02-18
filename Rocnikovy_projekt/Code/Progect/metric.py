from abc import ABC, abstractmethod
from typing import Any

from pandas import DataFrame
from datetime import datetime
from metric_value import MetricValue


# abstract Metric class
class Metric(ABC):
    def __init__(self, name):
        self.name = name
    @abstractmethod
    def calculate(self, data: Any) -> MetricValue:
        pass


class RecordCount(Metric):
    def __init__(self):
        super().__init__("RecordCount")

    def calculate(self, data : DataFrame):
        return MetricValue(self.name ,data.shape[0], datetime.now())

class EmptyRecordCount(Metric):
    def __init__(self):
        super().__init__("EmptyRecordCount")

    def calculate(self, data : DataFrame):
        is_null_object = data.isna()
        shape = is_null_object.shape

        counter = 0
        for i in range(shape[0]):
            found = True
            for j in range(shape[1]):
                if not is_null_object.iloc[i, j]:
                    found = False
                    break
            if found:
                counter+=1

        return MetricValue(self.name, counter, datetime.now())

class EmptyObjectCount(Metric):
    def __init__(self):
        super().__init__("EmptyObjectCount")

    def calculate(self, data ):
        return MetricValue(self.name, self._count_empty(data), datetime.now())

    def _is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, (list, dict)) and len(value) == 0:
            return True
        return False

    def _is_empty_object(self, obj):
        if isinstance(obj, dict):
            return all(self._is_empty(value) or self._is_empty_object(value) for value in obj.values())
        return False

    def _count_empty(self, data):
        if isinstance(data, dict):
            count = 1 if self._is_empty_object(data) else 0
            count += sum(self._count_empty(value) for value in data.values())
            return count
        elif isinstance(data, list):
            return sum(self._count_empty(item) for item in data)
        return 0

class NullObjectCount(Metric):
    def __init__(self):
        super().__init__("NullObjectCount")

    def calculate(self, data):
        return MetricValue(self.name, self._null_count(data), datetime.now())

    def _null_count(self, data):
        if data is None:
            return 1

        elif isinstance(data, dict):
            if all(not isinstance(value, (dict, list)) for value in data.values()):
                return 0

            return sum(self._null_count(value) for value in data.values())
        elif isinstance(data, list):
            return sum(self._null_count(item) for item in data)

        return 0

class DuplicateRecordCount(Metric):
    def __init__(self):
        super().__init__("DuplicateCount")
    def calculate(self, data: DataFrame):
        empty_duplicates = 0
        duplicates = data.duplicated()
        for index, row in data.isna().iterrows():
            if all(element for element in row) and duplicates[index]:
                empty_duplicates += 1

        return MetricValue(self.name, data.duplicated().sum()-empty_duplicates, datetime.now())
