import os.path
import json
import pandas as pd
from database_manager import DBManager
from enums import FileType
from data_monitor import DataMonitor
from metric import RecordCount, EmptyRecordCount, NullObjectCount, EmptyObjectCount, DuplicateRecordCount

def main():
    folder = input("Enter the folder path: ")

    monitored_metrics = [RecordCount(), EmptyRecordCount(), NullObjectCount(), EmptyObjectCount(), DuplicateRecordCount()]
    #You can connect to your db by changing arguments. I dont mind if you use mine
    manager = create_db_manager("localhost","postgres", "postgres",
                                "ArsGrez2024", monitored_metrics)

    #Comment those two lines after processing files you want.
    # Results will be saved into db, so you can test whether values are stored in db and continue testing
    #monitor = DataMonitor("Monitored", folder, "Data", monitored_metrics, "json", manager)
    #monitor.start_monitoring()

    action = input("Enter action(database_test or metric_test): ")
    while action != "stop":
        match action:
            case "database_test":
                #Add to a folder your file before testing this
                #I guess it covers data batch file test
                file_name = input("Enter file name: ")
                metric_name = input("Enter metric name: ")
                file_type = input("Enter file format(Parquet, CSV or JSON)")
                time_stamp = input("Enter expected time stamp: (just sequence of 14 digits as in file name)")

                print(f"Stored value: {manager.get_value(file_name, metric_name, file_type, time_stamp)}")

                action = input("Enter action(database_test or metric_test or stop): ")
            case "metric_test":

                file_type = process_file_format(input("Enter file format: "))
                file_name = input("Enter file name: ")


                metrics_for_test_json = [RecordCount(), NullObjectCount(), EmptyObjectCount(), DuplicateRecordCount()]
                other_metrics = [RecordCount(), EmptyRecordCount(), DuplicateRecordCount()]
                data = None

                match file_type:
                    case FileType.JSON:
                        for metric in metrics_for_test_json:
                            data = get_data(metric.name)
                            print(f" Result of {metric.name} for {file_name} is {metric.calculate(data)}")

                    case FileType.PARQUET:
                        other_metrics_cl(file_name, file_type, other_metrics, folder)

                    case FileType.CSV:
                        other_metrics_cl(file_name, file_type, other_metrics, folder)
                    case _:
                        raise ValueError("Error!")
                action = input("Enter action(database_test or metric_test or stop): ")
            case _:
                action = input("Enter action(database_test or metric_test or stop): ")


def get_data(name: str, file_type, folder, file_name):
    return _get_parsed_data(file_type,
                            os.path.join("/", folder) + "\\" + file_name + "." + file_type.value.lower(),
                            name)

def create_db_manager(host, database, user, password, monitored_metrics):
    return DBManager(host, database, user, password, monitored_metrics)

def process_file_format(file_format: str):
        match file_format:
            case "JSON":
                return FileType.JSON
            case "CSV":
                return FileType.CSV
            case "Parquet":
                return FileType.PARQUET
            case _:
                raise ValueError("Unsupported file format!")


def _get_parsed_data(file_type, path, metric_name:str):
    match file_type:
        case FileType.JSON:
            with open(path, 'r') as file:
                data = json.load(file)
            if metric_name =='NullObjectCount' or metric_name == 'EmptyObjectCount':
                data = pd.json_normalize(data)

            return data
        case FileType.CSV:
            return pd.read_csv(path)
        case FileType.PARQUET:
            return pd.read_parquet(path)
        case _:
            raise ValueError(f"Unsupported file type: {file_type.value}")

def other_metrics_cl(f_name, f_type, metrics, folder):
    for metric in metrics:
        data = get_data(metric.name, f_type, folder, f_name)
        print(f" Result of {metric.name} for {f_name} is {metric.calculate(data).value}")


main()


