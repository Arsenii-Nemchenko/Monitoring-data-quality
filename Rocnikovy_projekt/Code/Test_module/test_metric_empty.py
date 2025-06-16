import os
from unittest import TestCase
import pandas as pd
import json

from ..src.metric import EmptyObjectCount
from ..src.metric import EmptyRecordCount


class TestClass(TestCase):
    def test_empty_record_count_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty_11nullcol.csv
        name = "MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty_11nullcol.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)

        try:
            result = EmptyRecordCount().calculate(data=pd.read_csv(file_path, index_col=False))

            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 8)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_empty_record_count_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> TB_Burden_Country_5130rows_10empty.csv
        name = "TB_Burden_Country_5130rows_10empty.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)

        try:
            result = EmptyRecordCount().calculate(data=pd.read_csv(file_path, index_col=False))

            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 10)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_empty_record_count_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> catering_9empty_10colnull.parquet
        name = "catering_9empty_10colnull.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)

        try:
            result = EmptyRecordCount().calculate(data=pd.read_parquet(file_path))

            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 9)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_empty_record_count_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> complects_3empty_3unique_6avg.parquet
        name = "complects_3empty_3unique_6avg.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)

        try:
            result = EmptyRecordCount().calculate(data=pd.read_parquet(file_path))

            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 3)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError


    def test_empty_record_count_Json_case1(self):
        # Path to Test_files -> Json_cases -> gas_supply_22empty_7nullcol_4defined.json
        name = "gas_supply_22empty_7nullcol_4defined.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = EmptyObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 22)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError


    def test_empty_record_count_Json_case2(self):
        # Path to Test_files -> Json_cases -> Gurteen_weather_4empty_3defined_90avg.json
        name = "Gurteen_weather_4empty_3defined_90avg.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = EmptyObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 3)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError
