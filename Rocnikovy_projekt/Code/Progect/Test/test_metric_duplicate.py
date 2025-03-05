import tempfile
import pandas as pd
import json
from unittest import TestCase

from Progect.metric import DuplicateRecordCount

class TestClass(TestCase):

    def test_duplicate_count_CSV_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("""
"model","mpg","cyl","disp","hp","drat","wt","qsec","vs","am","gear","carb"
"Mazda RX4",21,6,160,110,3.9,2.62,16.46,0,1,4,4
"Mazda RX4 Wag",21,6,160,110,3.9,2.875,17.02,0,1,4,4
"Datsun 710",22.8,4,108,93,3.85,2.32,18.61,1,1,4,1
"Hornet 4 Drive",21.4,6,258,110,3.08,3.215,19.44,1,0,3,1
"Hornet Sportabout",18.7,8,360,175,3.15,3.44,17.02,0,0,3,2
"Valiant",18.1,6,225,105,2.76,3.46,20.22,1,0,3,1
"Duster 360",14.3,8,360,245,3.21,3.57,15.84,0,0,3,4
"Merc 240D",24.4,4,146.7,62,3.69,3.19,20,1,0,4,2
"Merc 230",22.8,4,140.8,95,3.92,3.15,22.9,1,0,4,2
"Merc 280",19.2,6,167.6,123,3.92,3.44,18.3,1,0,4,4
"Merc 280C",17.8,6,167.6,123,3.92,3.44,18.9,1,0,4,4
"Merc 450SE",16.4,8,275.8,180,3.07,4.07,17.4,0,0,3,3
"Merc 450SL",17.3,8,275.8,180,3.07,3.73,17.6,0,0,3,3
"Merc 450SLC",15.2,8,275.8,180,3.07,3.78,18,0,0,3,3
"Cadillac Fleetwood",10.4,8,472,205,2.93,5.25,17.98,0,0,3,4
"Lincoln Continental",10.4,8,460,215,3,5.424,17.82,0,0,3,4
"Chrysler Imperial",14.7,8,440,230,3.23,5.345,17.42,0,0,3,4
"Fiat 128",32.4,4,78.7,66,4.08,2.2,19.47,1,1,4,1
"Honda Civic",30.4,4,75.7,52,4.93,1.615,18.52,1,1,4,2
"Toyota Corolla",33.9,4,71.1,65,4.22,1.835,19.9,1,1,4,1
"Toyota Corona",21.5,4,120.1,97,3.7,2.465,20.01,1,0,3,1
"Dodge Challenger",15.5,8,318,150,2.76,3.52,16.87,0,0,3,2
"AMC Javelin",15.2,8,304,150,3.15,3.435,17.3,0,0,3,2
"Camaro Z28",13.3,8,350,245,3.73,3.84,15.41,0,0,3,4
"Camaro Z28",13.3,8,350,245,3.73,3.84,15.41,0,0,3,4
"Pontiac Firebird",19.2,8,400,175,3.08,3.845,17.05,0,0,3,2
"Fiat X1-9",27.3,4,79,66,4.08,1.935,18.9,1,1,4,1
"Porsche 914-2",26,4,120.3,91,4.43,2.14,16.7,0,1,5,2
"Lotus Europa",30.4,4,95.1,113,3.77,1.513,16.9,1,1,5,2
"Ford Pantera L",15.8,8,351,264,4.22,3.17,14.5,0,1,5,4
"Ferrari Dino",19.7,6,145,175,3.62,2.77,15.5,0,1,5,6
"Maserati Bora",15,8,301,335,3.54,3.57,14.6,0,1,5,8
"Volvo 142E",21.4,4,121,109,4.11,2.78,18.6,1,1,4,2
"Volvo 142E",21.4,4,121,109,4.11,2.78,18.6,1,1,4,2
"Volvo 142E",21.4,4,121,109,4.11,2.78,18.6,1,1,4,2
"Volvo 142E",21.4,4,121,109,4.11,2.78,18.6,1,1,4,2
"Volvo 142E",21.4,4,121,109,4.11,2.78,18.6,1,1,4,2
,,,,,,,,,,,
,,,,,,,,,,,
,,,,,,,,,,,
    """)
        temp_file_path = temp_file.name

        result = DuplicateRecordCount().calculate(data=pd.read_csv(temp_file_path))
        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 5)

    def test_duplicate_count_CSV_case2(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("""
"price","area","bedrooms","bathrooms","stories","mainroad","guestroom","basement","hotwaterheating","airconditioning","parking","prefarea","furnishingstatus"
13300000,7420,4,2,3,"yes","no","no","no","yes",2,"yes","furnished"
12250000,8960,4,4,4,"yes","no","no","no","yes",3,"no","furnished"
,,,,,,,,,,,,
,,,,,,,,,,,,
,,,,,,,,,,,,
,,,,,,,,,,,,
12250000,9960,3,2,2,"yes","no","yes","no","no",2,"yes","semi-furnished"
12215000,7500,4,2,2,"yes","no","yes","no","yes",3,"yes","furnished"
11410000,7420,4,1,2,"yes","yes","yes","no","yes",2,"no","furnished"
10850000,7500,3,3,1,"yes","no","yes","no","yes",2,"yes","semi-furnished"
10150000,8580,4,3,4,"yes","no","no","no","yes",2,"yes","semi-furnished"
10150000,16200,5,3,2,"yes","no","no","no","no",0,"no","unfurnished"
9870000,8100,4,1,2,"yes","yes","yes","no","yes",2,"yes","furnished"
9800000,5750,3,2,4,"yes","yes","no","no","yes",1,"yes","unfurnished"
9800000,13200,3,1,2,"yes","no","yes","no","yes",2,"yes","furnished"
9681000,6000,4,3,2,"yes","yes","yes","yes","no",2,"no","semi-furnished"
9310000,6550,4,2,2,"yes","no","no","no","yes",1,"yes","semi-furnished"
9240000,3500,4,2,2,"yes","no","no","yes","no",2,"no","furnished"
9240000,7800,3,2,2,"yes","no","no","no","no",0,"yes","semi-furnished"
9100000,6000,4,1,2,"yes","no","yes","no","no",2,"no","semi-furnished"
9100000,6600,4,2,2,"yes","yes","yes","no","yes",1,"yes","unfurnished"
8960000,8500,3,2,4,"yes","no","no","no","yes",2,"no","furnished"
8890000,4600,3,2,2,"yes","yes","no","no","yes",2,"no","furnished"
8855000,6420,3,2,2,"yes","no","no","no","yes",1,"yes","semi-furnished"
8750000,4320,3,1,2,"yes","no","yes","yes","no",2,"no","semi-furnished"
8680000,7155,3,2,1,"yes","yes","yes","no","yes",2,"no","unfurnished"
8645000,8050,3,1,1,"yes","yes","yes","no","yes",1,"no","furnished"
8645000,4560,3,2,2,"yes","yes","yes","no","yes",1,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8575000,8800,3,2,2,"yes","no","no","no","yes",2,"no","furnished"
8540000,6540,4,2,2,"yes","yes","yes","no","yes",2,"yes","furnished"
8463000,6000,3,2,4,"yes","yes","yes","no","yes",0,"yes","semi-furnished"
8400000,8875,3,1,1,"yes","no","no","no","no",1,"no","semi-furnished"
8400000,7950,5,2,2,"yes","no","yes","yes","no",2,"no","unfurnished"
8400000,5500,4,2,2,"yes","no","yes","no","yes",1,"yes","semi-furnished"
8400000,7475,3,2,4,"yes","no","no","no","yes",2,"no","unfurnished"
8400000,7000,3,1,4,"yes","no","no","no","yes",2,"no","semi-furnished"
8295000,4880,4,2,2,"yes","no","no","no","yes",1,"yes","furnished"
8190000,5960,3,3,2,"yes","yes","yes","no","no",1,"no","unfurnished"
8120000,6840,5,1,2,"yes","yes","yes","no","yes",1,"no","furnished"
8080940,7000,3,2,4,"yes","no","no","no","yes",2,"no","furnished"
8043000,7482,3,2,3,"yes","no","no","yes","no",1,"yes","furnished"
7980000,9000,4,2,4,"yes","no","no","no","yes",2,"no","furnished"
7962500,6000,3,1,4,"yes","yes","no","no","yes",2,"no","unfurnished"
7910000,6000,4,2,4,"yes","no","no","no","yes",1,"no","semi-furnished"
7875000,6550,3,1,2,"yes","no","yes","no","yes",0,"yes","furnished"
7840000,6360,3,2,4,"yes","no","no","no","yes",0,"yes","furnished"
7700000,6480,3,2,4,"yes","no","no","no","yes",2,"no","unfurnished"
7700000,6000,4,2,4,"yes","no","no","no","no",2,"no","semi-furnished"
7560000,6000,4,2,4,"yes","no","no","no","yes",1,"no","furnished"
7560000,6000,3,2,3,"yes","no","no","no","yes",0,"no","semi-furnished"
7525000,6000,3,2,4,"yes","no","no","no","yes",1,"no","furnished"
7490000,6600,3,1,4,"yes","no","no","no","yes",3,"yes","furnished"
7455000,4300,3,2,2,"yes","no","yes","no","no",1,"no","unfurnished"
7420000,7440,3,2,1,"yes","yes","yes","no","yes",0,"yes","semi-furnished"
7420000,7440,3,2,4,"yes","no","no","no","no",1,"yes","unfurnished"
    """)
        temp_file_path = temp_file.name

        result = DuplicateRecordCount().calculate(data=pd.read_csv(temp_file_path))
        self.assertEqual(result.metric_name, "DuplicateCount")
        self.assertEqual(result.value, 12)

    def test_record_count_Parquet_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name

            df = pd.json_normalize([{'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'M4A1-S', 'skin': 'Hyper Beast'},
                     'secondary': {'weapon': 'Glock-18', 'skin': 'Water Elemental'},
                     'knife': {'weapon': 'Bayonet', 'skin': 'Crimson Web'},
                     'grenades': [{'name': 'Molotov'}, {'name': 'Smoke'}, {'name': 'Decoy'}]},
                    {'primary': {'weapon': 'AWP', 'skin': 'Dragon Lore'},
                     'secondary': {'weapon': 'P250', 'skin': 'Mehndi'},
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
                     'grenades': [{'name': 'Molotov'}, None, {'name': 'Smoke'}]}, None, None])

            df.to_parquet(temp_file_path, index=False)

            result = DuplicateRecordCount().calculate(data=pd.read_parquet(temp_file_path))
            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 12)

    def test_record_count_Parquet_case2(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name

            df = pd.json_normalize([{
      "name": "San Francisco Farmers Market",
      "city": "San Francisco",
      "type": "Farmers Market",
      "address": "",
      "opening_hours": "8 AM - 2 PM",
      "products": ["Fruits", "Vegetables", None, "Baked Goods"]
    },
    {},
    {},
    {
      "name": "Los Angeles Grand Central Market",
      "city": "",
      "type": "Public Market",
      "address": "317 S Broadway, Los Angeles, CA 90013",
      "opening_hours": None,
      "products": ["Seafood", "Meat", "Spices", "Street Food"]
    },
                {
                    "name": "Los Angeles Grand Central Market",
                    "city": "",
                    "type": "Public Market",
                    "address": "317 S Broadway, Los Angeles, CA 90013",
                    "opening_hours": None,
                    "products": ["Seafood", "Meat", "Spices", "Street Food"]
                },
                {
                    "name": "Los Angeles Grand Central Market",
                    "city": "",
                    "type": "Public Market",
                    "address": "317 S Broadway, Los Angeles, CA 90013",
                    "opening_hours": None,
                    "products": ["Seafood", "Meat", "Spices", "Street Food"]
                },
                {
                    "name": "Los Angeles Grand Central Market",
                    "city": "",
                    "type": "Public Market",
                    "address": "317 S Broadway, Los Angeles, CA 90013",
                    "opening_hours": None,
                    "products": ["Seafood", "Meat", "Spices", "Street Food"]
                },
    {
      "name": None,
      "city": "Dallas",
      "type": "Farmers Market",
      "address": "920 S Harwood St, Dallas, TX 75201",
      "opening_hours": "9 AM - 5 PM",
      "products": ["Organic Produce", "", "Flowers", "Honey"]
    },
    {
      "name": "Austin SFC Farmers' Market",
      "city": "Austin",
      "type": None,
      "address": "422 Guadalupe St, Austin, TX 78701",
      "opening_hours": "9 AM - 1 PM",
      "products": ["Grass-fed Meat", "Eggs", "Handmade Goods"]
    },
    {
      "name": "Union Square Greenmarket",
      "city": "New York",
      "type": "Farmers Market",
      "address": "",
      "opening_hours": "8 AM - 6 PM",
      "products": ["Fresh Produce", "Wine", "Plants", None]
    },
    {
      "name": "Chelsea Market",
      "city": "New York",
      "type": "Public Market",
      "address": "75 9th Ave, New York, NY 10011",
      "opening_hours": "",
      "products": [None, "Gourmet Cheese", "Seafood"]
    },
                {
                    "name": "Chelsea Market",
                    "city": "New York",
                    "type": "Public Market",
                    "address": "75 9th Ave, New York, NY 10011",
                    "opening_hours": "",
                    "products": [None, "Gourmet Cheese", "Seafood"]
                },
                {
                    "name": "Chelsea Market",
                    "city": "New York",
                    "type": "Public Market",
                    "address": "75 9th Ave, New York, NY 10011",
                    "opening_hours": "",
                    "products": [None, "Gourmet Cheese", "Seafood"]
                },
                {
                    "name": "Chelsea Market",
                    "city": "New York",
                    "type": "Public Market",
                    "address": "75 9th Ave, New York, NY 10011",
                    "opening_hours": "",
                    "products": [None, "Gourmet Cheese", "Seafood"]
                },
                {
                    "name": "Chelsea Market",
                    "city": "New York",
                    "type": "Public Market",
                    "address": "75 9th Ave, New York, NY 10011",
                    "opening_hours": "",
                    "products": [None, "Gourmet Cheese", "Seafood"]
                },
                {
                    "name": "Chelsea Market",
                    "city": "New York",
                    "type": "Public Market",
                    "address": "75 9th Ave, New York, NY 10011",
                    "opening_hours": "",
                    "products": [None, "Gourmet Cheese", "Seafood"]
                },
    None,
    None])

            df.to_parquet(temp_file_path, index=False)

            result = DuplicateRecordCount().calculate(data=pd.read_parquet(temp_file_path))
            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 8)


    def test_duplicate_Json_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name
            data = [{'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'AK-47', 'skin': 'Asiimov'},
                     'secondary': {'weapon': 'Desert Eagle', 'skin': 'Blaze'},
                     'knife': {'weapon': 'Karambit', 'skin': 'Fade'},
                     'grenades': [None, {'name': 'HE Grenade'}, {'name': 'Smoke'}]},
                    {'primary': {'weapon': 'M4A1-S', 'skin': 'Hyper Beast'},
                     'secondary': {'weapon': 'Glock-18', 'skin': 'Water Elemental'},
                     'knife': {'weapon': 'Bayonet', 'skin': 'Crimson Web'},
                     'grenades': [{'name': 'Molotov'}, {'name': 'Smoke'}, {'name': 'Decoy'}]},
                    {'primary': {'weapon': 'AWP', 'skin': 'Dragon Lore'},
                     'secondary': {'weapon': 'P250', 'skin': 'Mehndi'},
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
                loaded_data = pd.json_normalize(loaded_data)
            result = DuplicateRecordCount().calculate(data=loaded_data)

            self.assertEqual(result.metric_name, "DuplicateCount")
            self.assertEqual(result.value, 12)

    def test_duplicate_Json_case2(self):
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


                with open(temp_file_path, 'w') as file:
                    json.dump(data, file)

                with open(temp_file_path, 'r') as file:
                    loaded_data = json.load(file)
                    loaded_data = pd.json_normalize(loaded_data)
                result = DuplicateRecordCount().calculate(data=loaded_data)

                self.assertEqual(result.metric_name, "DuplicateCount")
                self.assertEqual(result.value, 13)