import json
import os
from unittest import TestCase

from src.metric import NullObjectCount

class TestClass(TestCase):
    def test_null_object_Json_case1(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_19null_19nullcol.json
        name = "cs_weapons_12duplicate_19null_19nullcol.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "NullObjectCount")
            self.assertEqual(result.value, 19)
            print(f"Ok {name}")

        except AssertionError:
            print(f"Fail {name}")
            raise AssertionError


    def test_null_object_Json_case2(self):
        # Path to Test_files -> Json_cases -> courses_13duplicate_1null_6unique.json
        name = "courses_13duplicate_1null_6unique.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "NullObjectCount")
            self.assertEqual(result.value, 1)
            print(f"Ok {name}")

        except AssertionError:
            print(f"Fail {name}")
            raise AssertionError

