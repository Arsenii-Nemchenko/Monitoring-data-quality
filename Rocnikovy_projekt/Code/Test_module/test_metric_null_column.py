import json
import os

import pandas as pd

from unittest import TestCase
from src.metric import NullValuesCountColumn, NullValuesCountJson

class TestClass(TestCase):
    def test_null_count_column_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty_11nullcol.csv
        name = "MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty_11nullcol.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)
        column = "Death Rate Per 100,000"

        try:
            result = NullValuesCountColumn().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            self.assertEqual(result.value, 11)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError


    def test_null_count_column_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> weather_empty31_40nullcol_14unique.csv
        name = "weather_empty31_40nullcol_14unique.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)
        column = "Pressure9am"

        try:
            result = NullValuesCountColumn().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            self.assertEqual(result.value, 40)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_null_count_column_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> car_owners_44rows_15colnull.parquet
        name = "car_owners_44rows_15colnull.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)
        column = "contact"

        try:
            result = NullValuesCountColumn().calculate(data=pd.read_parquet(file_path), column=column)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            self.assertEqual(result.value, 15)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_null_count_column_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> catering_9empty_10colnull.parquet
        name = "catering_9empty_10colnull.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)
        column = "name"

        try:
            result = NullValuesCountColumn().calculate(data=pd.read_parquet(file_path), column=column)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            self.assertEqual(result.value, 10)
            print(f"Ok {name.ljust(60)} column: {column}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_null_count_column_Json_case1(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_19null_19nullcol.json
        name = "cs_weapons_12duplicate_19null_19nullcol.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$something that... does not make sense"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullValuesCountJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            print(f"Ok {name.ljust(60)} path: {path}")
        except ValueError:
            return
        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError


    def test_null_count_column_Json_case2(self):
        # Path to Test_files -> Json_cases -> gas_supply_24empty_9nullcol_4defined.json
        name = "gas_supply_24empty_9nullcol_4defined.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$.Moffat"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullValuesCountJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            self.assertEqual(result.value, 9)
            print(f"Ok {name.ljust(60)} path: {path}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError

    def test_null_count_column_Json_case3(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_19null_19nullcol.json
        name = "cs_weapons_12duplicate_19null_19nullcol.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$.grenades.name"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullValuesCountJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "NullValuesCountColumn")
            self.assertEqual(result.value, 19)
            print(f"Ok {name.ljust(60)} path: {path}")

        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError

