from enum import Enum

# FileType enum (3 values - "CSV", "JSON", "Parquet")
class FileType(Enum):
    PARQUET = "Parquet"
    CSV = "CSV"
    JSON = "JSON"
