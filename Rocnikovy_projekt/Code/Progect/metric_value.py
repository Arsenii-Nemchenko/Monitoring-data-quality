from datetime import datetime
class MetricValue:
    def __init__(self, metric_name: str, value: float, timestamp: datetime):
        self.metric_name = metric_name
        self.value = value
        self.timestamp = timestamp