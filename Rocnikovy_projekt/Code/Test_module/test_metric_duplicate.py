import pandas as pd
import json
from unittest import TestCase

from src.metric import DuplicateRecordCount

class TestClass(TestCase):

    def test_duplicate_count_CSV_case1(self):
        #Path to Test_files -> CSV_cases -> cars_37rows_3empty_4duplicate.csv
        file_path = r"..\..\Test_files\CSV_cases\cars_37rows_3empty_4duplicate.csv"

        result = DuplicateRecordCount().calculate(data=pd.read_csv(file_path))
        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 5)

    def test_duplicate_count_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> house_price_557rows_12duplicate.csv
        file_path = r"..\..\Test_files\CSV_cases\house_price_557rows_12duplicate.csv"

        result = DuplicateRecordCount().calculate(data=pd.read_csv(file_path))
        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 12)

    def test_duplicate_count_Parquet_case1(self):
        # Path to Test_files -> Parquet_cases -> cs_loadouts_12duplicate.parquet
        file_path = r"..\..\Test_files\Parquet_cases\cs_loadouts_12duplicate.parquet"

        result = DuplicateRecordCount().calculate(data=pd.read_parquet(file_path))
        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 12)

    def test_duplicate_count_Parquet_case2(self):
        # Path to Test_files -> Parquet_cases -> markets_8duplicate_5unique.parquet
        file_path = r"..\..\Test_files\Parquet_cases\markets_8duplicate_5unique.parquet"

        result = DuplicateRecordCount().calculate(data=pd.read_parquet(file_path))
        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 8)


    def test_duplicate_Json_case1(self):
        # Path to Test_files -> JSON_cases -> cs_weapons_12duplicate_19null_19nullcol.json
        file_path = r"..\..\Test_files\Json_cases\cs_weapons_12duplicate_19null_19nullcol.json"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)
            loaded_data = pd.json_normalize(loaded_data)
        result = DuplicateRecordCount().calculate(data=loaded_data)

        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 12)

    def test_duplicate_Json_case2(self):
        # Path to Test_files -> JSON_cases -> courses_13duplicate_1null_6unique.json
        file_path = r"..\..\Test_files\Json_cases\courses_13duplicate_1null_6unique.json"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)
            loaded_data = pd.json_normalize(loaded_data)
            result = DuplicateRecordCount().calculate(data=loaded_data)

        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 13)