import pandas as pd
import json

#Pocet vsetkych zaznamov

#Csv subor
df_csv = pd.read_csv(r"CSV examples\cars_sql_example_rows6.csv")

row_csv = df_csv.shape[0]

print(f"Row count of file cars_sql_example_rows6.csv is: {row_csv}")

#Parquet subor
df_parquet = pd.read_parquet(r"Parquet_examples\flights_rows1m.parquet")

row_parq = df_parquet.shape[0]

print(f"Row count of file flights_rows1m.parquet is: {row_parq}")

#Json subor
df_json = pd.read_json(r"Json_examples\house_price_rows545.json", lines=True)

row_json = df_json.shape[0]

print(f"Row count of file house_price_rows545.json is: {row_json}")

#Pocet praznych zaznamov
def emptyLines(dataframe):
    isNullObject = dataframe.isna()
    shape = isNullObject.shape
    
    counter = 0
    for i in range(shape[0]):
        found = True
        for j in range(shape[1]):
            if not isNullObject.iloc[i, j]:
                found = False
                break
        if found:
            counter+=1
            
    return counter

#Pocet praznych zaznamov v csv subore
df_csv_weather = pd.read_csv(r"CSV examples\weather_emptyline31.csv")

print(f"\nEmpty lines count of file weather_emptyline31.csv is:{emptyLines(df_csv_weather)}")



def preprocess_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)


    def clean(obj):
        if isinstance(obj, dict):
            
            cleaned_dict = {k: clean(v) for k, v in obj.items()}
            if all(v is None for v in cleaned_dict.values()):
                return None
            return cleaned_dict
        elif isinstance(obj, list):
            
            cleaned_list = [clean(item) for item in obj]
            if all(item is None for item in cleaned_list):
                return None
            return cleaned_list
        elif obj == "" or obj is None:
            return None
        else:
            return obj


    cleaned_data = clean(data)

    preprocessed_file_path = file_path.replace(".json", "_preprocessed.json")
    with open(preprocessed_file_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

    return preprocessed_file_path

def count_empty_objects(df):


    df = df.replace("", pd.NA)
    
    empty_object_count = df.isna().all(axis=1).sum()
    
    return empty_object_count


#Pocet praznych zaznamov v json subore
json_file_path = r"Json_examples\employees_with_nested_fields_emptyline3.json"

preprocessed_file_path = preprocess_json(json_file_path)

df_json_empl = pd.read_json(preprocessed_file_path)

print(f"Empty lines count of file employees_with_nested_fields_emptyline3.json is:{count_empty_objects(df_json_empl)}")

#Pocet praznych zaznamov v parquet subore
df_parquet_iris_emptyline101 = pd.read_parquet(r"Parquet_examples\iris_emptyline101.parquet")

print(f"Empty lines count of file iris_emptyline101.parquet is:{emptyLines(df_parquet_iris_emptyline101)}")



