import json
import os
import trace
from unittest import TestCase

from src.metric import DefinedPathCount

class TestClass(TestCase):

    def test_defined_count_Json_case1(self):
        # Path to Test_files -> Json_cases -> Gurteen_weather_4empty_3defined_90avg.json
        name = "Gurteen_weather_4empty_3defined_90avg.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$[*].temperature"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = DefinedPathCount().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "DefinedPathCount")
            self.assertEqual(result.value, 3)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

    def test_defined_count_Json_case2(self):
        # Path to Test_files -> Json_cases -> gas_supply_22empty_7nullcol_4defined.json
        name = "gas_supply_22empty_7nullcol_4defined.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)
        path = "$[*][\"Corrib production\"]"

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = DefinedPathCount().calculate(data=loaded_data, column=path)

            self.assertEqual(result.metric_name, "DefinedPathCount")
            self.assertEqual(result.value, 4)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError
