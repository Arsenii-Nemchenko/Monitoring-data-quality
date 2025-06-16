import threading
from PyQt5.QtCore import QThread, pyqtSignal, QMutexLocker, QMutex


class CalculationThread(QThread):
    plot_ready = pyqtSignal(list, list, str, str)
    calculation_error = pyqtSignal(str)

    def __init__(self, graph_widget, monitoring, metric_name, interval, column, is_column_metric):
        super().__init__()
        self.graph_widget = graph_widget
        self.monitoring = monitoring
        self.metric_name = metric_name
        self.interval = interval
        self.column = column
        self.is_column_metric = is_column_metric
        self._stop_flag = False
        self._connection = True
        self._mutex = QMutex()
        self.plot_ready.connect(self.graph_widget.plot)

    def stop(self):
        with QMutexLocker(self._mutex):
            self._stop_flag = True

        if self._connection:
            self.plot_ready.disconnect()
            self._connection = False

        with QMutexLocker(self.monitoring.mutex):
            self.monitoring.data_condition.wakeAll()
            self.monitoring.calculation_condition.wakeAll()

    def run(self):
        try:

            initial_data_ready = False
            with QMutexLocker(self.monitoring.mutex):

                initial_data_ready = self.monitoring.is_initial_data_ready()
                if self._stop_flag:
                    return

            # Wait for initial data
            while not initial_data_ready and not self._stop_flag:
                with QMutexLocker(self.monitoring.mutex):

                    if self.monitoring.is_initial_data_ready():
                        break

                    self.monitoring.data_condition.wait(self.monitoring.mutex)
                    initial_data_ready = self.monitoring.is_initial_data_ready()

            if self._stop_flag:
                return


            # Main processing loop
            while not self._stop_flag:
                self.monitoring.signal_calculation_start()
                self.perform_calculation()
                with QMutexLocker(self.monitoring.mutex):
                    self.monitoring.signal_calculation_end()

                with QMutexLocker(self.monitoring.mutex):
                    if self._stop_flag:
                        break
                    self.monitoring.data_condition.wait(self.monitoring.mutex, (self.interval * 1000))

        except Exception as e:
            self.calculation_error.emit(f"Calculation thread error: {str(e)}")
            self.monitoring.signal_calculation_end()
        finally:
            self.deleteLater()

    def perform_calculation(self):
        try:
            with QMutexLocker(self.monitoring.mutex):
                batch_files = self.monitoring.get_batch_files(self.column)
                if not batch_files:
                    raise ValueError(f"No batch files available for column {self.column}")

                data = [bf.get_metric_value(self.metric_name) for bf in batch_files]

            if len(data) == 0:
                return

            data = [item for sublist in data for item in sublist]
            if data:
                values, timestamps = zip(*data)
                if self.is_column_metric:
                    self.plot_ready.emit(
                        list(timestamps),
                        list(values),
                        f"{self.metric_name} over time",
                        self.column
                    )
                else:
                    self.plot_ready.emit(
                        list(timestamps),
                        list(values),
                        f"{self.metric_name} over time",
                        None
                    )
        except Exception as e:
            print(f"I just crashed {str(e)}")