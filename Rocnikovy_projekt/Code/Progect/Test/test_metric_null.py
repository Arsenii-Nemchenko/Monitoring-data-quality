import tempfile
import json
from unittest import TestCase

from Progect.metric import NullObjectCount

class TestClass(TestCase):
    def test_null_object_Json_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name
            data = [{'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
              'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'}, 'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'M4A1-S', 'skin': 'Hyper Beast'},
              'secondary': {'weapon': 'Glock-18', 'skin': 'Water Elemental'},
              'knife': {'weapon': 'Bayonet', 'skin': 'Crimson Web'},
              'grenades': [{'name': 'Molotov'}, {'name': 'Smoke'}, {'name': 'Decoy'}]},
             {'primary': {'weapon': 'AWP', 'skin': 'Dragon Lore'}, 'secondary': {'weapon': 'P250', 'skin': 'Mehndi'},
              'knife': {'weapon': 'Butterfly Knife', 'skin': 'Doppler'},
              'grenades': [None, {'name': 'Smoke'}, {'name': 'HE Grenade'}]},
             {'primary': {'weapon': 'FAMAS', 'skin': 'Mecha Industries'},
              'secondary': {'weapon': 'Tec-9', 'skin': 'Fuel Injector'},
              'knife': {'weapon': 'Falchion Knife', 'skin': 'Slaughter'},
              'grenades': [{'name': 'Smoke'}, None, {'name': 'HE Grenade'}]},
             {'primary': {'weapon': 'Galil AR', 'skin': 'Chromatic Aberration'},
              'secondary': {'weapon': 'CZ75-Auto', 'skin': 'Xiangliu'},
              'knife': {'weapon': 'Huntsman Knife', 'skin': 'Tiger Tooth'},
              'grenades': [{'name': 'Molotov'}, {'name': 'Smoke'}, {'name': 'Decoy'}]},
             {'primary': {'weapon': 'MP9', 'skin': 'Rose Iron'},
              'secondary': {'weapon': 'USP-S', 'skin': 'Kill Confirmed'},
              'knife': {'weapon': 'Shadow Daggers', 'skin': 'Crimson Web'},
              'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'SG 553', 'skin': 'Colony IV'},
              'secondary': {'weapon': 'Five-SeveN', 'skin': 'Monkey Business'},
              'knife': {'weapon': 'M9 Bayonet', 'skin': 'Lore'},
              'grenades': [{'name': 'Molotov'}, None, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'SG 553', 'skin': 'Colony IV'},
              'secondary': {'weapon': 'Five-SeveN', 'skin': 'Monkey Business'},
              'knife': {'weapon': 'M9 Bayonet', 'skin': 'Lore'},
              'grenades': [{'name': 'Molotov'}, None, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'SG 553', 'skin': 'Colony IV'},
              'secondary': {'weapon': 'Five-SeveN', 'skin': 'Monkey Business'},
              'knife': {'weapon': 'M9 Bayonet', 'skin': 'Lore'},
              'grenades': [{'name': 'Molotov'}, None, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'SG 553', 'skin': 'Colony IV'},
              'secondary': {'weapon': 'Five-SeveN', 'skin': 'Monkey Business'},
              'knife': {'weapon': 'M9 Bayonet', 'skin': 'Lore'},
              'grenades': [{'name': 'Molotov'}, None, {'name': 'Smoke'}]},
             {'primary': {'weapon': 'SG 553', 'skin': 'Colony IV'},
              'secondary': {'weapon': 'Five-SeveN', 'skin': 'Monkey Business'},
              'knife': {'weapon': 'M9 Bayonet', 'skin': 'Lore'},
              'grenades': [{'name': 'Molotov'}, None, {'name': 'Smoke'}]}, None, None]

            with open(temp_file_path, 'w') as file:
                json.dump(data, file)

            with open(temp_file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "NullObjectCount")
            self.assertEqual(result.value, 19)

    def test_null_object_Json_case2(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name
            data = [
                {
                    "name": "Mathematics",
                    "code": None,
                    "credits": 5,
                    "students": [],
                    "passed%": 45
                },
                {
                    "name": "Physics",
                    "code": "",
                    "credits": None,
                    "students": ["Sara Johnson", "Emma Wilson", "Anna Heineman"],
                    "passed%": 55
                },
                {
                    "name": "",
                    "code": "",
                    "credits": None,
                    "students": None,
                    "passed%": None
                },
                {
                    "name": "",
                    "code": "",
                    "credits": None,
                    "students": None,
                    "passed%": None
                },
                {
                    "name": None,
                    "code": "CHEM205",
                    "credits": 4,
                    "students": None,
                    "passed%": None
                },
                {},
                {
                    "name": "Philosophy",
                    "code": None,
                    "credits": None,
                    "students": ["Brian Adams", "Sophia Martinez", "Emma Wilson", "Lucas Brown"],
                    "passed%": ""
                },
                {},
                {},
                {},
                {
                    "name": "Psychology",
                    "code": "",
                    "credits": 5,
                    "students": ["Brian Adams", "Emily Carter", "Sophia Martinez", "Sara Johnson"],
                    "passed%": None
                },
                {
                    "name": "Psychology",
                    "code": "",
                    "credits": 5,
                    "students": ["Brian Adams", "Emily Carter", "Sophia Martinez", "Sara Johnson"],
                    "passed%": None
                },
                {
                    "name": "Psychology",
                    "code": "",
                    "credits": 5,
                    "students": ["Brian Adams", "Emily Carter", "Sophia Martinez", "Sara Johnson"],
                    "passed%": None
                },
                {
                    "name": "Psychology",
                    "code": "",
                    "credits": 5,
                    "students": ["Brian Adams", "Emily Carter", "Sophia Martinez", "Sara Johnson"],
                    "passed%": None
                },
                {
                    "name": "Art History",
                    "code": None,
                    "credits": "",
                    "students": ["Emily Carter", "Sophia Martinez", "Emma Wilson", "Sara Johnson"],
                    "passed%": 68
                },
                {},
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {
                    "name": "Literature",
                    "code": "LIT140",
                    "credits": None,
                    "students": "",
                    "passed%": 54
                },
                {},
                {
                    "name": "Artificial Intelligence",
                    "code": "AI320",
                    "credits": "",
                    "students": ["Brian Adams", "Sophia Martinez", "Emma Wilson", "Daniel White"],
                    "passed%": 80
                },
                {
                    "name": "Artificial Intelligence",
                    "code": "AI320",
                    "credits": "",
                    "students": ["Brian Adams", "Sophia Martinez", "Emma Wilson", "Daniel White"],
                    "passed%": 80
                },
                {
                    "name": "Artificial Intelligence",
                    "code": "AI320",
                    "credits": "",
                    "students": ["Brian Adams", "Sophia Martinez", "Emma Wilson", "Daniel White"],
                    "passed%": 80
                },
                {
                    "name": "Game Development",
                    "code": None,
                    "credits": None,
                    "students": None,
                    "passed%": None
                },
                {
                    "name": "Game Development",
                    "code": None,
                    "credits": None,
                    "students": None,
                    "passed%": None},
                {
                    "name": "Game Development",
                    "code": None,
                    "credits": None,
                    "students": None,
                    "passed%": None},
                {
                    "name": "Cybersecurity",
                    "code": "CYBER360",
                    "credits": 5,
                    "students": "",
                    "passed%": 67
                },
                None,
                {},
                {
                    "name": "Software Engineering",
                    "code": None,
                    "credits": 5,
                    "students": None,
                    "passed%": None
                }
            ]
            with open(r'C:\Users\Arsen\Desktop\Rocnikovy_projekt\Test_cases_files\Json_cases\courses_1null.json',
                      'w') as f:
                json.dump(data, f)

            with open(temp_file_path, 'w') as file:
                json.dump(data, file)

            with open(temp_file_path, 'r') as file:
                loaded_data = json.load(file)

            result = NullObjectCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "NullObjectCount")
            self.assertEqual(result.value, 1)

