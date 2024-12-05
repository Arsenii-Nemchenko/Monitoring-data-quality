import pandas as pd


#Pocet vsetkych zaznamov
dataframe = pd.read_csv(r"CSV examples\cars_sql_exaple.csv")

row_count = dataframe.shape[0]

print(f"Row count of this csv file is: {row_count}")

df_parquet = pd.read_parquet(r"Parquet_examples\flights-1m.parquet")

row_parq = df_parquet.shape[0]

print(f"Row count of this parquet file is: {row_parq}")

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

print(emptyLines(dataframe))



#Pocet praznych zaznamov v json subore
newDataFrame = pd.read_json(r"Json_examples\Employees.json")

print(emptyLines(newDataFrame))
        
