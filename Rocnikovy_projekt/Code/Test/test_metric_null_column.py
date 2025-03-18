import json

import pandas as pd

from unittest import TestCase
from metric import NullValuesCountColumn, NullValuesCountJson

class TestClass(TestCase):
    def test_null_count_column_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty_11nullcol.csv
        file_path = input("Enter path to MORTALITY_AGE_SPECIFIC_BY_COUNTRY_8empty_11nullcol.csv: ")
        column = "Death Rate Per 100,000"

        result = NullValuesCountColumn().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

        self.assertEqual(result.metric_name, "NullValuesCountColumn")
        self.assertEqual(result.value, 11)

    def test_null_count_column_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> weather_empty31_nullcol40.csv
        file_path = input("Enter path to weather_empty31_nullcol40.csv: ")
        column = "Pressure9am"

        result = NullValuesCountColumn().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

        self.assertEqual(result.metric_name, "NullValuesCountColumn")
        self.assertEqual(result.value, 40)

    def test_null_count_column_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> car_owners_44rows_15colnull.parquet
        file_path = input("Enter path to car_owners_44rows_15colnull.parquet: ")
        column = "contact"

        result = NullValuesCountColumn().calculate(data=pd.read_parquet(file_path), column=column)

        self.assertEqual(result.metric_name, "NullValuesCountColumn")
        self.assertEqual(result.value, 15)

    def test_null_count_column_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> catering_9empty_10colnull.parquet
        file_path = input("Enter path to catering_9empty_10colnull.parquet: ")
        column = "name"

        result = NullValuesCountColumn().calculate(data=pd.read_parquet(file_path), column=column)

        self.assertEqual(result.metric_name, "NullValuesCountColumn")
        self.assertEqual(result.value, 10)

    def test_null_count_column_Json_case1(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_19null.json
        file_path = input("Enter path to cs_weapons_12duplicate_19null.json: ")
        path = "$something that... does not make sense"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)
        try:
            result = NullValuesCountJson().calculate(data=loaded_data, column=path)
        except ValueError:
            return


    def test_null_count_column_Json_case2(self):
        # Path to Test_files -> Json_cases -> gas_supply_24empty_9nullcol_4defined.json
        file_path = input("Enter path to gas_supply_24empty_9nullcol_4defined.json: ")
        path = "$.Moffat"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = NullValuesCountJson().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "NullValuesCountColumn")
        self.assertEqual(result.value, 9)

    def test_null_count_column_Json_case3(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_19null_19nullcol.json
        file_path = input("Enter path to cs_weapons_12duplicate_19null_19nullcol: ")
        path = "$.grenades.name"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = NullValuesCountJson().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "NullValuesCountColumn")
        self.assertEqual(result.value, 19)

