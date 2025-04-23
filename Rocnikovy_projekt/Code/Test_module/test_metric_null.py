import json
import os
from unittest import TestCase

from src.metric import NullObjectCount

class TestClass(TestCase):
    def test_null_object_Json_case1(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_2null_2unique_1nullcol.json
        name = "cs_weapons_12duplicate_2null_2unique_1nullcol.json"
        file_path = os.path.join("..", "Test_files", "Json_cases", name)

        try:
            with open(file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "NullObjectCount")
            self.assertEqual(result.value, 2)
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
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
            print(f"Ok {name.ljust(60)}")

        except AssertionError:
            print(f"Fail {name.ljust(60)}")
            raise AssertionError

