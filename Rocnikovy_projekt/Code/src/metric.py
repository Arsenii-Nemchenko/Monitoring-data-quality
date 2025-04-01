import re
from abc import ABC, abstractmethod
from typing import Any
import numpy as np
import pandas as pd

import json

from pandas import DataFrame
from datetime import datetime

from src.enums import FileType
from src.metric_value import MetricValue


# abstract Metric class
class Metric(ABC):
    def __init__(self, name):
        self.name = name
        self.description = f"This is metric named {name}"
        self.file_types = list(FileType)

    def accept(self, file_type: FileType):
        if any(file_type.value == val.value  for val in self.file_types):
            return True
        return False

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
        self.file_types = [FileType.CSV, FileType.PARQUET]

    def is_na_or_empty(self, element):
        if isinstance(element, str):
            return element == ""
        else:
            return pd.isna(element)

    def calculate(self, data: DataFrame) -> MetricValue:
        empty = 0
        for index, row in data.iterrows():

            if all(self.is_na_or_empty(element) for element in row):
                empty += 1
        return MetricValue(self.name, empty, datetime.now())

class EmptyObjectCount(Metric):
    def __init__(self):
        super().__init__("EmptyRecordCount")
        self.file_types = [FileType.JSON]

    def calculate(self, data):
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
        self.file_types = [FileType.JSON]

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

    def calculate(self, data: DataFrame):
        empty_duplicates = 0

        for col in data.columns:
            data[col] = data[col].apply(self._make_hashable)

        duplicates = data.duplicated()
        for index, row in data.isna().iterrows():
            if all(element for element in row) and duplicates[index]:
                empty_duplicates += 1

        return MetricValue(self.name, duplicates.sum()-empty_duplicates, datetime.now())


class ColumnMetric(Metric):
    def __init__(self, name):
        super().__init__(name)
        self.file_types = [FileType.CSV, FileType.PARQUET]

    @abstractmethod
    def calculate(self, data: Any, column = None) -> MetricValue:
        pass

class ColumnMetricJson(Metric):
    def __init__(self, name):
        super().__init__(name)
        self.file_types = [FileType.JSON]

    @abstractmethod
    def calculate(self, data: Any, column = None) -> MetricValue:
        pass

    def _extract_name_and_column(self, column):
        dot_position = column.find(".")
        bracket_position = column.find("[")

        if dot_position == -1 and bracket_position == -1:
            name, column = column, ""
        elif dot_position == -1 or (bracket_position != -1 and bracket_position < dot_position):
            name, column = column[:bracket_position], column[bracket_position:]
        else:
            name = column[:dot_position]
            column = column[dot_position + 1:]

        return name, column

    def _process_list(self, data, column, function):
        if column.startswith("[*]"):
            return sum(function(item, column[4:]) for item in data)

        if column.startswith("["):
            end_idx = column.find("]")
            if end_idx != -1:
                try:
                    index = int(column[1:end_idx])
                    if 0 <= index < len(data):
                        return function(data[index], column[end_idx + 2:])
                    else:
                        raise IndexError(f"Index {index} is out of range")
                except ValueError:
                    pass
        return 0

    def _valid_path(self, path:str):
        pattern = r"^\$(\.\*|\.\w[\w\s]*|\[\"[^\"]+\"\]|\[\d+\]|\[\*\])+$"
        return bool(re.fullmatch(pattern, path))

    def _is_empty(self, value):
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, (list, dict)) and len(value) == 0:
            return True
        return False

class NullValuesCountColumn(ColumnMetric):
    def __init__(self):
        super().__init__("NullValuesCountColumn")
    def calculate(self, data: DataFrame, column = None) -> MetricValue:
        return MetricValue(self.name, sum(1 if pd.isna(value) or value=='' else 0 for value in data.loc[:,column]), datetime.now())

class NullValuesCountJson(ColumnMetricJson):
    def __init__(self):
        super().__init__("NullValuesCountColumn")

    def calculate(self, data: Any, column = "$") -> MetricValue:
        if column is None:
            raise ValueError("Column was not chosen!")

        if column == "$":
            return MetricValue(self.name,0, datetime.now())

        if not self._valid_path(column):
            raise ValueError("Wrong json-path!")


        column = column[1:]
        return MetricValue(self.name, self._count_nulls(data, column), datetime.now())

    def _count_nulls(self, data, column):
        if self._is_empty(data):
            return 1
        if column == "":
            return 0

        if isinstance(data, dict):
            name, column = self._extract_name_and_column(column)
            if name in data:
                return self._count_nulls(data[name], column)
            else:
                raise KeyError(f"Key '{name}' not found in JSON object")

        if isinstance(data, list):
            return self._process_list(data, column, self._count_nulls)

        return 0

