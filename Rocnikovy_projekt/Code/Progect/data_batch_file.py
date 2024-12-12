import pandas as pd

import json
from enums import FileType
from pandas import json_normalize


class DataBatchFile:
    def __init__(self, file_path: str, file_type: FileType):
        self.file_path = file_path
        self.file_type = file_type

    def load_data(self):
        match self.file_type:
            case FileType.CSV:
                return pd.read_csv(self.file_path)
            case FileType.JSON:
                with open(self.file_path, 'r') as file:
                    data = json.load(file)

                data = json_normalize(data)
                return data
            case FileType.PARQUET:
                return pd.read_parquet(self.file_path)
            case _:
                raise ValueError(f"Unsupported file type: {self.file_type}")