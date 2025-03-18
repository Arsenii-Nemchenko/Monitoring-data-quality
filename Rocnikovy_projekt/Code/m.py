from abc import ABC, abstractmethod

import pandas as pd

from enums import FileType


class MyAbstractClass(ABC):
    @abstractmethod
    def my_method(self, value: int):
        pass

class MyClassA(MyAbstractClass):
    def my_method(self, value: int):
        print(f"MyClassA received: {value}")



class MyClassC(MyAbstractClass):
    def my_method(self, value: int, extra: int):  # This is a new method, NOT an override
        print(f"MyClassC received two values: {value} and {extra}")


print(isinstance(FileType.CSV, FileType))
data = [{"p": 1}, {"p": 6.10}]

df = pd.json_normalize(data)
for index, val in df.iterrows():
    print(val.dtype == "float64")
    print(val)
    print(isinstance(val, (int, float)))

print(isinstance(df["p"], (int, float)))


