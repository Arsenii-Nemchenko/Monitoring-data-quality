import json
import os
from unittest import TestCase
import pandas as pd

from src.metric import RecordCount


class TestClass(TestCase):
    def test_record_count_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> cars_37rows_3empty_5duplicate.csv
        name = "cars_37rows_3empty_5duplicate.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)

        try:
            result = RecordCount().calculate(data=pd.read_csv(file_path))

            self.assertEqual(result.metric_name, "RecordCount")
            self.assertEqual(result.value, 37)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_record_count_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> house_price_557rows_12duplicate.csv
        name = "house_price_557rows_12duplicate.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)

        try:
            result = RecordCount().calculate(data=pd.read_csv(file_path))

            self.assertEqual(result.metric_name, "RecordCount")
            self.assertEqual(result.value, 557)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError


    def test_record_count_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> sales_10rows_104avg.parquet
        name = "sales_10rows_104avg.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)

        try:
            result = RecordCount().calculate(data=pd.read_parquet(file_path))

            self.assertEqual(result.metric_name, "RecordCount")
            self.assertEqual(result.value, 10)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_record_count_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> car_owners_44rows_15colnull.parquet
        name = "car_owners_44rows_15colnull.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)

        try:
            result = RecordCount().calculate(data=pd.read_parquet(file_path))

            self.assertEqual(result.metric_name, "RecordCount")
            self.assertEqual(result.value, 44)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError


    def test_record_count_Json_case1(self):
        # Path to Test_files -> JSON_cases -> fish_1record_2null_2empty.json
        name = "fish_1record_2null_2empty.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
                df = pd.json_normalize(json_data)

            result = RecordCount().calculate(data=df)

            self.assertEqual(result.value, 1)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_record_count_Json_case2(self):
        # Path to Test_files -> JSON_cases -> catering_27records_4empty_26unique.json
        name = "catering_27records_4empty_26unique.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                df = pd.json_normalize(data)

            result = RecordCount().calculate(data=df)

            self.assertEqual(result.value, 27)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError