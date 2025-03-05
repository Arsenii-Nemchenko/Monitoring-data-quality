from unittest import TestCase
import tempfile
import pandas as pd

from Progect.metric import RecordCount


class TestClass(TestCase):
    def test_record_count_CSV_case1(self):

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

        result = RecordCount().calculate(data=pd.read_csv(temp_file_path))
        self.assertEqual(result.metric_name, "RecordCount")
        self.assertEqual(result.value, 37)

    def test_record_count_CSV_case2(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write("""
"price","area","bedrooms","bathrooms","stories","mainroad","guestroom","basement","hotwaterheating","airconditioning","parking","prefarea","furnishingstatus"
13300000,7420,4,2,3,"yes","no","no","no","yes",2,"yes","furnished"
12250000,8960,4,4,4,"yes","no","no","no","yes",3,"no","furnished"
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
7420000,6325,3,1,4,"yes","no","no","no","yes",1,"no","unfurnished"
7350000,6000,4,2,4,"yes","yes","no","no","yes",1,"no","furnished"
7350000,5150,3,2,4,"yes","no","no","no","yes",2,"no","semi-furnished"
7350000,6000,3,2,2,"yes","yes","no","no","yes",1,"no","semi-furnished"
7350000,6000,3,1,2,"yes","no","no","no","yes",1,"no","unfurnished"
7343000,11440,4,1,2,"yes","no","yes","no","no",1,"yes","semi-furnished"
7245000,9000,4,2,4,"yes","yes","no","no","yes",1,"yes","furnished"
7210000,7680,4,2,4,"yes","yes","no","no","yes",1,"no","semi-furnished"
7210000,6000,3,2,4,"yes","yes","no","no","yes",1,"no","furnished"
7140000,6000,3,2,2,"yes","yes","no","no","no",1,"no","semi-furnished"
7070000,8880,2,1,1,"yes","no","no","no","yes",1,"no","semi-furnished"
7070000,6240,4,2,2,"yes","no","no","no","yes",1,"no","furnished"
7035000,6360,4,2,3,"yes","no","no","no","yes",2,"yes","furnished"
7000000,11175,3,1,1,"yes","no","yes","no","yes",1,"yes","furnished"
6930000,8880,3,2,2,"yes","no","yes","no","yes",1,"no","furnished"
6930000,13200,2,1,1,"yes","no","yes","yes","no",1,"no","furnished"
6895000,7700,3,2,1,"yes","no","no","no","no",2,"no","unfurnished"
6860000,6000,3,1,1,"yes","no","no","no","yes",1,"no","furnished"
6790000,12090,4,2,2,"yes","no","no","no","no",2,"yes","furnished"
6790000,4000,3,2,2,"yes","no","yes","no","yes",0,"yes","semi-furnished"
6755000,6000,4,2,4,"yes","no","no","no","yes",0,"no","unfurnished"
6720000,5020,3,1,4,"yes","no","no","no","yes",0,"yes","unfurnished"
6685000,6600,2,2,4,"yes","no","yes","no","no",0,"yes","furnished"
6650000,4040,3,1,2,"yes","no","yes","yes","no",1,"no","furnished"
6650000,4260,4,2,2,"yes","no","no","yes","no",0,"no","semi-furnished"
6650000,6420,3,2,3,"yes","no","no","no","yes",0,"yes","furnished"
6650000,6500,3,2,3,"yes","no","no","no","yes",0,"yes","furnished"
6650000,5700,3,1,1,"yes","yes","yes","no","yes",2,"yes","furnished"
6650000,6000,3,2,3,"yes","yes","no","no","yes",0,"no","furnished"
6629000,6000,3,1,2,"yes","no","no","yes","no",1,"yes","semi-furnished"
6615000,4000,3,2,2,"yes","no","yes","no","yes",1,"no","semi-furnished"
6615000,10500,3,2,1,"yes","no","yes","no","yes",1,"yes","furnished"
6580000,6000,3,2,4,"yes","no","no","no","yes",0,"no","semi-furnished"
6510000,3760,3,1,2,"yes","no","no","yes","no",2,"no","semi-furnished"
6510000,8250,3,2,3,"yes","no","no","no","yes",0,"no","furnished"
6510000,6670,3,1,3,"yes","no","yes","no","no",0,"yes","unfurnished"
6475000,3960,3,1,1,"yes","no","yes","no","no",2,"no","semi-furnished"
6475000,7410,3,1,1,"yes","yes","yes","no","yes",2,"yes","unfurnished"
6440000,8580,5,3,2,"yes","no","no","no","no",2,"no","furnished"
6440000,5000,3,1,2,"yes","no","no","no","yes",0,"no","semi-furnished"
6419000,6750,2,1,1,"yes","yes","yes","no","no",2,"yes","furnished"
6405000,4800,3,2,4,"yes","yes","no","no","yes",0,"no","furnished"
6300000,7200,3,2,1,"yes","no","yes","no","yes",3,"no","semi-furnished"
6300000,6000,4,2,4,"yes","no","no","no","no",1,"no","semi-furnished"
6300000,4100,3,2,3,"yes","no","no","no","yes",2,"no","semi-furnished"
6300000,9000,3,1,1,"yes","no","yes","no","no",1,"yes","furnished"
6300000,6400,3,1,1,"yes","yes","yes","no","yes",1,"yes","semi-furnished"
6293000,6600,3,2,3,"yes","no","no","no","yes",0,"yes","unfurnished"
6265000,6000,4,1,3,"yes","yes","yes","no","no",0,"yes","unfurnished"
6230000,6600,3,2,1,"yes","no","yes","no","yes",0,"yes","unfurnished"
6230000,5500,3,1,3,"yes","no","no","no","no",1,"yes","unfurnished"
6195000,5500,3,2,4,"yes","yes","no","no","yes",1,"no","semi-furnished"
6195000,6350,3,2,3,"yes","yes","no","no","yes",0,"no","furnished"
6195000,5500,3,2,1,"yes","yes","yes","no","no",2,"yes","furnished"
6160000,4500,3,1,4,"yes","no","no","no","yes",0,"no","unfurnished"
6160000,5450,4,2,1,"yes","no","yes","no","yes",0,"yes","semi-furnished"
6125000,6420,3,1,3,"yes","no","yes","no","no",0,"yes","unfurnished"
6107500,3240,4,1,3,"yes","no","no","no","no",1,"no","semi-furnished"
6090000,6615,4,2,2,"yes","yes","no","yes","no",1,"no","semi-furnished"
6090000,6600,3,1,1,"yes","yes","yes","no","no",2,"yes","semi-furnished"
6090000,8372,3,1,3,"yes","no","no","no","yes",2,"no","unfurnished"
6083000,4300,6,2,2,"yes","no","no","no","no",0,"no","furnished"
6083000,9620,3,1,1,"yes","no","yes","no","no",2,"yes","furnished"
6020000,6800,2,1,1,"yes","yes","yes","no","no",2,"no","furnished"
6020000,8000,3,1,1,"yes","yes","yes","no","yes",2,"yes","semi-furnished"
6020000,6900,3,2,1,"yes","yes","yes","no","no",0,"yes","unfurnished"
5950000,3700,4,1,2,"yes","yes","no","no","yes",0,"no","furnished"
5950000,6420,3,1,1,"yes","no","yes","no","yes",0,"yes","furnished"
5950000,7020,3,1,1,"yes","no","yes","no","yes",2,"yes","semi-furnished"
5950000,6540,3,1,1,"yes","yes","yes","no","no",2,"yes","furnished"
5950000,7231,3,1,2,"yes","yes","yes","no","yes",0,"yes","semi-furnished"
5950000,6254,4,2,1,"yes","no","yes","no","no",1,"yes","semi-furnished"
5950000,7320,4,2,2,"yes","no","no","no","no",0,"no","furnished"
5950000,6525,3,2,4,"yes","no","no","no","no",1,"no","furnished"
5943000,15600,3,1,1,"yes","no","no","no","yes",2,"no","semi-furnished"
5880000,7160,3,1,1,"yes","no","yes","no","no",2,"yes","unfurnished"
5880000,6500,3,2,3,"yes","no","no","no","yes",0,"no","unfurnished"
5873000,5500,3,1,3,"yes","yes","no","no","yes",1,"no","furnished"
5873000,11460,3,1,3,"yes","no","no","no","no",2,"yes","semi-furnished"
5866000,4800,3,1,1,"yes","yes","yes","no","no",0,"no","unfurnished"
5810000,5828,4,1,4,"yes","yes","no","no","no",0,"no","semi-furnished"
5810000,5200,3,1,3,"yes","no","no","no","yes",0,"no","semi-furnished"
5810000,4800,3,1,3,"yes","no","no","no","yes",0,"no","unfurnished"
5803000,7000,3,1,1,"yes","no","yes","no","no",2,"yes","semi-furnished"
5775000,6000,3,2,4,"yes","no","no","no","yes",0,"no","unfurnished"
5740000,5400,4,2,2,"yes","no","no","no","yes",2,"no","unfurnished"
5740000,4640,4,1,2,"yes","no","no","no","no",1,"no","semi-furnished"
5740000,5000,3,1,3,"yes","no","no","no","yes",0,"no","semi-furnished"
5740000,6360,3,1,1,"yes","yes","yes","no","yes",2,"yes","furnished"
5740000,5800,3,2,4,"yes","no","no","no","yes",0,"no","unfurnished"
5652500,6660,4,2,2,"yes","yes","yes","no","no",1,"yes","semi-furnished"
5600000,10500,4,2,2,"yes","no","no","no","no",1,"no","semi-furnished"
5600000,4800,5,2,3,"no","no","yes","yes","no",0,"no","unfurnished"
5600000,4700,4,1,2,"yes","yes","yes","no","yes",1,"no","furnished"
5600000,5000,3,1,4,"yes","no","no","no","no",0,"no","furnished"
5600000,10500,2,1,1,"yes","no","no","no","no",1,"no","semi-furnished"
5600000,5500,3,2,2,"yes","no","no","no","no",1,"no","semi-furnished"
5600000,6360,3,1,3,"yes","no","no","no","no",0,"yes","semi-furnished"
5600000,6600,4,2,1,"yes","no","yes","no","no",0,"yes","semi-furnished"
5600000,5136,3,1,2,"yes","yes","yes","no","yes",0,"yes","unfurnished"
5565000,4400,4,1,2,"yes","no","no","no","yes",2,"yes","semi-furnished"
5565000,5400,5,1,2,"yes","yes","yes","no","yes",0,"yes","furnished"
5530000,3300,3,3,2,"yes","no","yes","no","no",0,"no","semi-furnished"
5530000,3650,3,2,2,"yes","no","no","no","no",2,"no","semi-furnished"
5530000,6100,3,2,1,"yes","no","yes","no","no",2,"yes","furnished"
5523000,6900,3,1,1,"yes","yes","yes","no","no",0,"yes","semi-furnished"
5495000,2817,4,2,2,"no","yes","yes","no","no",1,"no","furnished"
5495000,7980,3,1,1,"yes","no","no","no","no",2,"no","semi-furnished"
5460000,3150,3,2,1,"yes","yes","yes","no","yes",0,"no","furnished"
5460000,6210,4,1,4,"yes","yes","no","no","yes",0,"no","furnished"
5460000,6100,3,1,3,"yes","yes","no","no","yes",0,"yes","semi-furnished"
5460000,6600,4,2,2,"yes","yes","yes","no","no",0,"yes","semi-furnished"
5425000,6825,3,1,1,"yes","yes","yes","no","yes",0,"yes","semi-furnished"
5390000,6710,3,2,2,"yes","yes","yes","no","no",1,"yes","furnished"
5383000,6450,3,2,1,"yes","yes","yes","yes","no",0,"no","unfurnished"
5320000,7800,3,1,1,"yes","no","yes","no","yes",2,"yes","unfurnished"
5285000,4600,2,2,1,"yes","no","no","no","yes",2,"no","semi-furnished"
5250000,4260,4,1,2,"yes","no","yes","no","yes",0,"no","furnished"
5250000,6540,4,2,2,"no","no","no","no","yes",0,"no","semi-furnished"
5250000,5500,3,2,1,"yes","no","yes","no","no",0,"no","semi-furnished"
5250000,10269,3,1,1,"yes","no","no","no","no",1,"yes","semi-furnished"
5250000,8400,3,1,2,"yes","yes","yes","no","yes",2,"yes","unfurnished"
5250000,5300,4,2,1,"yes","no","no","no","yes",0,"yes","unfurnished"
5250000,3800,3,1,2,"yes","yes","yes","no","no",1,"yes","unfurnished"
5250000,9800,4,2,2,"yes","yes","no","no","no",2,"no","semi-furnished"
5250000,8520,3,1,1,"yes","no","no","no","yes",2,"no","furnished"
5243000,6050,3,1,1,"yes","no","yes","no","no",0,"yes","semi-furnished"
5229000,7085,3,1,1,"yes","yes","yes","no","no",2,"yes","semi-furnished"
5215000,3180,3,2,2,"yes","no","no","no","no",2,"no","semi-furnished"
5215000,4500,4,2,1,"no","no","yes","no","yes",2,"no","semi-furnished"
5215000,7200,3,1,2,"yes","yes","yes","no","no",1,"yes","furnished"
5145000,3410,3,1,2,"no","no","no","no","yes",0,"no","semi-furnished"
5145000,7980,3,1,1,"yes","no","no","no","no",1,"yes","semi-furnished"
5110000,3000,3,2,2,"yes","yes","yes","no","no",0,"no","furnished"
5110000,3000,3,1,2,"yes","no","yes","no","no",0,"no","unfurnished"
5110000,11410,2,1,2,"yes","no","no","no","no",0,"yes","furnished"
5110000,6100,3,1,1,"yes","no","yes","no","yes",0,"yes","semi-furnished"
5075000,5720,2,1,2,"yes","no","no","no","yes",0,"yes","unfurnished"
5040000,3540,2,1,1,"no","yes","yes","no","no",0,"no","semi-furnished"
5040000,7600,4,1,2,"yes","no","no","no","yes",2,"no","furnished"
5040000,10700,3,1,2,"yes","yes","yes","no","no",0,"no","semi-furnished"
5040000,6600,3,1,1,"yes","yes","yes","no","no",0,"yes","furnished"
5033000,4800,2,1,1,"yes","yes","yes","no","no",0,"no","semi-furnished"
5005000,8150,3,2,1,"yes","yes","yes","no","no",0,"no","semi-furnished"
4970000,4410,4,3,2,"yes","no","yes","no","no",2,"no","semi-furnished"
4970000,7686,3,1,1,"yes","yes","yes","yes","no",0,"no","semi-furnished"
4956000,2800,3,2,2,"no","no","yes","no","yes",1,"no","semi-furnished"
4935000,5948,3,1,2,"yes","no","no","no","yes",0,"no","semi-furnished"
4907000,4200,3,1,2,"yes","no","no","no","no",1,"no","furnished"
4900000,4520,3,1,2,"yes","no","yes","no","yes",0,"no","semi-furnished"
4900000,4095,3,1,2,"no","yes","yes","no","yes",0,"no","semi-furnished"
4900000,4120,2,1,1,"yes","no","yes","no","no",1,"no","semi-furnished"
4900000,5400,4,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
4900000,4770,3,1,1,"yes","yes","yes","no","no",0,"no","semi-furnished"
4900000,6300,3,1,1,"yes","no","no","no","yes",2,"no","semi-furnished"
4900000,5800,2,1,1,"yes","yes","yes","no","yes",0,"no","semi-furnished"
4900000,3000,3,1,2,"yes","no","yes","no","yes",0,"no","semi-furnished"
4900000,2970,3,1,3,"yes","no","no","no","no",0,"no","semi-furnished"
4900000,6720,3,1,1,"yes","no","no","no","no",0,"no","unfurnished"
4900000,4646,3,1,2,"yes","yes","yes","no","no",2,"no","semi-furnished"
4900000,12900,3,1,1,"yes","no","no","no","no",2,"no","furnished"
4893000,3420,4,2,2,"yes","no","yes","no","yes",2,"no","semi-furnished"
4893000,4995,4,2,1,"yes","no","yes","no","no",0,"no","semi-furnished"
4865000,4350,2,1,1,"yes","no","yes","no","no",0,"no","unfurnished"
4830000,4160,3,1,3,"yes","no","no","no","no",0,"no","unfurnished"
4830000,6040,3,1,1,"yes","no","no","no","no",2,"yes","semi-furnished"
4830000,6862,3,1,2,"yes","no","no","no","yes",2,"yes","furnished"
4830000,4815,2,1,1,"yes","no","no","no","yes",0,"yes","semi-furnished"
4795000,7000,3,1,2,"yes","no","yes","no","no",0,"no","unfurnished"
4795000,8100,4,1,4,"yes","no","yes","no","yes",2,"no","semi-furnished"
4767000,3420,4,2,2,"yes","no","no","no","no",0,"no","semi-furnished"
4760000,9166,2,1,1,"yes","no","yes","no","yes",2,"no","semi-furnished"
4760000,6321,3,1,2,"yes","no","yes","no","yes",1,"no","furnished"
4760000,10240,2,1,1,"yes","no","no","no","yes",2,"yes","unfurnished"
4753000,6440,2,1,1,"yes","no","no","no","yes",3,"no","semi-furnished"
4690000,5170,3,1,4,"yes","no","no","no","yes",0,"no","semi-furnished"
4690000,6000,2,1,1,"yes","no","yes","no","yes",1,"no","furnished"
4690000,3630,3,1,2,"yes","no","no","no","no",2,"no","semi-furnished"
4690000,9667,4,2,2,"yes","yes","yes","no","no",1,"no","semi-furnished"
4690000,5400,2,1,2,"yes","no","no","no","no",0,"yes","semi-furnished"
4690000,4320,3,1,1,"yes","no","no","no","no",0,"yes","semi-furnished"
4655000,3745,3,1,2,"yes","no","yes","no","no",0,"no","furnished"
4620000,4160,3,1,1,"yes","yes","yes","no","yes",0,"no","unfurnished"
4620000,3880,3,2,2,"yes","no","yes","no","no",2,"no","semi-furnished"
4620000,5680,3,1,2,"yes","yes","no","no","yes",1,"no","semi-furnished"
4620000,2870,2,1,2,"yes","yes","yes","no","no",0,"yes","semi-furnished"
4620000,5010,3,1,2,"yes","no","yes","no","no",0,"no","semi-furnished"
4613000,4510,4,2,2,"yes","no","yes","no","no",0,"no","semi-furnished"
4585000,4000,3,1,2,"yes","no","no","no","no",1,"no","furnished"
4585000,3840,3,1,2,"yes","no","no","no","no",1,"yes","semi-furnished"
4550000,3760,3,1,1,"yes","no","no","no","no",2,"no","semi-furnished"
4550000,3640,3,1,2,"yes","no","no","no","yes",0,"no","furnished"
4550000,2550,3,1,2,"yes","no","yes","no","no",0,"no","furnished"
4550000,5320,3,1,2,"yes","yes","yes","no","no",0,"yes","semi-furnished"
4550000,5360,3,1,2,"yes","no","no","no","no",2,"yes","unfurnished"
4550000,3520,3,1,1,"yes","no","no","no","no",0,"yes","semi-furnished"
4550000,8400,4,1,4,"yes","no","no","no","no",3,"no","unfurnished"
4543000,4100,2,2,1,"yes","yes","yes","no","no",0,"no","semi-furnished"
4543000,4990,4,2,2,"yes","yes","yes","no","no",0,"yes","furnished"
4515000,3510,3,1,3,"yes","no","no","no","no",0,"no","semi-furnished"
4515000,3450,3,1,2,"yes","no","yes","no","no",1,"no","semi-furnished"
4515000,9860,3,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
4515000,3520,2,1,2,"yes","no","no","no","no",0,"yes","furnished"
4480000,4510,4,1,2,"yes","no","no","no","yes",2,"no","semi-furnished"
4480000,5885,2,1,1,"yes","no","no","no","yes",1,"no","unfurnished"
4480000,4000,3,1,2,"yes","no","no","no","no",2,"no","furnished"
4480000,8250,3,1,1,"yes","no","no","no","no",0,"no","furnished"
4480000,4040,3,1,2,"yes","no","no","no","no",1,"no","semi-furnished"
4473000,6360,2,1,1,"yes","no","yes","no","yes",1,"no","furnished"
4473000,3162,3,1,2,"yes","no","no","no","yes",1,"no","furnished"
4473000,3510,3,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
4445000,3750,2,1,1,"yes","yes","yes","no","no",0,"no","semi-furnished"
4410000,3968,3,1,2,"no","no","no","no","no",0,"no","semi-furnished"
4410000,4900,2,1,2,"yes","no","yes","no","no",0,"no","semi-furnished"
4403000,2880,3,1,2,"yes","no","no","no","no",0,"yes","semi-furnished"
4403000,4880,3,1,1,"yes","no","no","no","no",2,"yes","unfurnished"
4403000,4920,3,1,2,"yes","no","no","no","no",1,"no","semi-furnished"
4382000,4950,4,1,2,"yes","no","no","no","yes",0,"no","semi-furnished"
4375000,3900,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
4340000,4500,3,2,3,"yes","no","no","yes","no",1,"no","furnished"
4340000,1905,5,1,2,"no","no","yes","no","no",0,"no","semi-furnished"
4340000,4075,3,1,1,"yes","yes","yes","no","no",2,"no","semi-furnished"
4340000,3500,4,1,2,"yes","no","no","no","no",2,"no","furnished"
4340000,6450,4,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
4319000,4032,2,1,1,"yes","no","yes","no","no",0,"no","furnished"
4305000,4400,2,1,1,"yes","no","no","no","no",1,"no","semi-furnished"
4305000,10360,2,1,1,"yes","no","no","no","no",1,"yes","semi-furnished"
4277000,3400,3,1,2,"yes","no","yes","no","no",2,"yes","semi-furnished"
4270000,6360,2,1,1,"yes","no","no","no","no",0,"no","furnished"
4270000,6360,2,1,2,"yes","no","no","no","no",0,"no","unfurnished"
4270000,4500,2,1,1,"yes","no","no","no","yes",2,"no","furnished"
4270000,2175,3,1,2,"no","yes","yes","no","yes",0,"no","unfurnished"
4270000,4360,4,1,2,"yes","no","no","no","no",0,"no","furnished"
4270000,7770,2,1,1,"yes","no","no","no","no",1,"no","furnished"
4235000,6650,3,1,2,"yes","yes","no","no","no",0,"no","semi-furnished"
4235000,2787,3,1,1,"yes","no","yes","no","no",0,"yes","furnished"
4200000,5500,3,1,2,"yes","no","no","no","yes",0,"no","unfurnished"
4200000,5040,3,1,2,"yes","no","yes","no","yes",0,"no","unfurnished"
4200000,5850,2,1,1,"yes","yes","yes","no","no",2,"no","semi-furnished"
4200000,2610,4,3,2,"no","no","no","no","no",0,"no","semi-furnished"
4200000,2953,3,1,2,"yes","no","yes","no","yes",0,"no","unfurnished"
4200000,2747,4,2,2,"no","no","no","no","no",0,"no","semi-furnished"
4200000,4410,2,1,1,"no","no","no","no","no",1,"no","unfurnished"
4200000,4000,4,2,2,"no","no","no","no","no",0,"no","semi-furnished"
4200000,2325,3,1,2,"no","no","no","no","no",0,"no","semi-furnished"
4200000,4600,3,2,2,"yes","no","no","no","yes",1,"no","semi-furnished"
4200000,3640,3,2,2,"yes","no","yes","no","no",0,"no","unfurnished"
4200000,5800,3,1,1,"yes","no","no","yes","no",2,"no","semi-furnished"
4200000,7000,3,1,1,"yes","no","no","no","no",3,"no","furnished"
4200000,4079,3,1,3,"yes","no","no","no","no",0,"no","semi-furnished"
4200000,3520,3,1,2,"yes","no","no","no","no",0,"yes","semi-furnished"
4200000,2145,3,1,3,"yes","no","no","no","no",1,"yes","unfurnished"
4200000,4500,3,1,1,"yes","no","yes","no","no",0,"no","furnished"
4193000,8250,3,1,1,"yes","no","yes","no","no",3,"no","semi-furnished"
4193000,3450,3,1,2,"yes","no","no","no","no",1,"no","semi-furnished"
4165000,4840,3,1,2,"yes","no","no","no","no",1,"no","semi-furnished"
4165000,4080,3,1,2,"yes","no","no","no","no",2,"no","semi-furnished"
4165000,4046,3,1,2,"yes","no","yes","no","no",1,"no","semi-furnished"
4130000,4632,4,1,2,"yes","no","no","no","yes",0,"no","semi-furnished"
4130000,5985,3,1,1,"yes","no","yes","no","no",0,"no","semi-furnished"
4123000,6060,2,1,1,"yes","no","yes","no","no",1,"no","semi-furnished"
4098500,3600,3,1,1,"yes","no","yes","no","yes",0,"yes","furnished"
4095000,3680,3,2,2,"yes","no","no","no","no",0,"no","semi-furnished"
4095000,4040,2,1,2,"yes","no","no","no","no",1,"no","semi-furnished"
4095000,5600,2,1,1,"yes","no","no","no","yes",0,"no","semi-furnished"
4060000,5900,4,2,2,"no","no","yes","no","no",1,"no","unfurnished"
4060000,4992,3,2,2,"yes","no","no","no","no",2,"no","unfurnished"
4060000,4340,3,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
4060000,3000,4,1,3,"yes","no","yes","no","yes",2,"no","semi-furnished"
4060000,4320,3,1,2,"yes","no","no","no","no",2,"yes","furnished"
4025000,3630,3,2,2,"yes","no","no","yes","no",2,"no","semi-furnished"
4025000,3460,3,2,1,"yes","no","yes","no","yes",1,"no","furnished"
4025000,5400,3,1,1,"yes","no","no","no","no",3,"no","semi-furnished"
4007500,4500,3,1,2,"no","no","yes","no","yes",0,"no","semi-furnished"
4007500,3460,4,1,2,"yes","no","no","no","yes",0,"no","semi-furnished"
3990000,4100,4,1,1,"no","no","yes","no","no",0,"no","unfurnished"
3990000,6480,3,1,2,"no","no","no","no","yes",1,"no","semi-furnished"
3990000,4500,3,2,2,"no","no","yes","no","yes",0,"no","semi-furnished"
3990000,3960,3,1,2,"yes","no","no","no","no",0,"no","furnished"
3990000,4050,2,1,2,"yes","yes","yes","no","no",0,"yes","unfurnished"
3920000,7260,3,2,1,"yes","yes","yes","no","no",3,"no","furnished"
3920000,5500,4,1,2,"yes","yes","yes","no","no",0,"no","semi-furnished"
3920000,3000,3,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
3920000,3290,2,1,1,"yes","no","no","yes","no",1,"no","furnished"
3920000,3816,2,1,1,"yes","no","yes","no","yes",2,"no","furnished"
3920000,8080,3,1,1,"yes","no","no","no","yes",2,"no","semi-furnished"
3920000,2145,4,2,1,"yes","no","yes","no","no",0,"yes","unfurnished"
3885000,3780,2,1,2,"yes","yes","yes","no","no",0,"no","semi-furnished"
3885000,3180,4,2,2,"yes","no","no","no","no",0,"no","furnished"
3850000,5300,5,2,2,"yes","no","no","no","no",0,"no","semi-furnished"
3850000,3180,2,2,1,"yes","no","yes","no","no",2,"no","semi-furnished"
3850000,7152,3,1,2,"yes","no","no","no","yes",0,"no","furnished"
3850000,4080,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3850000,3850,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3850000,2015,3,1,2,"yes","no","yes","no","no",0,"yes","semi-furnished"
3850000,2176,2,1,2,"yes","yes","no","no","no",0,"yes","semi-furnished"
3836000,3350,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3815000,3150,2,2,1,"no","no","yes","no","no",0,"no","semi-furnished"
3780000,4820,3,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
3780000,3420,2,1,2,"yes","no","no","yes","no",1,"no","semi-furnished"
3780000,3600,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3780000,5830,2,1,1,"yes","no","no","no","no",2,"no","unfurnished"
3780000,2856,3,1,3,"yes","no","no","no","no",0,"yes","furnished"
3780000,8400,2,1,1,"yes","no","no","no","no",1,"no","furnished"
3773000,8250,3,1,1,"yes","no","no","no","no",2,"no","furnished"
3773000,2520,5,2,1,"no","no","yes","no","yes",1,"no","furnished"
3773000,6930,4,1,2,"no","no","no","no","no",1,"no","furnished"
3745000,3480,2,1,1,"yes","no","no","no","no",0,"yes","semi-furnished"
3710000,3600,3,1,1,"yes","no","no","no","no",1,"no","unfurnished"
3710000,4040,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3710000,6020,3,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3710000,4050,2,1,1,"yes","no","no","no","no",0,"no","furnished"
3710000,3584,2,1,1,"yes","no","no","yes","no",0,"no","semi-furnished"
3703000,3120,3,1,2,"no","no","yes","yes","no",0,"no","semi-furnished"
3703000,5450,2,1,1,"yes","no","no","no","no",0,"no","furnished"
3675000,3630,2,1,1,"yes","no","yes","no","no",0,"no","furnished"
3675000,3630,2,1,1,"yes","no","no","no","yes",0,"no","unfurnished"
3675000,5640,2,1,1,"no","no","no","no","no",0,"no","semi-furnished"
3675000,3600,2,1,1,"yes","no","no","no","no",0,"no","furnished"
3640000,4280,2,1,1,"yes","no","no","no","yes",2,"no","semi-furnished"
3640000,3570,3,1,2,"yes","no","yes","no","no",0,"no","semi-furnished"
3640000,3180,3,1,2,"no","no","yes","no","no",0,"no","semi-furnished"
3640000,3000,2,1,2,"yes","no","no","no","yes",0,"no","furnished"
3640000,3520,2,2,1,"yes","no","yes","no","no",0,"no","semi-furnished"
3640000,5960,3,1,2,"yes","yes","yes","no","no",0,"no","unfurnished"
3640000,4130,3,2,2,"yes","no","no","no","no",2,"no","semi-furnished"
3640000,2850,3,2,2,"no","no","yes","no","no",0,"yes","unfurnished"
3640000,2275,3,1,3,"yes","no","no","yes","yes",0,"yes","semi-furnished"
3633000,3520,3,1,1,"yes","no","no","no","no",2,"yes","unfurnished"
3605000,4500,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3605000,4000,2,1,1,"yes","no","no","no","no",0,"yes","semi-furnished"
3570000,3150,3,1,2,"yes","no","yes","no","no",0,"no","furnished"
3570000,4500,4,2,2,"yes","no","yes","no","no",2,"no","furnished"
3570000,4500,2,1,1,"no","no","no","no","no",0,"no","furnished"
3570000,3640,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3535000,3850,3,1,1,"yes","no","no","no","no",2,"no","unfurnished"
3500000,4240,3,1,2,"yes","no","no","no","yes",0,"no","semi-furnished"
3500000,3650,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3500000,4600,4,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
3500000,2135,3,2,2,"no","no","no","no","no",0,"no","unfurnished"
3500000,3036,3,1,2,"yes","no","yes","no","no",0,"no","semi-furnished"
3500000,3990,3,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
3500000,7424,3,1,1,"no","no","no","no","no",0,"no","unfurnished"
3500000,3480,3,1,1,"no","no","no","no","yes",0,"no","unfurnished"
3500000,3600,6,1,2,"yes","no","no","no","no",1,"no","unfurnished"
3500000,3640,2,1,1,"yes","no","no","no","no",1,"no","semi-furnished"
3500000,5900,2,1,1,"yes","no","no","no","no",1,"no","furnished"
3500000,3120,3,1,2,"yes","no","no","no","no",1,"no","unfurnished"
3500000,7350,2,1,1,"yes","no","no","no","no",1,"no","semi-furnished"
3500000,3512,2,1,1,"yes","no","no","no","no",1,"yes","unfurnished"
3500000,9500,3,1,2,"yes","no","no","no","no",3,"yes","unfurnished"
3500000,5880,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3500000,12944,3,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3493000,4900,3,1,2,"no","no","no","no","no",0,"no","unfurnished"
3465000,3060,3,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3465000,5320,2,1,1,"yes","no","no","no","no",1,"yes","unfurnished"
3465000,2145,3,1,3,"yes","no","no","no","no",0,"yes","furnished"
3430000,4000,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3430000,3185,2,1,1,"yes","no","no","no","no",2,"no","unfurnished"
3430000,3850,3,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3430000,2145,3,1,3,"yes","no","no","no","no",0,"yes","furnished"
3430000,2610,3,1,2,"yes","no","yes","no","no",0,"yes","unfurnished"
3430000,1950,3,2,2,"yes","no","yes","no","no",0,"yes","unfurnished"
3423000,4040,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3395000,4785,3,1,2,"yes","yes","yes","no","yes",1,"no","furnished"
3395000,3450,3,1,1,"yes","no","yes","no","no",2,"no","unfurnished"
3395000,3640,2,1,1,"yes","no","no","no","no",0,"no","furnished"
3360000,3500,4,1,2,"yes","no","no","no","yes",2,"no","unfurnished"
3360000,4960,4,1,3,"no","no","no","no","no",0,"no","semi-furnished"
3360000,4120,2,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3360000,4750,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3360000,3720,2,1,1,"no","no","no","no","yes",0,"no","unfurnished"
3360000,3750,3,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3360000,3100,3,1,2,"no","no","yes","no","no",0,"no","semi-furnished"
3360000,3185,2,1,1,"yes","no","yes","no","no",2,"no","furnished"
3353000,2700,3,1,1,"no","no","no","no","no",0,"no","furnished"
3332000,2145,3,1,2,"yes","no","yes","no","no",0,"yes","furnished"
3325000,4040,2,1,1,"yes","no","no","no","no",1,"no","unfurnished"
3325000,4775,4,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3290000,2500,2,1,1,"no","no","no","no","yes",0,"no","unfurnished"
3290000,3180,4,1,2,"yes","no","yes","no","yes",0,"no","unfurnished"
3290000,6060,3,1,1,"yes","yes","yes","no","no",0,"no","furnished"
3290000,3480,4,1,2,"no","no","no","no","no",1,"no","semi-furnished"
3290000,3792,4,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
3290000,4040,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3290000,2145,3,1,2,"yes","no","yes","no","no",0,"yes","furnished"
3290000,5880,3,1,1,"yes","no","no","no","no",1,"no","unfurnished"
3255000,4500,2,1,1,"no","no","no","no","no",0,"no","semi-furnished"
3255000,3930,2,1,1,"no","no","no","no","no",0,"no","unfurnished"
3234000,3640,4,1,2,"yes","no","yes","no","no",0,"no","unfurnished"
3220000,4370,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3220000,2684,2,1,1,"yes","no","no","no","yes",1,"no","unfurnished"
3220000,4320,3,1,1,"no","no","no","no","no",1,"no","unfurnished"
3220000,3120,3,1,2,"no","no","no","no","no",0,"no","furnished"
3150000,3450,1,1,1,"yes","no","no","no","no",0,"no","furnished"
3150000,3986,2,2,1,"no","yes","yes","no","no",1,"no","unfurnished"
3150000,3500,2,1,1,"no","no","yes","no","no",0,"no","semi-furnished"
3150000,4095,2,1,1,"yes","no","no","no","no",2,"no","semi-furnished"
3150000,1650,3,1,2,"no","no","yes","no","no",0,"no","unfurnished"
3150000,3450,3,1,2,"yes","no","yes","no","no",0,"no","semi-furnished"
3150000,6750,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3150000,9000,3,1,2,"yes","no","no","no","no",2,"no","semi-furnished"
3150000,3069,2,1,1,"yes","no","no","no","no",1,"no","unfurnished"
3143000,4500,3,1,2,"yes","no","no","no","yes",0,"no","unfurnished"
3129000,5495,3,1,1,"yes","no","yes","no","no",0,"no","unfurnished"
3118850,2398,3,1,1,"yes","no","no","no","no",0,"yes","semi-furnished"
3115000,3000,3,1,1,"no","no","no","no","yes",0,"no","unfurnished"
3115000,3850,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3115000,3500,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3087000,8100,2,1,1,"yes","no","no","no","no",1,"no","unfurnished"
3080000,4960,2,1,1,"yes","no","yes","no","yes",0,"no","unfurnished"
3080000,2160,3,1,2,"no","no","yes","no","no",0,"no","semi-furnished"
3080000,3090,2,1,1,"yes","yes","yes","no","no",0,"no","unfurnished"
3080000,4500,2,1,2,"yes","no","no","yes","no",1,"no","semi-furnished"
3045000,3800,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
3010000,3090,3,1,2,"no","no","no","no","no",0,"no","semi-furnished"
3010000,3240,3,1,2,"yes","no","no","no","no",2,"no","semi-furnished"
3010000,2835,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
3010000,4600,2,1,1,"yes","no","no","no","no",0,"no","furnished"
3010000,5076,3,1,1,"no","no","no","no","no",0,"no","unfurnished"
3010000,3750,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
3010000,3630,4,1,2,"yes","no","no","no","no",3,"no","semi-furnished"
3003000,8050,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2975000,4352,4,1,2,"no","no","no","no","no",1,"no","unfurnished"
2961000,3000,2,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
2940000,5850,3,1,2,"yes","no","yes","no","no",1,"no","unfurnished"
2940000,4960,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2940000,3600,3,1,2,"no","no","no","no","no",1,"no","unfurnished"
2940000,3660,4,1,2,"no","no","no","no","no",0,"no","unfurnished"
2940000,3480,3,1,2,"no","no","no","no","no",1,"no","semi-furnished"
2940000,2700,2,1,1,"no","no","no","no","no",0,"no","furnished"
2940000,3150,3,1,2,"no","no","no","no","no",0,"no","unfurnished"
2940000,6615,3,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
2870000,3040,2,1,1,"no","no","no","no","no",0,"no","unfurnished"
2870000,3630,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2870000,6000,2,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
2870000,5400,4,1,2,"yes","no","no","no","no",0,"no","unfurnished"
2852500,5200,4,1,3,"yes","no","no","no","no",0,"no","unfurnished"
2835000,3300,3,1,2,"no","no","no","no","no",1,"no","semi-furnished"
2835000,4350,3,1,2,"no","no","no","yes","no",1,"no","unfurnished"
2835000,2640,2,1,1,"no","no","no","no","no",1,"no","furnished"
2800000,2650,3,1,2,"yes","no","yes","no","no",1,"no","unfurnished"
2800000,3960,3,1,1,"yes","no","no","no","no",0,"no","furnished"
2730000,6800,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2730000,4000,3,1,2,"yes","no","no","no","no",1,"no","unfurnished"
2695000,4000,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2660000,3934,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2660000,2000,2,1,2,"yes","no","no","no","no",0,"no","semi-furnished"
2660000,3630,3,3,2,"no","yes","no","no","no",0,"no","unfurnished"
2660000,2800,3,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2660000,2430,3,1,1,"no","no","no","no","no",0,"no","unfurnished"
2660000,3480,2,1,1,"yes","no","no","no","no",1,"no","semi-furnished"
2660000,4000,3,1,1,"yes","no","no","no","no",0,"no","semi-furnished"
2653000,3185,2,1,1,"yes","no","no","no","yes",0,"no","unfurnished"
2653000,4000,3,1,2,"yes","no","no","no","yes",0,"no","unfurnished"
2604000,2910,2,1,1,"no","no","no","no","no",0,"no","unfurnished"
2590000,3600,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2590000,4400,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2590000,3600,2,2,2,"yes","no","yes","no","no",1,"no","furnished"
2520000,2880,3,1,1,"no","no","no","no","no",0,"no","unfurnished"
2520000,3180,3,1,1,"no","no","no","no","no",0,"no","unfurnished"
2520000,3000,2,1,2,"yes","no","no","no","no",0,"no","furnished"
2485000,4400,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
2485000,3000,3,1,2,"no","no","no","no","no",0,"no","semi-furnished"
2450000,3210,3,1,2,"yes","no","yes","no","no",0,"no","unfurnished"
2450000,3240,2,1,1,"no","yes","no","no","no",1,"no","unfurnished"
2450000,3000,2,1,1,"yes","no","no","no","no",1,"no","unfurnished"
2450000,3500,2,1,1,"yes","yes","no","no","no",0,"no","unfurnished"
2450000,4840,2,1,2,"yes","no","no","no","no",0,"no","unfurnished"
2450000,7700,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2408000,3635,2,1,1,"no","no","no","no","no",0,"no","unfurnished"
2380000,2475,3,1,2,"yes","no","no","no","no",0,"no","furnished"
2380000,2787,4,2,2,"yes","no","no","no","no",0,"no","furnished"
2380000,3264,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2345000,3640,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2310000,3180,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
2275000,1836,2,1,1,"no","no","yes","no","no",0,"no","semi-furnished"
2275000,3970,1,1,1,"no","no","no","no","no",0,"no","unfurnished"
2275000,3970,3,1,2,"yes","no","yes","no","no",0,"no","unfurnished"
2240000,1950,3,1,1,"no","no","no","yes","no",0,"no","unfurnished"
2233000,5300,3,1,1,"no","no","no","no","yes",0,"yes","unfurnished"
2135000,3000,2,1,1,"no","no","no","no","no",0,"no","unfurnished"
2100000,2400,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
2100000,3000,4,1,2,"yes","no","no","no","no",0,"no","unfurnished"
2100000,3360,2,1,1,"yes","no","no","no","no",1,"no","unfurnished"
1960000,3420,5,1,2,"no","no","no","no","no",0,"no","unfurnished"
1890000,1700,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
1890000,3649,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
1855000,2990,2,1,1,"no","no","no","no","no",1,"no","unfurnished"
1820000,3000,2,1,1,"yes","no","yes","no","no",2,"no","unfurnished"
1767150,2400,3,1,1,"no","no","no","no","no",0,"no","semi-furnished"
1750000,3620,2,1,1,"yes","no","no","no","no",0,"no","unfurnished"
1750000,2910,3,1,1,"no","no","no","no","no",0,"no","furnished"
1750000,3850,3,1,2,"yes","no","no","no","no",0,"no","unfurnished"
""")
            temp_file_path = temp_file.name
            temp_file.flush()

            result = RecordCount().calculate(data=pd.read_csv(temp_file_path))
            self.assertEqual(result.metric_name, "RecordCount")
            self.assertEqual(result.value, 545)

    def test_record_count_Parquet_case1(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name

            df = pd.DataFrame([{"product_id": 101, "name": "Apple", "category": "Fruits", "price": 0.5, "stock": 150, "variants": ["Red", "Green"], "suppliers": [{"name": "Supplier A", "rating": 4.5}, {"name": "Supplier B", "rating": 4.2}]},
{"product_id": 102, "name": "Banana", "category": "Fruits", "price": 0.3, "stock": 200, "variants": ["Yellow"], "suppliers": [{"name": "Supplier C", "rating": 4.3}]},
{"product_id": 103, "name": "Orange", "category": "Fruits", "price": 0.6, "stock": 180, "variants": ["Navel", "Mandarin"], "suppliers": [{"name": "Supplier A", "rating": 4.5}]},
{"product_id": 104, "name": "Milk", "category": "Dairy", "price": 1.2, "stock": 100, "variants": ["Whole", "Skimmed", "Lactose-Free"], "suppliers": [{"name": "Supplier D", "rating": 4.7}]},
{"product_id": 105, "name": "Cheese", "category": "Dairy", "price": 2.5, "stock": 50, "variants": ["Cheddar", "Mozzarella"], "suppliers": [{"name": "Supplier E", "rating": 4.6}, {"name": "Supplier F", "rating": 4.4}]},
{"product_id": 106, "name": "Bread", "category": "Bakery", "price": 1.0, "stock": 120, "variants": ["Whole Wheat", "White"], "suppliers": [{"name": "Supplier G", "rating": 4.3}]},
{"product_id": 107, "name": "Eggs", "category": "Dairy", "price": 2.0, "stock": 80, "variants": ["Organic", "Regular"], "suppliers": [{"name": "Supplier H", "rating": 4.2}]},
{"product_id": 108, "name": "Chicken", "category": "Meat", "price": 5.0, "stock": 40, "variants": ["Whole", "Breast", "Thigh"], "suppliers": [{"name": "Supplier I", "rating": 4.5}]},
{"product_id": 109, "name": "Beef", "category": "Meat", "price": 7.5, "stock": 30, "variants": ["Ground", "Steak"], "suppliers": [{"name": "Supplier J", "rating": 4.6}]},
{"product_id": 110, "name": "Rice", "category": "Grains", "price": 1.5, "stock": 90, "variants": ["Basmati", "Jasmine", "Brown"], "suppliers": [{"name": "Supplier K", "rating": 4.3}]}])

            df.to_parquet(temp_file_path, index=False)

            result = RecordCount().calculate(data=pd.read_parquet(temp_file_path))
            self.assertEqual(result.metric_name, "RecordCount")
            self.assertEqual(result.value, 10)

    def test_record_count_Parquet_case2(self):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file_path = temp_file.name

                df = pd.json_normalize([
    {"owner_id": None, "name": None, "car_make": None, "car_model": None, "year": None, "registration_date": None, "ownership_status": None, "contact": None},
    {"owner_id": None, "name": None, "car_make": None, "car_model": None, "year": None, "registration_date": "", "ownership_status": "", "contact": ""},
    {"owner_id": 3, "name": None, "car_make": "Ford", "car_model": "Focus", "year": 2013, "registration_date": "2013-09-15", "ownership_status": "Active", "contact": "ford.owner@email.com"},
    {"owner_id": 4, "name": "Alice Johnson", "car_make": "Chevrolet", "car_model": "Malibu", "year": None, "registration_date": "2018-11-05", "ownership_status": None, "contact": "alice.johnson@email.com"},
    {"owner_id": 5, "name": "Bob Lee", "car_make": "BMW", "car_model": "X5", "year": 2019, "registration_date": None, "ownership_status": "Active", "contact": None},
    {"owner_id": 6, "name": "Sara Patel", "car_make": "Nissan", "car_model": "Altima", "year": 2020, "registration_date": "2020-06-22", "ownership_status": "Active", "contact": "sara.patel@email.com"},
    {"owner_id": 7, "name": None, "car_make": "Mazda", "car_model": "CX-5", "year": None, "registration_date": "2019-12-11", "ownership_status": "Inactive", "contact": "mazda.owner@email.com"},
    {"owner_id": 8, "name": "Emily Davis", "car_make": "Hyundai", "car_model": "Elantra", "year": 2016, "registration_date": "2016-05-30", "ownership_status": "Active", "contact": None},
    {"owner_id": 9, "name": "Michael Brown", "car_make": "Volkswagen", "car_model": "Jetta", "year": 2017, "registration_date": None, "ownership_status": "Inactive", "contact": None},
    {"owner_id": 10, "name": "Lisa White", "car_make": "Audi", "car_model": "A4", "year": None, "registration_date": "2018-07-19", "ownership_status": "Active", "contact": "lisa.white@email.com"},
    {"owner_id": 11, "name": "David Wilson", "car_make": "Mercedes-Benz", "car_model": "C-Class", "year": 2021, "registration_date": None, "ownership_status": None, "contact": "david.wilson@email.com"},
    {"owner_id": 12, "name": "Megan Harris", "car_make": "Toyota", "car_model": "Camry", "year": 2022, "registration_date": "2022-02-18", "ownership_status": "Active", "contact": "megan.harris@email.com"},
    {"owner_id": 13, "name": "Chris Clark", "car_make": "Kia", "car_model": "Sorento", "year": None, "registration_date": "2015-11-25", "ownership_status": "Active", "contact": None},
    {"owner_id": 14, "name": "John Brown", "car_make": "Ford", "car_model": "F-150", "year": 2021, "registration_date": None, "ownership_status": "Inactive", "contact": None},
    {"owner_id": 15, "name": "Nina Adams", "car_make": "Chevrolet", "car_model": "Equinox", "year": 2020, "registration_date": "2020-07-02", "ownership_status": None, "contact": "nina.adams@email.com"},
    {"owner_id": 16, "name": "Rachel King", "car_make": "Honda", "car_model": "Pilot", "year": 2018, "registration_date": "2018-03-14", "ownership_status": "Active", "contact": "rachel.king@email.com"},
    {"owner_id": 17, "name": "Oliver Scott", "car_make": "BMW", "car_model": "328i", "year": 2014, "registration_date": None, "ownership_status": "Inactive", "contact": None},
    {"owner_id": 18, "name": "Jack Turner", "car_make": "Mercedes-Benz", "car_model": "GLC", "year": 2019, "registration_date": "2019-04-09", "ownership_status": "Active", "contact": "jack.turner@email.com"},
    {"owner_id": 19, "name": None, "car_make": "Audi", "car_model": "Q5", "year": None, "registration_date": "2017-12-21", "ownership_status": "Active", "contact": "audi.owner@email.com"},
    {"owner_id": 20, "name": "Sophia Gonzalez", "car_make": "Mazda", "car_model": "Mazda3", "year": 2016, "registration_date": "2016-01-13", "ownership_status": "Inactive", "contact": "sophia.gonzalez@email.com"},
    {"owner_id": 21, "name": "Liam Robinson", "car_make": "Chevrolet", "car_model": "Traverse", "year": None, "registration_date": "2018-10-17", "ownership_status": "Active", "contact": None},
    {"owner_id": 22, "name": "Emma Martinez", "car_make": "Honda", "car_model": "HR-V", "year": 2015, "registration_date": None, "ownership_status": "Inactive", "contact": "emma.martinez@email.com"},
    {"owner_id": 23, "name": "Zoe Perez", "car_make": "Hyundai", "car_model": "Sonata", "year": 2014, "registration_date": "2014-08-22", "ownership_status": "Active", "contact": "zoe.perez@email.com"},
    {"owner_id": 24, "name": "James Young", "car_make": "Toyota", "car_model": "Highlander", "year": 2021, "registration_date": None, "ownership_status": "Inactive", "contact": "james.young@email.com"},
    {"owner_id": 25, "name": "Lucas Martinez", "car_make": "Volkswagen", "car_model": "Passat", "year": 2018, "registration_date": "2018-04-09", "ownership_status": "Active", "contact": None},
    {"owner_id": 26, "name": None, "car_make": "BMW", "car_model": "X6", "year": 2022, "registration_date": "2022-05-04", "ownership_status": "Active", "contact": None},
    {"owner_id": 27, "name": "Olivia Thompson", "car_make": "Nissan", "car_model": "Maxima", "year": None, "registration_date": "2019-10-14", "ownership_status": "Inactive", "contact": "olivia.thompson@email.com"},
    {"owner_id": 28, "name": "Sophia White", "car_make": "Toyota", "car_model": "4Runner", "year": None, "registration_date": "2017-01-25", "ownership_status": "Active", "contact": None},
    {"owner_id": 29, "name": "Noah Jackson", "car_make": "Chevrolet", "car_model": "Tahoe", "year": 2021, "registration_date": None, "ownership_status": "Inactive", "contact": "noah.jackson@email.com"},
    {"owner_id": 30, "name": "Isabella Lee", "car_make": "Honda", "car_model": "Accord", "year": 2020, "registration_date": "2020-11-02", "ownership_status": None, "contact": "isabella.lee@email.com"},
    {"owner_id": 31, "name": "Daniel Hall", "car_make": "Ford", "car_model": "Escape", "year": 2016, "registration_date": "2016-02-07", "ownership_status": "Active", "contact": "daniel.hall@email.com"},
    {"owner_id": 32, "name": "Mason Allen", "car_make": "Jeep", "car_model": "Cherokee", "year": 2018, "registration_date": None, "ownership_status": "Inactive", "contact": "mason.allen@email.com"},
    {"owner_id": 33, "name": "Amelia Harris", "car_make": "Mazda", "car_model": "Mazda6", "year": None, "registration_date": "2017-07-23", "ownership_status": "Active", "contact": None},
    {"owner_id": 34, "name": "Aiden Walker", "car_make": "Toyota", "car_model": "Tacoma", "year": 2020, "registration_date": "2020-08-14", "ownership_status": "Inactive", "contact": "aiden.walker@email.com"},
    {"owner_id": 35, "name": "Charlotte Clark", "car_make": "Ford", "car_model": "Escape", "year": 2022, "registration_date": None, "ownership_status": "Active", "contact": "charlotte.clark@email.com"},
    {"owner_id": 36, "name": "Henry Allen", "car_make": "BMW", "car_model": "X3", "year": None, "registration_date": "2021-02-15", "ownership_status": "Inactive", "contact": "henry.allen@email.com"},
    {"owner_id": 37, "name": "Jackie Mitchell", "car_make": "Chevrolet", "car_model": "Silverado", "year": 2018, "registration_date": "2018-11-21", "ownership_status": None, "contact": "jackie.mitchell@email.com"},
    {"owner_id": 38, "name": "Elijah Thompson", "car_make": "Hyundai", "car_model": "Kona", "year": None, "registration_date": "2022-09-04", "ownership_status": "Active", "contact": "elijah.thompson@email.com"},
    {"owner_id": 39, "name": "Ella Wilson", "car_make": "Mazda", "car_model": "CX-9", "year": 2021, "registration_date": "2021-05-29", "ownership_status": "Inactive", "contact": "ella.wilson@email.com"},
    {"owner_id": 40, "name": "Ethan Roberts", "car_make": "Ford", "car_model": "F-150", "year": 2019, "registration_date": None, "ownership_status": "Active", "contact": "ethan.roberts@email.com"},
    {"owner_id": 41, "name": "Harper Johnson", "car_make": "Chevrolet", "car_model": "Equinox", "year": None, "registration_date": "2020-06-10", "ownership_status": "Inactive", "contact": "harper.johnson@email.com"},
    {"owner_id": 42, "name": "Lily King", "car_make": "Toyota", "car_model": "RAV4", "year": 2021, "registration_date": None, "ownership_status": "Active", "contact": "lily.king@email.com"},
    {"owner_id": 43, "name": "Lucas Davis", "car_make": "Honda", "car_model": "CR-V", "year": 2020, "registration_date": "2020-12-09", "ownership_status": None, "contact": "lucas.davis@email.com"},
    {"owner_id": 44, "name": "Mason Lee", "car_make": "Mazda", "car_model": "CX-5", "year": 2019, "registration_date": "2019-04-17", "ownership_status": "Inactive", "contact": "mason.lee@email.com"},
    {"owner_id": 45, "name": "Harper White", "car_make": "Toyota", "car_model": "Sienna", "year": 2021, "registration_date": None, "ownership_status": "Active", "contact": None},
    {"owner_id": 46, "name": "James Clark", "car_make": "Ford", "car_model": "Expedition", "year": 2018, "registration_date": "2018-06-05", "ownership_status": "Inactive", "contact": "james.clark@email.com"},
    None])

                df.to_parquet(temp_file_path, index=False)

                result = RecordCount().calculate(data=pd.read_parquet(temp_file_path))
                self.assertEqual(result.metric_name, "RecordCount")
                self.assertEqual(result.value, 44)


    def test_record_count_Json_case1(self):
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file_path = temp_file.name

                data =[
    {
      "id": 1,
      "name": "Clownfish",
      "species": "Amphiprioninae",
      "size": {
        "length": "10 cm",
        "weight": "250 g"
      },
      "habitat": {
        "ocean": "Pacific Ocean",
        "reef": "Coral Reefs",
        "depth": "1-50 meters"
      },
      "diet": ["Algae", "Zooplankton", "Small Invertebrates"],
      "predators": ["Moray Eels", "Larger Fish"],
      "conservation_status": "Least Concern"
    },
    {
      "id": 2,
      "name": "Great White Shark",
      "species": "Carcharodon carcharias",
      "size": {
        "length": "6 meters",
        "weight": "1,100 kg"
      },
      "habitat": {
        "ocean": "Pacific Ocean",
        "reef": "Open Water",
        "depth": "50-200 meters"
      },
      "diet": ["Seals", "Fish", "Dolphins"],
      "predators": ["Orcas", "Humans"],
      "conservation_status": "Vulnerable"
    },
    {
      "id": 3,
      "name": "Anglerfish",
      "species": "Lophiiformes",
      "size": {
        "length": "1.5 meters",
        "weight": "100 kg"
      },
      "habitat": {
        "ocean": "Atlantic Ocean",
        "reef": "Deep Sea",
        "depth": "200-2,000 meters"
      },
      "diet": ["Fish", "Crustaceans"],
      "predators": ["Larger Fish"],
      "conservation_status": "Least Concern"
    },
    None,
    {
      "id": 4,
      "name": "Blue Tang",
      "species": "Paracanthurus hepatus",
      "size": {
        "length": "25 cm",
        "weight": "80 g"
      },
      "habitat": None,
      "diet": ["Algae", "Plankton"],
      "predators": ["Groupers", "Sharks"],
      "conservation_status": "Near Threatened"
    },
    None
  ]

                dataframe = pd.json_normalize(data)
                dataframe.to_json(temp_file_path, index=False)

                result = RecordCount().calculate(data=pd.read_json(temp_file_path))
                self.assertEqual(result.value, 4)

    def test_record_count_Json_case2(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file_path = temp_file.name

            data = [
    {
        "caterer_id": None,
        "name": None,
        "city": None,
        "menu": None
    },
    {
        "caterer_id": None,
        "name": None,
        "city": None,
        "menu": None
    },
    {
        "caterer_id": None,
        "name": None,
        "city": None,
        "menu": None
    },
    {
        "caterer_id": 4,
        "name": "Catering Delights",
        "city": "Miami",
        "menu": [
            {"dish_name": "Chicken Parmesan", "category": "Main", "price": 18.99},
            {"dish_name": "Greek Salad", "category": "Appetizer", "price": 7.49},
            {"dish_name": "Cheesecake", "category": "Dessert", "price": 6.49}
        ]
    },
    {
        "caterer_id": 5,
        "name": "Healthy Harvest",
        "city": "Austin",
        "menu": [
            {"dish_name": "Vegan Tacos", "category": "Main", "price": 12.99},
            {"dish_name": "Kale Caesar Salad", "category": "Appetizer", "price": 6.49},
            {"dish_name": "Coconut Macaroons", "category": "Dessert", "price": 4.99}
        ]
    },
    {
        "caterer_id": 6,
        "name": "Sushi Supreme",
        "city": "San Francisco",
        "menu": [
            {"dish_name": "Sushi Platter", "category": "Main", "price": 35.99},
            {"dish_name": "Miso Soup", "category": "Appetizer", "price": 3.99},
            {"dish_name": "Green Tea Ice Cream", "category": "Dessert", "price": 4.49}
        ]
    },
    {
        "caterer_id": 7,
        "name": "Flavors of the World",
        "city": "Seattle",
        "menu": [
            {"dish_name": "Paella", "category": "Main", "price": 28.99},
            {"dish_name": "Bruschetta", "category": "Appetizer", "price": 7.99},
            {"dish_name": "Churros", "category": "Dessert", "price": 5.99}
        ]
    },
    {
        "caterer_id": 8,
        "name": "Grand Gala Catering",
        "city": "Dallas",
        "menu": [
            {"dish_name": "Prime Rib", "category": "Main", "price": 40.99},
            {"dish_name": "Cauliflower Soup", "category": "Appetizer", "price": 6.99},
            {"dish_name": "Apple Pie", "category": "Dessert", "price": 4.49}
        ]
    },
    {
        "caterer_id": 9,
        "name": "Rustic Table",
        "city": "Portland",
        "menu": [
            {"dish_name": "Wood-fired Pizza", "category": "Main", "price": 16.99},
            {"dish_name": "Roasted Vegetables", "category": "Appetizer", "price": 5.49},
            {"dish_name": "Peach Cobbler", "category": "Dessert", "price": 5.99}
        ]
    },
    {
        "caterer_id": 10,
        "name": "Culinary Creations",
        "city": "Denver",
        "menu": [
            {"dish_name": "Braised Short Ribs", "category": "Main", "price": 36.99},
            {"dish_name": "Spinach Artichoke Dip", "category": "Appetizer", "price": 8.99},
            {"dish_name": "Chocolate Mousse", "category": "Dessert", "price": 7.49}
        ]
    },
    {
        "caterer_id": 11,
        "name": "Tasty Treats",
        "city": "Boston",
        "menu": [
            {"dish_name": "Lobster Roll", "category": "Main", "price": 30.99},
            {"dish_name": "Clam Chowder", "category": "Appetizer", "price": 6.49},
            {"dish_name": "Blueberry Muffin", "category": "Dessert", "price": 3.99}
        ]
    },
    {
        "caterer_id": 12,
        "name": "Mediterranean Delights",
        "city": "Las Vegas",
        "menu": [
            {"dish_name": "Lamb Shawarma", "category": "Main", "price": 22.99},
            {"dish_name": "Hummus and Pita", "category": "Appetizer", "price": 5.99},
            {"dish_name": "Baklava", "category": "Dessert", "price": 4.49}
        ]
    },
    {
        "caterer_id": 13,
        "name": "Spicy Bites",
        "city": "Phoenix",
        "menu": [
            {"dish_name": "Spicy Chicken Wings", "category": "Main", "price": 12.99},
            {"dish_name": "Guacamole and Chips", "category": "Appetizer", "price": 6.49},
            {"dish_name": "Churros", "category": "Dessert", "price": 4.99}
        ]
    },
    {
        "caterer_id": 14,
        "name": "Classic Comfort",
        "city": "Houston",
        "menu": [
            {"dish_name": "Mac and Cheese", "category": "Main", "price": 9.99},
            {"dish_name": "Chicken Tenders", "category": "Appetizer", "price": 7.99},
            {"dish_name": "Brownie Sundae", "category": "Dessert", "price": 5.49}
        ]
    },
    {
        "caterer_id": 15,
        "name": "Southern Cooking",
        "city": "Atlanta",
        "menu": [
            {"dish_name": "Fried Chicken", "category": "Main", "price": 14.99},
            {"dish_name": "Collard Greens", "category": "Appetizer", "price": 5.49},
            {"dish_name": "Peach Cobbler", "category": "Dessert", "price": 6.49}
        ]
    },
    {
        "caterer_id": 16,
        "name": "Vegan Vibes",
        "city": "San Diego",
        "menu": [
            {"dish_name": "Tofu Stir Fry", "category": "Main", "price": 11.99},
            {"dish_name": "Avocado Toast", "category": "Appetizer", "price": 5.99},
            {"dish_name": "Coconut Yogurt Parfait", "category": "Dessert", "price": 4.49}
        ]
    },
    {
        "caterer_id": 17,
        "name": "Farm to Fork",
        "city": "Minneapolis",
        "menu": [
            {"dish_name": "Beef Stew", "category": "Main", "price": 16.99},
            {"dish_name": "Arugula Salad", "category": "Appetizer", "price": 7.99},
            {"dish_name": "Apple Crisp", "category": "Dessert", "price": 5.49}
        ]
    },
    {
        "caterer_id": 18,
        "name": "Luxury Plates",
        "city": "Washington, D.C.",
        "menu": [
            {"dish_name": "Wagyu Beef", "category": "Main", "price": 70.99},
            {"dish_name": "Caviar", "category": "Appetizer", "price": 49.99},
            {"dish_name": "Crème Brûlée", "category": "Dessert", "price": 8.99}
        ]
    },
    {
        "caterer_id": 19,
        "name": "Noodle House",
        "city": "Portland",
        "menu": [
            {"dish_name": "Ramen", "category": "Main", "price": 10.99},
            {"dish_name": "Edamame", "category": "Appetizer", "price": 4.99},
            {"dish_name": "Mochi", "category": "Dessert", "price": 3.99}
        ]
    },
    {
        "caterer_id": 20,
        "name": "Comfort Catering",
        "city": "St. Louis",
        "menu": [
            {"dish_name": "Pulled Pork Sandwich", "category": "Main", "price": 12.99},
            {"dish_name": "Coleslaw", "category": "Appetizer", "price": 4.49},
            {"dish_name": "Banana Pudding", "category": "Dessert", "price": 5.49}
        ]
    },
    {
        "caterer_id": 21,
        "name": "Delicious Dining",
        "city": "Salt Lake City",
        "menu": [
            {"dish_name": "Chicken Marsala", "category": "Main", "price": 18.99},
            {"dish_name": "Brussels Sprouts", "category": "Appetizer", "price": 6.49},
            {"dish_name": "Lemon Sorbet", "category": "Dessert", "price": 3.99}
        ]
    },
    {
        "caterer_id": 22,
        "name": "Modern Cuisine",
        "city": "Philadelphia",
        "menu": [
            {"dish_name": "Beef Wellington", "category": "Main", "price": 45.99},
            {"dish_name": "Arancini", "category": "Appetizer", "price": 7.99},
            {"dish_name": "Raspberry Tart", "category": "Dessert", "price": 5.49}
        ]
    },
    {
        "caterer_id": 23,
        "name": "Picnic Perfection",
        "city": "New Orleans",
        "menu": [
            {"dish_name": "Shrimp Po'Boy", "category": "Main", "price": 15.99},
            {"dish_name": "Gumbo", "category": "Appetizer", "price": 8.99},
            {"dish_name": "Beignets", "category": "Dessert", "price": 4.99}
        ]
    },
    {
        "caterer_id": 24,
        "name": "Banquet Bliss",
        "city": "Detroit",
        "menu": [
            {"dish_name": "Grilled Chicken", "category": "Main", "price": 18.49},
            {"dish_name": "Cauliflower Soup", "category": "Appetizer", "price": 5.99},
            {"dish_name": "Lemon Cake", "category": "Dessert", "price": 4.99}
        ]
    },
    {
        "caterer_id": 25,
        "name": "Elegant Events",
        "city": "Miami",
        "menu": [
            {"dish_name": "Salmon en Papillote", "category": "Main", "price": 29.99},
            {"dish_name": "Spinach Salad", "category": "Appetizer", "price": 6.49},
            {"dish_name": "Lemon Cheesecake", "category": "Dessert", "price": 6.99}
        ]
    },
    {
        "caterer_id": 26,
        "name": "Tasty Treats",
        "city": "Indianapolis",
        "menu": [
            {"dish_name": "Chicken Alfredo", "category": "Main", "price": 17.99},
            {"dish_name": "Caprese Skewers", "category": "Appetizer", "price": 7.99},
            {"dish_name": "Lemon Bars", "category": "Dessert", "price": 4.49}
        ]
    },
    {
        "caterer_id": 27,
        "name": "Baked Goods",
        "city": "Kansas City",
        "menu": [
            {"dish_name": "BBQ Ribs", "category": "Main", "price": 22.99},
            {"dish_name": "Cornbread", "category": "Appetizer", "price": 5.49},
            {"dish_name": "Apple Pie", "category": "Dessert", "price": 5.99}
        ]
    },
    {
        "caterer_id": 28,
        "name": "Fiesta Feast",
        "city": "Houston",
        "menu": [
            {"dish_name": "Chicken Enchiladas", "category": "Main", "price": 14.99},
            {"dish_name": "Guacamole", "category": "Appetizer", "price": 6.99},
            {"dish_name": "Churros", "category": "Dessert", "price": 4.49}
        ]
    },
    {
        "caterer_id": 29,
        "name": "Gourmet Gatherings",
        "city": "Cleveland",
        "menu": [
            {"dish_name": "Beef Tenderloin", "category": "Main", "price": 38.99},
            {"dish_name": "Cauliflower Soup", "category": "Appetizer", "price": 5.99},
            {"dish_name": "Chocolate Cake", "category": "Dessert", "price": 6.99}
        ]
    },
    None,
    {
        "caterer_id": 30,
        "name": "Funky Fusion",
        "city": "Nashville",
        "menu": [
            None
        ]
    }
]
            dataframe = pd.json_normalize(data)
            dataframe.to_json(temp_file_path, index=False)

            result = RecordCount().calculate(data=pd.read_json(temp_file_path))
            self.assertEqual(result.value, 27)