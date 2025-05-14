import threading
from PyQt5.QtCore import QThread, pyqtSignal


class CalculationThread(QThread):
    plot_ready = pyqtSignal(list, list, str)

    def __init__(self, graph_widget, monitoring, metric_name, interval_sec):
        super().__init__()
        self.graph_widget = graph_widget
        self.monitoring = monitoring
        self.metric_name = metric_name
        self.interval_sec = interval_sec
        self._stop_event = threading.Event()
        self.plot_ready.connect(self.graph_widget.plot)

    def stop(self):
        self._stop_event.set()

    def _run(self):
        print("Calculation thread started")

        # Wait until batch_files are available
        with self.monitoring.condition:
            while not self.monitoring.batch_files and not self._stop_event.is_set():
                print("Waiting for batch files")
                self.monitoring.condition.wait(timeout=2)

        if self._stop_event.is_set():
            return

        self.perform_calculation()

        while not self._stop_event.is_set():
            self._stop_event.wait(self.interval_sec)
            if self._stop_event.is_set():
                break
            self.perform_calculation()

    def perform_calculation(self):
        try:
            with self.monitoring.lock:
                data = [bf.get_metric_value(self.metric_name) for bf in self.monitoring.batch_files]
            if not data:
                raise AttributeError(f"No data available for {self.metric_name} metric!")

            data = [item for sublist in data for item in sublist]
            if data:
                values, timestamps = zip(*data)
                self.plot_ready.emit(list(timestamps), list(values), f"{self.metric_name} over time")
        except Exception as e:
            print(f"Calculation error for metric '{self.metric_name}': {e}")

    def run(self):
        try:
            self._run()
        except Exception as e:
            print(f"Calculation thread error: {e}")