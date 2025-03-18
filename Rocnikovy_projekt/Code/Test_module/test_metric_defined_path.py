import json
from unittest import TestCase

from src.metric import DefinedPathCount

class TestClass(TestCase):

    def test_defined_count_Json_case1(self):
        # Path to Test_files -> Json_cases -> Gurteen_weather_4empty_5defined_90avg.json
        file_path = r"..\..\Test_files\Json_cases\Gurteen_weather_4empty_5defined_90avg.json"
        path = "$.temperature"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = DefinedPathCount().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "DefinedPathCount")
        self.assertEqual(result.value, 3)

    def test_defined_count_Json_case2(self):
        # Path to Test_files -> Json_cases -> gas_supply_24empty_9nullcol_4defined.json
        file_path = r"..\..\Test_files\Json_cases\gas_supply_24empty_9nullcol_4defined.json"
        path = "$.Corrib production"

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = DefinedPathCount().calculate(data=loaded_data, column=path)

        self.assertEqual(result.metric_name, "DefinedPathCount")
        self.assertEqual(result.value, 4)

