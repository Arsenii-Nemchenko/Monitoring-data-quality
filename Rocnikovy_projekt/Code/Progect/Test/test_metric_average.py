import json
import pandas as pd
from unittest import TestCase

from Progect.metric import AverageValueJson, AverageValue

class TestClass(TestCase):
    def test_average_value_column_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> business_operations_survey_23044745avg.csv
        file_path = input("Enter path to business_operations_survey_23044745avg.csv: ")
        column = "value"

        result = AverageValue().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

        self.assertEqual(result.metric_name, "AverageValue")
        self.assertEqual(result.value, 23044745)

    def test_average_value_column_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> food_price_september_963avg.csv
        file_path = input("Enter path to food_price_september_963.csv: ")
        column = "Data_value"

        result = AverageValue().calculate(data=pd.read_csv(file_path, index_col=False), column=column)

        self.assertEqual(result.metric_name, "AverageValue")
        self.assertEqual(result.value, 963)

    def test_average_value_column_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> sales_10rows_104avg.parquet
        file_path = input("Enter path to sales_10rows_104avg.parquet: ")
        column = "stock"

        result = AverageValue().calculate(data=pd.read_parquet(file_path), column=column)

        self.assertEqual(result.metric_name, "AverageValue")
        self.assertEqual(result.value, 104)

    def test_average_value_column_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> complects_3empty_3unique_6avg.parquet
        file_path = input("Enter path to complects_3empty_3unique_6avg.parquet: ")
        column = "price"

        result = AverageValue().calculate(data=pd.read_parquet(file_path), column=column)

        self.assertEqual(result.metric_name, "AverageValue")
        self.assertEqual(result.value, 6)

    def test_average_value_column_Json_case1(self):
        # Path to Test_files -> Json_cases -> company_5avg.json
        file_path = input("Enter path to company_5avg.json: ")
        path = "$.company.departments.employees.performance.2024.projects_completed"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = AverageValueJson().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "AverageValue")
        self.assertEqual(result.value, 5)

    def test_average_value_column_Json_case2(self):
        # Path to Test_files -> Json_cases -> Gurteen_weather_4empty_5defined_90avg.json
        file_path = input("Enter path to Gurteen_weather_4empty_5defined_90avg.json: ")
        path = "$.humidity"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = AverageValueJson().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "AverageValue")
        self.assertEqual(result.value, 90)