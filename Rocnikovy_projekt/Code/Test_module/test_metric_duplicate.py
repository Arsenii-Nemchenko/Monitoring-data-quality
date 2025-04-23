import os

import pandas as pd
import json
from unittest import TestCase

from src.metric import DuplicateRecordCount


class TestClass(TestCase):

    def test_duplicate_count_CSV_case1(self):
        #Path to Test_files -> CSV_cases -> cars_37rows_3empty_5duplicate.csv
        name = "cars_37rows_3empty_5duplicate.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)

        try:
            result = DuplicateRecordCount().calculate(data=pd.read_csv(file_path))

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 5)
            print(f"OK {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")

    def test_duplicate_count_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> house_price_561rows_12duplicate_284unique.csv
        name = "house_price_561rows_12duplicate_284unique.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)

        try:
            result = DuplicateRecordCount().calculate(data=pd.read_csv(file_path))

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 12)
            print(f"OK {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_duplicate_count_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> cs_loadouts_12duplicate.parquet
        name = "cs_loadouts_12duplicate.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)

        try:
            result = DuplicateRecordCount().calculate(data=pd.read_parquet(file_path))

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 12)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_duplicate_count_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> markets_8duplicate_5unique.parquet
        name = "markets_8duplicate_5unique.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)

        try:
            result = DuplicateRecordCount().calculate(data=pd.read_parquet(file_path))

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 8)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_duplicate_Json_case1(self):
        # Path to Test_files -> JSON_cases -> cs_weapons_12duplicate_2null_2unique_1nullcol.json
        name = "cs_weapons_12duplicate_2null_2unique_1nullcol.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
                loaded_data = pd.json_normalize(loaded_data)

            result = DuplicateRecordCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 12)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_duplicate_Json_case2(self):
        # Path to Test_files -> JSON_cases -> courses_13duplicate_1null_6unique.json
        name = "courses_13duplicate_1null_6unique.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)
                loaded_data = pd.json_normalize(loaded_data)

            result = DuplicateRecordCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 13)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError
