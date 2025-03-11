from unittest import TestCase
import tempfile
import pandas as pd

from Progect.metric import RecordCount


class TestClass(TestCase):
    def test_record_count_CSV_case1(self):
        # Path to Test_files -> CSV_cases -> cars_37rows_3empty_4duplicate.csv
        file_path = input("Enter path to cars_37rows_3empty_4duplicate.csv: ")

        result = RecordCount().calculate(data=pd.read_csv(file_path))
        self.assertEqual(result.metric_name, "RecordCount")
        self.assertEqual(result.value, 37)

    def test_record_count_CSV_case2(self):
        # Path to Test_files -> CSV_cases -> house_price_557rows_12duplicate.csv
        file_path = input("Enter path to house_price_557rows_12duplicate.csv: ")

        result = RecordCount().calculate(data=pd.read_csv(file_path))
        self.assertEqual(result.metric_name, "RecordCount")
        self.assertEqual(result.value, 545)

    def test_record_count_Parquet_case1(self):
        # Path to Test_files -> Parquet-cases -> sales_10rows.parquet
        file_path = input("Enter path to sales_10rows.parquet: ")

        result = RecordCount().calculate(data=pd.read_parquet(file_path))
        self.assertEqual(result.metric_name, "RecordCount")
        self.assertEqual(result.value, 10)

    def test_record_count_Parquet_case2(self):
        # Path to Test_files -> Parquet-cases -> car_owners_44rows.parquet
        file_path = input("Enter path to car_owners_44rows.parquet: ")

        result = RecordCount().calculate(data=pd.read_parquet(file_path))
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