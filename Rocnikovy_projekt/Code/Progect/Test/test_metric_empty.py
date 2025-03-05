from unittest import TestCase
import tempfile
import pandas as pd
import json

from Progect.metric import EmptyObjectCount
from Progect.metric import EmptyRecordCount


class TestClass(TestCase):
    def test_empty_record_count_CSV_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("""
Country or territory name,ISO 2-character country/territory code,ISO 3-character country/territory code,ISO numeric country/territory code,Region,Year,Estimated total population number,Estimated prevalence of TB (all forms) per 100 000 population,"Estimated prevalence of TB (all forms) per 100 000 population, low bound","Estimated prevalence of TB (all forms) per 100 000 population, high bound",Estimated prevalence of TB (all forms),"Estimated prevalence of TB (all forms), low bound","Estimated prevalence of TB (all forms), high bound",Method to derive prevalence estimates,"Estimated mortality of TB cases (all forms, excluding HIV) per 100 000 population","Estimated mortality of TB cases (all forms, excluding HIV), per 100 000 population, low bound","Estimated mortality of TB cases (all forms, excluding HIV), per 100 000 population, high bound","Estimated number of deaths from TB (all forms, excluding HIV)","Estimated number of deaths from TB (all forms, excluding HIV), low bound","Estimated number of deaths from TB (all forms, excluding HIV), high bound","Estimated mortality of TB cases who are HIV-positive, per 100 000 population","Estimated mortality of TB cases who are HIV-positive, per 100 000 population, low bound","Estimated mortality of TB cases who are HIV-positive, per 100 000 population, high bound",Estimated number of deaths from TB in people who are HIV-positive,"Estimated number of deaths from TB in people who are HIV-positive, low bound","Estimated number of deaths from TB in people who are HIV-positive, high bound",Method to derive mortality estimates,Estimated incidence (all forms) per 100 000 population,"Estimated incidence (all forms) per 100 000 population, low bound","Estimated incidence (all forms) per 100 000 population, high bound",Estimated number of incident cases (all forms),"Estimated number of incident cases (all forms), low bound","Estimated number of incident cases (all forms), high bound",Method to derive incidence estimates,Estimated HIV in incident TB (percent),"Estimated HIV in incident TB (percent), low bound","Estimated HIV in incident TB (percent), high bound",Estimated incidence of TB cases who are HIV-positive per 100 000 population,"Estimated incidence of TB cases who are HIV-positive per 100 000 population, low bound","Estimated incidence of TB cases who are HIV-positive per 100 000 population, high bound",Estimated incidence of TB cases who are HIV-positive,"Estimated incidence of TB cases who are HIV-positive, low bound","Estimated incidence of TB cases who are HIV-positive, high bound",Method to derive TBHIV estimates,"Case detection rate (all forms), percent","Case detection rate (all forms), percent, low bound","Case detection rate (all forms), percent, high bound"
Afghanistan,AF,AFG,4,EMR,1990,11731193,306,156,506,36000,18000,59000,predicted,37,24,54,4300,2800,6400,0.04,0.03,0.05,5,4.1,6,Indirect,189,157,238,22000,18000,28000,,0.06,0.04,0.08,0.11,0.08,0.14,12,9.4,16,,20,15,24
Afghanistan,AF,AFG,4,EMR,1991,12612043,343,178,562,43000,22000,71000,predicted,46,29,61,5800,3700,7700,0.06,0.05,0.08,8,6.2,10,Indirect,191,167,227,24000,21000,29000,,0.07,0.06,0.09,0.13,0.11,0.16,17,14,20,,96,80,110
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Afghanistan,AF,AFG,4,EMR,1992,13811876,371,189,614,51000,26000,85000,predicted,54,34,68,7400,4700,9400,0.08,0.06,0.1,11,8.3,14,Indirect,191,171,217,26000,24000,30000,,0.08,0.07,0.1,0.16,0.14,0.18,22,19,24,,,,
Afghanistan,AF,AFG,4,EMR,1993,15175325,392,194,657,59000,30000,100000,predicted,60,38,73,9100,5800,11000,0.11,0.09,0.14,17,13,21,Indirect,189,171,209,29000,26000,32000,,0.1,0.09,0.11,0.19,0.17,0.21,28,25,31,,,,
Afghanistan,AF,AFG,4,EMR,1994,16485018,410,198,697,68000,33000,110000,predicted,65,41,79,11000,6800,13000,0.13,0.11,0.16,22,17,27,Indirect,188,169,208,31000,28000,34000,,0.11,0.1,0.13,0.21,0.18,0.24,35,30,39,,,,
Afghanistan,AF,AFG,4,EMR,1995,17586073,424,199,733,75000,35000,130000,predicted,69,45,82,12000,7800,14000,0.15,0.12,0.19,27,21,34,Indirect,188,166,209,33000,29000,37000,,0.12,0.1,0.15,0.23,0.21,0.27,41,37,47,,,,
Afghanistan,AF,AFG,4,EMR,1996,18415307,438,202,764,81000,37000,140000,predicted,71,48,85,13000,8900,16000,0.17,0.14,0.21,32,26,39,Indirect,188,169,206,35000,31000,38000,,0.14,0.12,0.16,0.25,0.23,0.28,47,42,52,,,,
""")
        temp_file_path = temp_file.name

        result = EmptyRecordCount().calculate(data=pd.read_csv(temp_file_path))
        self.assertEqual(result.metric_name, "EmptyRecordCount")
        self.assertEqual(result.value, 10)

    def test_empty_record_count_CSV_case2(self):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file.write("""
Country Code,Country Name,Year,Age Group,Sex,Number of Deaths,"Death Rate Per 100,000"
AFG,,,,,,
AFG,,,,,,
AFG,,,,,,
AFG,Afghanistan,1970,0-6 days,Male,"19,241","318,292.90"
AFG,Afghanistan,1970,0-6 days,Female,"12,600","219,544.20"
AFG,Afghanistan,1970,0-6 days,Both,"31,840","270,200.70"
AFG,Afghanistan,1970,7-27 days,Male,"15,939","92,701.00"
AFG,Afghanistan,1970,7-27 days,Female,"11,287","68,594.50"
,,,,,,"67,3"
AFG,Afghanistan,1970,7-27 days,Both,"27,226","80,912.50"
AFG,Afghanistan,1970,28-364 days,Male,"37,513","15,040.10"
AFG,Afghanistan,1970,28-364 days,Female,"32,113","13,411.80"
AFG,Afghanistan,1970,28-364 days,Both,"69,626","14,242.60"
AFG,Afghanistan,1970,1-4 years,Male,"36,694","4,288.20"
,,,,,,
,,,,,,
,,,,,,
,,,,,,
AFG,Afghanistan,1970,1-4 years,Female,"32,848","4,022.90"
AFG,Afghanistan,1970,1-4 years,Both,"69,542","4,158.60"
AFG,Afghanistan,1970,5-9 years,Male,"3,467",396.2
AFG,Afghanistan,1970,5-9 years,Female,"2,492",306
AFG,Afghanistan,1970,5-9 years,Both,"5,959",352.7
AFG,Afghanistan,1970,10-14 years,Male,"1,723",230.8
AFG,Afghanistan,1970,10-14 years,Female,"1,806",262.3
AFG,Afghanistan,1970,10-14 years,Both,"3,529",245.9
AFG,Afghanistan,1970,15-19 years,Male,"1,816",282.9
AFG,Afghanistan,1970,15-19 years,Female,"1,902",324.7
AFG,Afghanistan,1970,15-19 years,Both,"3,718",302.8
AFG,Afghanistan,1970,20-24 years,Male,"2,240",392.9
,,,,,,
,,,,,,
,,,,,,
,,,,,,
AFG,Afghanistan,1970,20-24 years,Female,"2,630",508.4""")
            temp_file_path = temp_file.name

            result = EmptyRecordCount().calculate(data=pd.read_csv(temp_file_path))
            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 8)

    def test_empty_record_count_Parquet_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name

            df = pd.DataFrame([
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": 102, "name": "", "category": "Fruits", "price": 0.3, "stock": 200,
     "variants": ["Yellow"], "suppliers": [{"name": "Supplier C", "rating": 4.3}]},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None},
    {"product_id": None, "name": None, "category": None, "price": None, "stock": None,
     "variants": None, "suppliers": None}
])

            df.to_parquet(temp_file_path, index=False)

            result = EmptyRecordCount().calculate(data=pd.read_parquet(temp_file_path))
            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 9)


    def test_empty_record_count_Parquet_case2(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name
            df = pd.json_normalize([
                {
                    "complect_id": None,
                    "name": "",
                    "category": None,
                    "price": None,
                    "products": "",
                    "discount": None
                },
                None,
                {
                    "complect_id": 201,
                    "name": "Breakfast Set",
                    "category": "Food Bundles",
                    "price": 5.5,
                    "products": None,
                    "discount": 0.1
                },
                {
                    "complect_id": 202,
                    "name": "",
                    "category": "Food Bundles",
                    "price": 3.8,
                    "products": None,
                    "discount": 0.05
                },
                {
                    "complect_id": None,
                    "name": "",
                    "category": "",
                    "price": None,
                    "products": None,
                    "discount": None
                },
                {
                    "complect_id": 204,
                    "name": "Italian Dinner Set",
                    "category": "Food Bundles",
                    "price": None,
                    "products": None,
                    "discount": 0.1
                },
                {
                    "complect_id": 205,
                    "name": "Vegetarian Essentials",
                    "category": "Healthy Eating",
                    "price": 9.0,
                    "products": None,
                    "discount": 0.08
                }
])
            df.to_parquet(temp_file_path, index=False)

            result = EmptyRecordCount().calculate(data=pd.read_parquet(temp_file_path))
            self.assertEqual(result.metric_name, "EmptyRecordCount")
            self.assertEqual(result.value, 3)

    def test_empty_record_count_Json_case1(self):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file_path = temp_file.name

                data = [
  {
    "Date": "01/01/2018",
    "Corrib production": 102.065496,
    "Moffat": None,
    "ROI imports via interconnector": "",
    "Total": 200.528802
  },
  {
    "Date": "02/01/2018",
    "Corrib production": "",
    "Moffat": 72.3,
    "ROI imports via interconnector": None,
    "Total": 204.880714
  },
  {},
  {},
  {
    "Date": "05/01/2018",
    "Corrib production": 101.724944,
    "Moffat": 127.9,
    "ROI imports via interconnector": "",
    "Total": None
  },
  {},
  {},
  {
    "Date": "08/01/2018",
    "Corrib production": None,
    "Moffat": 134.066667,
    "ROI imports via interconnector": 78.485538,
    "Total": 314.17579
  },
  {},
  {
    "Date": "10/01/2018",
    "Corrib production": "",
    "Moffat": 151.677778,
    "ROI imports via interconnector": 91.159686,
    "Total": 344.455045
  },
  {},
  {},
  {
    "Date": "14/01/2018",
    "Corrib production": None,
    "Moffat": "",
    "ROI imports via interconnector": None,
    "Total": None
  },
  {},
  {
    "Date": "16/01/2018",
    "Corrib production": None,
    "Moffat": None,
    "ROI imports via interconnector": None,
    "Total": None
  },
  {},
  {},
  {},
  {
    "Date": "21/01/2018",
    "Corrib production": None,
    "Moffat": None,
    "ROI imports via interconnector": None,
    "Total": None
  },
  {},
  {},
  {},
  {},
  {
    "Date": "26/01/2018",
    "Corrib production": 100.334303,
    "Moffat": "",
    "ROI imports via interconnector": None,
    "Total": 299.159626
  },
  {},
  {
    "Date": "28/01/2018",
    "Corrib production": None,
    "Moffat": None,
    "ROI imports via interconnector": None,
    "Total": None
  },
  {},
  {},
  {},
  {
    "Date": "02/02/2018",
    "Corrib production": None,
    "Moffat": None,
    "ROI imports via interconnector": None,
    "Total": None
  },
  {},
  {},
  {},
  {
    "Date": "07/02/2018",
    "Corrib production": 99.340602,
    "Moffat": 158.488889,
    "ROI imports via interconnector": "",
    "Total": None
  },
  None,
  None
]

                with open(temp_file_path, 'w') as file:
                    json.dump(data, file)

                with open(temp_file_path, 'r') as file:
                    loaded_data = json.load(file)
                result = EmptyObjectCount().calculate(data=loaded_data)
                # Todo
                self.assertEqual(result.metric_name, "EmptyRecordCount")
                self.assertEqual(result.value, 24)


    def test_empty_record_count_Json_case2(self):
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file_path = temp_file.name

                data = [{
                            "name": "Gurteen",
                            "temperature": "2",
                            "symbol": "02n",
                            "weatherDescription": "Fair",
                            "text": "\"Fair\"",
                            "windSpeed": "15",
                            "windGust": "-",
                            "cardinalWindDirection": "W",
                            "windDirection": 270,
                            "humidity": " 87 ",
                            "rainfall": " 0.0 ",
                            "pressure": "1021",
                            "dayName": "Thursday",
                            "date": "27-02-2025",
                            "reportTime": "00:00"
                        },
                        {
                            "name": "",
                            "temperature": "",
                            "symbol": "",
                            "weatherDescription": "",
                            "text": "",
                            "windSpeed": "",
                            "windGust": "",
                            "cardinalWindDirection": "",
                            "windDirection": "",
                            "humidity": "",
                            "rainfall": "",
                            "pressure": "",
                            "dayName": "",
                            "date": "",
                            "reportTime": ""
                        },
                        {
                            "name": "Gurteen",
                            "temperature": "1",
                            "symbol": "02n",
                            "weatherDescription": "Fair",
                            "text": "\"Fair\"",
                            "windSpeed": "7",
                            "windGust": "-",
                            "cardinalWindDirection": "W",
                            "windDirection": 270,
                            "humidity": " 90 ",
                            "rainfall": " 0.0 ",
                            "pressure": "1021",
                            "dayName": "Thursday",
                            "date": "27-02-2025",
                            "reportTime": "02:00"
                        },
                        {
                            "name": "",
                            "temperature": "",
                            "symbol": "",
                            "weatherDescription": "",
                            "text": "",
                            "windSpeed": "",
                            "windGust": "",
                            "cardinalWindDirection": "",
                            "windDirection": "",
                            "humidity": "",
                            "rainfall": "",
                            "pressure": "",
                            "dayName": "",
                            "date": "",
                            "reportTime": ""
                        },
                        {
                            "name": "Gurteen",
                            "temperature": "0",
                            "symbol": "02n",
                            "weatherDescription": "Fair",
                            "text": "\"Fair\"",
                            "windSpeed": "7",
                            "windGust": "-",
                            "cardinalWindDirection": "SW",
                            "windDirection": 225,
                            "humidity": " 93 ",
                            "rainfall": " 0.0 ",
                            "pressure": "1022",
                            "dayName": "Thursday",
                            "date": "27-02-2025",
                            "reportTime": "04:00"
                        },
                        {
                            "name": "",
                            "temperature": "",
                            "symbol": "",
                            "weatherDescription": "",
                            "text": "",
                            "windSpeed": "",
                            "windGust": "",
                            "cardinalWindDirection": "",
                            "windDirection": "",
                            "humidity": "",
                            "rainfall": "",
                            "pressure": "",
                            "dayName": "",
                            "date": "",
                            "reportTime": ""
                        },
                        None
                    ]

                with open(temp_file_path, 'w') as file:
                    json.dump(data, file)

                with open(temp_file_path, 'r') as file:
                    loaded_data = json.load(file)
                result = EmptyObjectCount().calculate(data=loaded_data)

                self.assertEqual(result.metric_name, "EmptyRecordCount")
                self.assertEqual(result.value, 4)
