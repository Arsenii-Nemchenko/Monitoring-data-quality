import json
from unittest import TestCase

from Progect.metric import NullObjectCount

class TestClass(TestCase):
    def test_null_object_Json_case1(self):
        # Path to Test_files -> Json_cases -> cs_weapons_12duplicate_19null_19nullcol.json
        file_path = input("Enter path to cs_weapons_12duplicate_19null_19nullcol.json: ")

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = NullObjectCount().calculate(data=loaded_data)

        self.assertEqual(result.metric_name, "NullObjectCount")
        self.assertEqual(result.value, 19)

    def test_null_object_Json_case2(self):
        # Path to Test_files -> Json_cases -> courses_13duplicate_1null.json
        file_path = input("Enter path to courses_13duplicate_1null.json: ")

        with open(file_path, 'r') as file:
            loaded_data = json.load(file)

        result = NullObjectCount().calculate(data=loaded_data)

        self.assertEqual(result.metric_name, "NullObjectCount")
        self.assertEqual(result.value, 1)

