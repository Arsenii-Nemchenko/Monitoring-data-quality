import traceback

from PyQt5.QtCore import QThread
import threading
import time


class MonitoringThread(QThread):
    def __init__(self, monitoring, interval):
        super().__init__()
        self.monitoring = monitoring
        self.interval = interval
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            while not self._stop_event.is_set():
                print("Monitoring")
                self.monitoring.start_monitoring()
                time.sleep(self.interval)
        except Exception as e:
            print(f"Monitoring thread error: {e}")