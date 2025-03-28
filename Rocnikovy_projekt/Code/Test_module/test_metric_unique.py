import json
import os

import pandas as pd
from unittest import TestCase

from src.metric import UniqueValuesCount, UniqueValuesCountJson

class TestClass(TestCase):
    def test_unique_count_column_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> weather_empty31_40nullcol_14unique.csv
        name = "weather_empty31_40nullcol_14unique.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)
        column = "WindDir9am"

        try:
            result = UniqueValuesCount().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

            self.assertEqual(result.metric_name, "UniqueCount")
            self.assertEqual(result.value, 14)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError


    def test_unique_count_column_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> house_price_557rows_12duplicate.csv
        name = "house_price_557rows_12duplicate.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)
        column = "area"

        try:
            result = UniqueValuesCount().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

            self.assertEqual(result.metric_name, "UniqueCount")
            self.assertEqual(result.value, 284)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_unique_count_column_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> markets_8duplicate_5unique.parquet
        name = "markets_8duplicate_5unique.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)
        column = "name"

        try:
            result = UniqueValuesCount().calculate(data=pd.read_parquet(file_path), column=column)

            self.assertEqual(result.metric_name, "UniqueCount")
            self.assertEqual(result.value, 5)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_unique_count_column_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> complects_3empty_3unique_6avg.parquet
        name = "complects_3empty_3unique_6avg.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)
        column = "discount"

        try:
            result = UniqueValuesCount().calculate(data=pd.read_parquet(file_path), column=column)

            self.assertEqual(result.metric_name, "UniqueCount")
            self.assertEqual(result.value, 3)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_unique_count_column_Json_case1(self):
        # Path to Test_files -> Json_cases -> courses_13duplicate_1null_6unique.json
        name = "courses_13duplicate_1null_6unique.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$.passed%"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = UniqueValuesCountJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "UniqueCount")
            self.assertEqual(result.value, 6)
            print(f"Ok {name.ljust(60)} path: {path}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError

    def test_unique_count_column_Json_case2(self):
        # Path to Test_files -> Json_cases -> catering_27records_4empty_26unique.json
        name = "catering_27records_4empty_26unique.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$.name"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = UniqueValuesCountJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "UniqueCount")
            self.assertEqual(result.value, 26)
            print(f"Ok {name.ljust(60)} path: {path}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError




