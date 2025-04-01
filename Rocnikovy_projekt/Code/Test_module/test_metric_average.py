import json
import os

import pandas as pd
from unittest import TestCase

from  src.metric import AverageValue, AverageValueJson

class TestClass(TestCase):
    def test_average_value_column_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> business_operations_survey_23044745avg.csv
        name = "business_operations_survey_23044745avg.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)
        column = "value"

        try:
            result = AverageValue().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

            self.assertEqual(result.metric_name, "AverageValue")
            self.assertEqual(result.value, 23044745)
            print(f"OK {name.ljust(60)} column: {column}")
        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError


    def test_average_value_column_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> food_price_september_963avg.csv
        name = "food_price_september_963avg.csv"
        file_path = os.path.join("..", "Test_files", "CSV_cases", name)
        column = "Data_value"

        try:
            result = AverageValue().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

            self.assertEqual(result.metric_name, "AverageValue")
            self.assertEqual(result.value, 963)
            print(f"OK {name.ljust(60)} column: {column}")
        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_average_value_column_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> sales_10rows_104avg.parquet
        name = "sales_10rows_104avg.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)
        column = "stock"
        try:
            result = AverageValue().calculate(data=pd.read_parquet(file_path), column=column)

            self.assertEqual(result.metric_name, "AverageValue")
            self.assertEqual(result.value, 104)
            print(f"OK {name.ljust(60)} column: {column}")
        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_average_value_column_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> complects_3empty_3unique_6avg.parquet
        name = "complects_3empty_3unique_6avg.parquet"
        file_path = os.path.join("..", "Test_files", "Parquet_cases", name)
        column = "price"
        try:
            result = AverageValue().calculate(data=pd.read_parquet(file_path), column=column)

            self.assertEqual(result.metric_name, "AverageValue")
            self.assertEqual(result.value, 6)
            print(f"OK {name.ljust(60)} column: {column}")
        except AssertionError:
            print(f"Fail {name.ljust(60)} column: {column}")
            raise AssertionError

    def test_average_value_column_Json_case1(self):
        # Path to Test_files -> Json_cases -> company_5avg.json
        name = "company_5avg.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$[*].company.departments[*].employees[*].performance.2024.projects_completed"
        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = AverageValueJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "AverageValue")
            self.assertEqual(result.value, 7)
            print(f"OK {name.ljust(60)} path: {path}")
        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError

    def test_average_value_column_Json_case2(self):
        # Path to Test_files -> Json_cases -> Gurteen_weather_4empty_5defined_90avg.json
        name = "Gurteen_weather_4empty_5defined_90avg.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$[*].humidity"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = AverageValueJson().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "AverageValue")
            self.assertEqual(result.value, 90)
            print(f"OK {name.ljust(60)} path: {path}")
        except AssertionError:
            print(f"Fail {name.ljust(60)} path: {path}")
            raise AssertionError