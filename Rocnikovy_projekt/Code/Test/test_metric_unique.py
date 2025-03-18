import json
import pandas as pd
from unittest import TestCase

from metric import UniqueValuesCount, UniqueValuesCountJson

class TestClass(TestCase):
    def test_null_count_column_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> weather_empty31_nullcol40_14unique.csv
        file_path = input("Enter path to weather_empty31_nullcol40_14unique.csv: ")
        column = "WindDir9am"

        result = UniqueValuesCount().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

        self.assertEqual(result.metric_name, "UniqueCount")
        self.assertEqual(result.value, 14)

    def test_null_count_column_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> house_price_557rows_12duplicate.csv
        file_path = input("Enter path to house_price_557rows_12duplicate.csv: ")
        column = "area"

        result = UniqueValuesCount().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

        self.assertEqual(result.metric_name, "UniqueCount")
        self.assertEqual(result.value, 284)

    def test_null_count_column_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> markets_8duplicate_5unique.parquet
        file_path = input("Enter path to markets_8duplicate_5unique.parquet: ")
        column = "name"

        result = UniqueValuesCount().calculate(data=pd.read_parquet(file_path), column=column)

        self.assertEqual(result.metric_name, "UniqueCount")
        self.assertEqual(result.value, 5)

    def test_null_count_column_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> complects_3empty_3unique.parquet
        file_path = input("Enter path to complects_3empty_3unique.parquet: ")
        column = "discount"

        result = UniqueValuesCount().calculate(data=pd.read_parquet(file_path), column=column)

        self.assertEqual(result.metric_name, "UniqueCount")
        self.assertEqual(result.value, 3)

    def test_null_count_column_Json_case1(self):
        # Path to Test_files -> Json_cases -> courses_13duplicate_1null_6unique.json
        file_path = input("Enter path to courses_13duplicate_1null_6unique.json: ")
        path = "$.passed%"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = UniqueValuesCountJson().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "UniqueCount")
        self.assertEqual(result.value, 6)

    def test_null_count_column_Json_case2(self):
        # Path to Test_files -> Json_cases -> catering_27records_4empty_26unique.json
        file_path = input("Enter path to catering_27records_4empty_26unique.json: ")
        path = "$.name"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = UniqueValuesCountJson().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "UniqueCount")
        self.assertEqual(result.value, 26)




