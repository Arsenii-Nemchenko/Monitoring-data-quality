import re
from abc import ABC, abstractmethod
from typing import Any
import numpy as np
import pandas as pd

import json

from pandas import DataFrame
from datetime import datetime

from Progect.metric_value import MetricValue


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
        empty = 0
        for index, row in data.iterrows():

            if all(self.is_na_or_empty(element) for element in row):
                empty += 1
        return MetricValue(self.name ,data.shape[0]-empty, datetime.now())

    def is_na_or_empty(self, element):
        if isinstance(element, str):
            return element == ""
        elif isinstance(element, list):
            return all(self.is_na_or_empty(item) for item in element)
        elif isinstance(element, dict):
            return all(self.is_na_or_empty(val) for val in element.values())
        else:
            return pd.isna(element)
class EmptyRecordCount(Metric):
    def __init__(self):
        super().__init__("EmptyRecordCount")

    def is_na_or_empty(self, element):
        if isinstance(element, str):
            return element == ""
        else:
            return pd.isna(element)

    def calculate(self, data: Any) -> MetricValue:
        empty = 0
        for index, row in data.iterrows():

            if all(self.is_na_or_empty(element) for element in row):
                empty += 1
        return MetricValue(self.name, empty, datetime.now())

class EmptyObjectCount(Metric):
    def __init__(self):
        super().__init__("EmptyRecordCount")

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
        if data is None:
            return 1
        if isinstance(data, dict):
            count = 1 if self._is_empty_object(data) else 0
            count += sum(self._count_empty(value) if isinstance(value, (dict, list)) else 0 for value in data.values())
            return count
        elif isinstance(data, list):
            return sum(self._count_empty(item) for item in data)
        return 0

class NullObjectCount(Metric):
    def __init__(self):
        super().__init__("NullObjectCount")

    def calculate(self, data):
        return MetricValue(self.name, self._null_count(data), datetime.now())

    def _no_nested_list(self, data, value):
        if data is None:
            return True
        if isinstance(data.get(value), (dict, list)):
            return True


    def _null_count(self, data):
        if data is None:
            return 1
        elif isinstance(data, list):

            return sum(self._null_count(value) for value in data)
        elif isinstance(data, dict):

            return sum(self._null_count(data.get(value)) if self._no_nested_list(data, value) else 0  for value in data)
        return 0




class DuplicateRecordCount(Metric):
    def __init__(self):
        super().__init__("DuplicateCount")

    def _make_hashable(self, value):
        if isinstance(value, list) or isinstance(value, np.ndarray):
            return tuple(self._make_hashable(item) for item in value)
        elif isinstance(value, dict):
            return json.dumps({k: self._make_hashable(v) for k, v in value.items()}, sort_keys=True)
        elif isinstance(value, str):
            if value == '':
                return None
        return value

    def calculate(self, data: pd.DataFrame):
        empty_duplicates = 0

        for col in data.columns:
            data[col] = data[col].apply(self._make_hashable)

        duplicates = data.duplicated()
        for index, row in data.isna().iterrows():
            if all(element for element in row) and duplicates[index]:
                empty_duplicates += 1

        return MetricValue(self.name, duplicates.sum()-empty_duplicates, datetime.now())


class ColumnMetric(Metric):
    @abstractmethod
    def calculate(self, data: Any, column = None) -> MetricValue:
        pass
    def _valid_path(self, path:str):
        pattern = r"^\$(\.[^.]+)+$"
        return bool(re.fullmatch(pattern, path))

class NullValuesCountColumn(ColumnMetric):
    def __init__(self):
        super().__init__("NullValuesCountColumn")
    def calculate(self, data: DataFrame, column = None) -> MetricValue:
        return MetricValue(self.name, sum(1 if pd.isna(value) or value=='' else 0 for value in data.loc[:,column]), datetime.now())

class NullValuesCountJson(ColumnMetric):
    def __init__(self):
        super().__init__("NullValuesCountColumn")

    def calculate(self, data: Any, column = "$") -> MetricValue:
        if column == "$":
            return MetricValue(self.name,0, datetime.now())

        if not self._valid_path(column):
            raise ValueError("Wrong json-path!")

        column = column[1:]
        return MetricValue(self.name, self._count_nulls(data, column), datetime.now())

    def _count_nulls(self, data, column):
        if data is None or data == "":
            return 1
        if isinstance(data, dict):
            dot_position = column[1:].find(".")
            if dot_position != -1:
                name = column[1:dot_position + 1]
                column = column[dot_position + 1:]
            else:
                name = column[1:]
                column = ""

            return sum(self._count_nulls(data[val], column)
                       if (val is not None and val == name) or val is None else 0 for val in data)

        if isinstance(data, list):
            return sum(self._count_nulls(val, column) for val in data)
        return 0

