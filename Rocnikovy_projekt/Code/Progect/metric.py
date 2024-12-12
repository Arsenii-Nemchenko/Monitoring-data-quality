from abc import ABC, abstractmethod
from pandas import DataFrame, json_normalize

from Progect.metric_value import MetricValue


# abstract Metric class
class Metric(ABC):
    @abstractmethod
    def calculate(self, data: DataFrame):
        pass


class RecordCount(Metric):
    def calculate(self, data : DataFrame):
        return MetricValue("RecordCount" ,data.shape[0])

class EmptyRecordCount(Metric):
    def calculate(self, data : DataFrame):
        isNullObject = data.isna()
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

        return MetricValue("EmptyRecordCount", counter)

class NullRecordCount(Metric):
    def calculate(self, data : DataFrame):
        return MetricValue("NullObjectCount", self.count_null_objects(data))

    def count_null_objects(self, data):
        null_object_count =0
        for index, row in data.iterrows():
            if row.isnull().all():
                null_object_count += 1


        return null_object_count