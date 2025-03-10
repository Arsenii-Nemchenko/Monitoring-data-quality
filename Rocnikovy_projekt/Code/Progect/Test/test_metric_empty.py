from unittest import TestCase
import tempfile
import pandas as pd
import json

from Progect.metric import EmptyObjectCount
from Progect.metric import EmptyRecordCount


class TestClass(TestCase):
    def test_empty_record_count_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty.csv
        file_path = input("Enter path to MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty.csv: ")

        result = EmptyRecordCount().calculate(data=pd.read_csv(file_path, index_col=False))
        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 8)

    def test_empty_record_count_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> TB_Burden_Country_5130rows_10empty.csv
        file_path = input("Enter path to TB_Burden_Country_5130rows_10empty.csv: ")

        result = EmptyRecordCount().calculate(data=pd.read_csv(file_path, index_col=False))
        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 10)

    def test_empty_record_count_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> catering_9empty.parquet
        file_path = input("Enter path to catering_9empty.parquet: ")

        result = EmptyRecordCount().calculate(data=pd.read_parquet(file_path))
        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 9)


    def test_empty_record_count_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> complects_3empty.parquet
        file_path = input("Enter path to complects_3empty.parquet: ")

        result = EmptyRecordCount().calculate(data=pd.read_parquet(file_path))
        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 3)

    def test_empty_record_count_Json_case1(self):
        # Path to Test_files -> Json_cases -> gas_supply_24empty.json
        file_path = input("Enter path to gas_supply_24empty.json: ")

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)
            result = EmptyObjectCount().calculate(data=loaded_data)

        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 24)


    def test_empty_record_count_Json_case2(self):
        #Path to Test_files -> Json_cases -> Gurteen_weather_4empty.json
        file_path = input("Enter path to Gurteen_weather_4empty.json: ")

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)
        result = EmptyObjectCount().calculate(data=loaded_data)

        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 4)