class DefinedPathCount(ColumnMetricJson):
    def __init__(self):
        super().__init__("DefinedPathCount")

    def calculate(self, data: Any, column = "$") -> MetricValue:
        if column is None:
            raise ValueError("Column was not chosen!")

        if column == "$":
            return MetricValue(self.name, 0, datetime.now())

        if not self._valid_path(column):
            raise ValueError("Wrong json-path!")

        column = column[1:]
        return MetricValue(self.name, self._count(data, column), datetime.now())


    def _count(self, data, column):
        if self._is_empty(data):
            return 0
        if column == "":
            return 1

        if isinstance(data, dict):
            name, column = self._extract_name_and_column(column)
            if name in data:
                return self._count(data[name], column)
            else:
                raise KeyError(f"Key '{name}' not found in JSON object")

        if isinstance(data, list):
            return self._process_list(data, column, self._count)
        return 0

class UniqueValuesCount(ColumnMetric):
    def __init__(self):
        super().__init__("UniqueCount")
    def _is_unique(self, unique_values: set, value):
        if pd.isna(value) or value == '':
            return False
        if unique_values.__contains__(value):
            return False
        unique_values.add(value)
        return True

    def calculate(self, data: DataFrame, column = None) -> MetricValue:
        if column is None:
            raise ValueError("Column was not chosen!")

        unique_values = set()
        return MetricValue(self.name, sum(1 if self._is_unique(unique_values, value) else 0 for value in data.loc[:,column]), datetime.now())

class UniqueValuesCountJson(ColumnMetricJson):
    def __init__(self):
        super().__init__("UniqueCount")
        self.unique_values = set()

    def _is_unique(self, value):
        if self.unique_values.__contains__(value):
            return False
        self.unique_values.add(value)
        return True

    def calculate(self, data: Any, column= "$") -> MetricValue:
        if column is None:
            raise ValueError("Column was not chosen!")

        if column == "$":
            return MetricValue(self.name, 0, datetime.now())

        if not self._valid_path(column):
            raise ValueError("Wrong json-path!")

        column = column[1:]
        self.unique_values = set()
        return MetricValue(self.name, self._count_unique(data, column), datetime.now())

    def _count_unique(self, data, column):
        if self._is_empty(data):
            return 0

        if column == "" and self._is_unique( data):
            return 1

        if isinstance(data, dict):
            name, column = self._extract_name_and_column(column)
            if name in data:
                return self._count_unique(data[name], column)
            else:
                raise KeyError(f"Key '{name}' not found in JSON object")

        if isinstance(data, list):
            return self._process_list(data, column, self._count_unique)

        return 0


class AverageValue(ColumnMetric):
    def __init__(self):
        super().__init__("AverageValue")

    def _contains_numeric(self, data: DataFrame, column):
        numeric_count = 0
        contains_string = False

        for val in data[column]:
            if isinstance(val, (int, float)) and not pd.isna(val):
                numeric_count += 1
            elif isinstance(val, str) and val.strip():
                contains_string = True

        return numeric_count, not contains_string

    def calculate(self, data: DataFrame, column = None) -> MetricValue:
        if column is None:
            raise ValueError("Column was not chosen!")

        count, has_numeric = self._contains_numeric(data, column)

        if not has_numeric or count == 0:
            return MetricValue(self.name, 0, datetime.now())

        return MetricValue(self.name, int(sum(0 if pd.isna(val) or val=="" else float(val) for val in data.loc[:,column])/float(count)), datetime.now())



class AverageValueJson(ColumnMetricJson):
    def __init__(self):
        super().__init__("AverageValue")
        self.counter = 0

    def calculate(self, data: Any, column = "$") -> MetricValue:
        self.counter = 0
        if column is None:
            raise ValueError("Column was not chosen!")

        if column == "$":
            return MetricValue(self.name,0, datetime.now())

        if not self._valid_path(column):
            raise ValueError("Wrong json-path!")
        column = column[1:]
        result = self._calculate_avg(data, column)

        if self.counter == 0:
            return MetricValue(self.name, 0, datetime.now())

        return MetricValue(self.name, int(result/self.counter), datetime.now())

    def _calculate_avg(self, data, column):
        if data is None or data=='':
            return 0
        if isinstance(data, (int, float)):
            self.counter+=1
            return data

        if isinstance(data, str):
            try:
                numeric_value = float(data) if "." in data else int(data)
                self.counter += 1
                return numeric_value
            except ValueError:
                raise ValueError(f"Json structure has non-numeric value on path")

        if isinstance(data, dict):
            name, column = self._extract_name_and_column(column)
            if name in data:
                return self._calculate_avg(data[name], column)
            else:
                raise KeyError(f"Key '{name}' not found in JSON object")

        if isinstance(data, list):
            return self._process_list(data, column, self._calculate_avg)
        return 0
