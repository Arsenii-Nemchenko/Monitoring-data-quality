import os
import threading

import pyarrow.parquet as pq
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from .calculation_thread import CalculationThread
from .metric_factory import MetricFactory
from .monitored_window import MonitoredFileWindow
from .multi_selected_combobox import MultiSelectComboBox
from ..src.database_manager import DBManager
from ..src.data_monitor import DataMonitor
from ..src.metric import *
from .graph import GraphWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.calc_thread = None
        self.monitor_thread = None
        self.setWindowTitle("Monitoring data quality")
        self.resize(1500, 500)

        regular_metrics =  [RecordCount(), RecordCountJson(), EmptyRecordCount(), NullObjectCount(), EmptyObjectCount(),
                             DuplicateRecordCount()]

        column_metrics = [NullValuesCountColumn(), NullValuesCountJson(), DefinedPathCount(),
                                    UniqueValuesCountJson(), UniqueValuesCount(), AverageValue(), AverageValueJson()]
        self.metric_factory = MetricFactory()
        self.database_manager = DBManager(regular_metrics + column_metrics)
        self.current_window = None
        self.current_columns = []
        self.working_directories = []
        self.monitored_file_window = MonitoredFileWindow(self.database_manager)
        self.monitored_files = {}
        self.monitored_file_windows = {}

        self.mutex = QMutex()
        #Pivot layout
        layout = QHBoxLayout()

        layout1 = QVBoxLayout()

        layout_header = QHBoxLayout()
        layout_header.setSpacing(5)
        layout_header.setAlignment(Qt.AlignRight)
        header_name = QLabel("Add new monitored folder")


        self.remove_file_button = QPushButton("Remove")
        self.remove_file_button.clicked.connect(self.remove_selected_file)

        plus_button = QPushButton("+")
        plus_button.setFixedSize(50, 50)
        plus_button.setStyleSheet("""
                   QPushButton {
                       border-radius: 20px;
                       background-color: #0f1436;
                       color: white;
                       font-size: 24px;
                   }
                   QPushButton:hover {
                       background-color: #313764;
                   }
                   QPushButton:pressed {
                       background-color: #313764;
                   }
               """)
        plus_button.clicked.connect(self._get_working_directory)
        layout_header.addWidget(self.remove_file_button, 30)
        layout_header.addWidget(header_name, 30)
        layout_header.addWidget(plus_button, 40)

        #Current directory files
        layout_directory_files = QHBoxLayout()
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.reload_current_directory)
        layout_directory_files.addWidget(self.file_list)




        #Adition to left pivot layout
        layout1.addLayout(layout_header)
        layout1.addLayout(layout_directory_files)


        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0, 0, 0, 0)
        layout2.setSpacing(5)

        #Metric layout
        layout2_1 = QHBoxLayout()
        layout2_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout2_1.setContentsMargins(0,0,0,0)
        layout2_1.setSpacing(10)


        #Metric type
        self.metric_type_selector = MultiSelectComboBox(["Regular", "Column"], self.update_select_metrics)
        layout2_1.addWidget(QLabel("Metric Type:"))
        layout2_1.addWidget(self.metric_type_selector)

        #Time interval
        time_interval_label = QLabel("Time Interval (seconds):")
        self.time_interval_input = QSpinBox()
        self.time_interval_input.setMinimum(1)
        self.time_interval_input.setMaximum(3600)
        self.time_interval_input.setValue(10)

        layout2_1.addWidget(time_interval_label)
        layout2_1.addWidget(self.time_interval_input)


        #Metric selection
        self.select_metrics = MultiSelectComboBox([])
        self.select_metrics.setMinimumSize(150, 30)

        layout2_1.addWidget(QLabel("Select Metrics:"))
        layout2_1.addWidget(self.select_metrics)

        #Calculate metric
        self.calculate_button = QPushButton("Show")
        self.calculate_button.clicked.connect(self.calculate)

        layout2_1.addWidget(self.calculate_button)

        self.shown_graph = GraphWidget()

        layout2_2 = QVBoxLayout()
        layout2_2.setContentsMargins(0, 0, 0, 0)
        layout2_2.setSpacing(10)

        self.show_metric = QComboBox()
        line_edit_metric = QLineEdit()
        line_edit_metric.setPlaceholderText("Show")
        self.show_metric.setLineEdit(line_edit_metric)

        self.show_metric.currentIndexChanged.connect(self.update_current_metric)

        layout2_2.addWidget(self.shown_graph)

        #Shown metric layout
        layout_shown_metric = QHBoxLayout()
        layout_shown_metric.setContentsMargins(0, 0, 0, 0)
        layout_shown_metric.setSpacing(10)


        self.column_button = QComboBox()
        self.last_column = None
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Column")
        self.column_button.setLineEdit(self.line_edit)


        self.line_edit.editingFinished.connect(self.validate_jsonpath)
        self.line_edit.editingFinished.connect(self.save_column)

        layout_shown_metric.addWidget(QLabel("Show Metrics:"))
        layout_shown_metric.addWidget(self.show_metric)
        layout_shown_metric.addWidget(self.column_button)

        layout2.addLayout(layout2_1)
        layout2.addLayout(layout_shown_metric)
        layout2.addLayout(layout2_2)

        layout.addLayout(layout1, 40)
        layout.addLayout(layout2, 60)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.update_select_metrics()

    def remove_selected_file(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            return

        self.stop_threads()

        name = selected_item.text()

        if name in self.monitored_files:
            directory = self.monitored_files[name].folder

            if self.monitor_thread and self.monitor_thread.name == name:
                self.monitor_thread.stop()
                self.monitor_thread = None
                self.current_window = None

            del self.monitored_files[name]
            if name in self.monitored_file_windows:
                del self.monitored_file_windows[name]

            if directory in self.working_directories:
                self.working_directories.remove(directory)

        row = self.file_list.row(selected_item)
        self.file_list.takeItem(row)

        self.shown_graph.clear_graph()
        self.column_button.clear()
        self.current_columns = []
        self.last_column = None
        self.show_metric.clear()
        self.select_metrics.clear()
        self.metric_type_selector.set_selected_options([])
        self.time_interval_input.setValue(10)

        self.current_window = None
        self.monitor_thread = None

        if not self.monitor_thread:
            self.shown_graph.clear_graph()
            self.column_button.clear()
            self.current_columns = []
            self.last_column = None

    def update_select_metrics(self):
        selected_types = self.metric_type_selector.selected_options

        prev_selected = self.select_metrics.selected_options.copy()

        if "Regular" in selected_types and "Column" in selected_types:
            options = {item for item in
                       self.database_manager.get_regular_metrics() + self.database_manager.get_column_metrics()}
        elif "Regular" in selected_types:
            options = {item for item in self.database_manager.get_regular_metrics()}
        elif "Column" in selected_types:
            options = {item for item in self.database_manager.get_column_metrics()}
        else:
            options = set()

        new_options = []
        for option in options:
            if not self.monitor_thread is None and option == "DefinedPathCount" and self.monitor_thread.file_format.value.lower() != 'json':
                continue
            new_options.append(option)

        valid_selection = prev_selected & options

        self.select_metrics.set_options(new_options, selected=valid_selection)

    def update_shown_metric(self):
        selected_metrics = self.select_metrics.selected_options
        self.show_metric.clear()

        if selected_metrics:
            self.show_metric.addItems(selected_metrics)
        else:
            self.show_metric.addItem("Show")

    def update_current_metric(self):
        text = self.show_metric.currentText()
        if text != "Show" and self.calc_thread:
            if not self.validate_column_for_metric():
                self.stop_threads()
                return

            if text in self.database_manager.get_column_metrics():

                current_col = self.column_button.currentText()
                if not current_col:
                    if not self.validate_column():
                        return
                elif self.monitor_thread.file_format == FileType.JSON and not self.validate_jsonpath():

                    if not self.validate_column():
                        return

                # Update only if column changed
                if current_col != self.last_column:
                    self.last_column = current_col
                self.update_thread()
            else:
                self.update_thread()
        else:
            self.shown_graph.clear_graph()

    def validate_jsonpath(self):
        if self.monitor_thread and self.monitor_thread.file_format == FileType.JSON:
            pattern = r'^\$(\.\*|\.\w[\w\s]*|\[\"[^\"]+\"\]|\[\d+\]|\[\*\])+$'
            return bool(re.fullmatch(pattern, self.line_edit.text()))
        return True

    def save_column(self):
        self.last_column = self.line_edit.text()

    def validate_column_for_metric(self):
        current_metrics = []
        for i in range(0, self.show_metric.count()):
            if self.show_metric.itemText(i) != "Show":
                current_metrics.append(self.show_metric.itemText(i))

        column_metrics = self.database_manager.get_column_metrics()

        # Only validate if the selected metrics contain a column metric
        if any(current_metric in column_metrics for current_metric in current_metrics):
            if not self.monitor_thread:
                QMessageBox.warning(self, "Warning", "No monitoring configuration selected")
                self.shown_graph.clear_graph()
                return False

            # For JSON files, check if JSON path is valid
            if self.monitor_thread.file_format == FileType.JSON:
                if not self.line_edit.text() or not self.validate_jsonpath():
                    QMessageBox.warning(self, "Column Required",
                                        f"Please enter a valid JSON path")
                    self.shown_graph.clear_graph()
                    return False
                return True

            # For other formats, check if a column is selected
            if not self.column_button.currentText():
                QMessageBox.warning(self, "Column Required",
                                    f"Please select a column")
                self.shown_graph.clear_graph()
                return False

        return True


    #Getting directory and setting up the data
    def _get_working_directory(self):
        try:
            self.monitored_file_window = MonitoredFileWindow(self.database_manager)

            result = self.monitored_file_window.exec_()

            if result == QDialog.Accepted:
                data_description = self.monitored_file_window.description_text.toPlainText()
                metric_types_selected = self.monitored_file_window.metric_type_selector.selected_options
                time_interval = self.monitored_file_window.time_interval_input_right.value()
                selected_column_metrics = self.monitored_file_window.selected_column
                selected_regular_metrics = self.monitored_file_window.selected_regular
                new_directory = self.monitored_file_window.new_directory
                name = self.monitored_file_window.name_text.text()
                file_format = self.monitored_file_window.file_type_selector.currentText().lower()

                state = {"description": data_description, "metric_types": metric_types_selected,
                         "time": time_interval, "column_metrics": selected_column_metrics,
                         "regular_metrics": selected_regular_metrics, "directory": new_directory, "name": name, "file_format": file_format, "column": None}
                self.monitored_file_windows[name] = state
                self.monitored_files[name] = DataMonitor(name, new_directory, data_description, selected_regular_metrics, selected_column_metrics,
                                                         file_format,self.database_manager, self.column_button.currentText(), time_interval)

                self.add_monitored_item(name, file_format, new_directory)
                self.working_directories.append(new_directory)

                #Setting up the widgets according to the data
                if self.current_window is None:
                    self.monitor_thread = self.monitored_files.get(name)
                    self.current_window = state
                    self.load_interface(metric_types_selected, selected_column_metrics, selected_regular_metrics, time_interval)
                    self.load_columns_from_directory()
        except OSError:
            pass

    def add_monitored_item(self, name, file_format, directory):
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(10)

        name_label = QLabel(name)
        format_label = QLabel(file_format)
        format_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(name_label)
        layout.addStretch()
        layout.addWidget(format_label)
        widget.setLayout(layout)

        list_item = QListWidgetItem()
        list_item.setData(Qt.UserRole, name)
        list_item.setToolTip(directory)
        list_item.setSizeHint(widget.sizeHint())

        self.file_list.addItem(list_item)
        self.file_list.setItemWidget(list_item, widget)

    def load_columns_from_directory(self):
        try:
            self.current_columns = []
            for filename in os.listdir(self.monitor_thread.folder):
                file_path = os.path.join(self.monitor_thread.folder, filename)

                if self.monitor_thread.file_format == FileType.CSV and filename.endswith(".csv"):
                    df = pd.read_csv(file_path, nrows=1)
                    self.current_columns = df.columns.tolist()

                elif self.monitor_thread.file_format == FileType.PARQUET and filename.endswith(".parquet"):
                    table = pq.read_table(file_path)
                    self.current_columns = table.schema.names

            self.column_button.clear()

            if self.current_columns:
                self.column_button.addItems(self.current_columns)
                self.last_column = (
                        self.current_window.get("column") or
                        self.current_columns[0]
                )
                if self.monitor_thread.file_format == FileType.JSON:
                    self.column_button.setCurrentText(self.last_column)
        except Exception as e:
            print(f"Error reading columns from directory: {e}")
            self.current_columns = []

    def reload_current_directory(self, item):
        name = item.data(Qt.UserRole)
        if not name or name not in self.monitored_files:
            QMessageBox.warning(self, "Error", "Invalid directory selection")
            return

        # Stop existing threads
        self.stop_threads()
        self.save_changes()

        self.monitor_thread = self.monitored_files[name]
        self.current_window = self.monitored_file_windows[name]

        self.load_interface(
            self.current_window.get("metric_types", set()),
            self.current_window.get("column_metrics", []),
            self.current_window.get("regular_metrics", []),
            self.current_window.get("time")
        )

        self.load_columns_from_directory()

    def load_interface(self, metric_types_selected, selected_column_metrics, selected_regular_metrics, time_interval):
        self.metric_type_selector.set_selected_options(metric_types_selected)
        self.update_select_metrics()

        selected_help = selected_column_metrics + selected_regular_metrics
        self.select_metrics.set_selected_options(selected_help)

        self.time_interval_input.setValue(time_interval)
        self.update_shown_metric()

    def save_changes(self):
        self.current_window["metric_types"] = set(self.metric_type_selector.selected_options)
        self.current_window["time"] = self.time_interval_input.value()

        selected_metrics = self.select_metrics.selected_options

        selected_column = []
        selected_regular = []
        self.divide_metrics(selected_metrics, selected_column, selected_regular)
        self.current_window["column_metrics"] = selected_column
        self.current_window["regular_metrics"] = selected_regular
        self.current_window["column"] = self.last_column

    def divide_metrics(self, selected, selected_column, selected_regular):
        column = self.database_manager.get_column_metrics()

        for metric in selected:
            if metric in column:
                selected_column.append(metric)
            else:
                selected_regular.append(metric)

    def calculate(self):
        if not self.current_window:
            return
        self.stop_threads()
        if not self.validate_column_for_metric():
            return

        self.update_shown_metric()
        self.start_threads()

    def start_threads(self):
        # Create new DataMonitor instance with current settings
        name = self.current_window.get("name")
        directory = self.current_window.get("directory")
        data_description = self.current_window.get("description")
        file_format = self.current_window.get("file_format")

        column_metrics_names = []
        regular_metrics_names = []
        self.divide_metrics([self.show_metric.currentText()], column_metrics_names, regular_metrics_names)

        regular_metrics = [self.metric_factory.get(name, file_format) for name in regular_metrics_names]
        column_metrics = [self.metric_factory.get(name, file_format) for name in column_metrics_names]

        was_before = False
        processed_files = None
        data_batch_files = None
        # Create new monitor thread
        if self.monitor_thread:
            was_before = True
            processed_files = self.monitor_thread.processed_files
            data_batch_files = self.monitor_thread.batch_files

        self.monitor_thread = DataMonitor(
            name, directory, data_description,
            regular_metrics, column_metrics,
            file_format, self.database_manager,
            self.column_button.currentText(), self.time_interval_input.value()
        )
        if was_before:
            self.monitor_thread.processed_files = processed_files
            self.monitor_thread.batch_files = data_batch_files

        self.monitor_thread.invalid_json_path.connect(self.handle_invalid_json_path)
        self.monitor_thread.start()

        is_column_metric = True if self.show_metric.currentText() in self.database_manager.get_column_metrics() else False
        self.calc_thread = CalculationThread(
            graph_widget=self.shown_graph,
            monitoring=self.monitor_thread,
            metric_name=self.show_metric.currentText(),
            interval=self.time_interval_input.value(),
            column=self.column_button.currentText(),
            is_column_metric=is_column_metric
        )
        self.calc_thread.start()

    def stop_threads(self):
        if hasattr(self, 'calc_thread') and self.calc_thread:
            try:
                self.calc_thread.stop()
                if not self.calc_thread.wait(500):
                    self.calc_thread.terminate()
                self.calc_thread.deleteLater()
            except Exception as e:
                print(f"Error stopping calculation thread: {e}")
            finally:
                self.calc_thread = None

        if hasattr(self, 'monitor_thread') and self.monitor_thread:
            self.monitor_thread.stop()

    def update_thread(self):
        try:
            self.stop_threads()

            is_column_metric = True if self.show_metric.currentText() in self.database_manager.get_column_metrics() else False
            self.calc_thread = CalculationThread(
                graph_widget=self.shown_graph,
                monitoring=self.monitor_thread,
                metric_name=self.show_metric.currentText(),
                interval=self.time_interval_input.value(),
                column=self.column_button.currentText(),
                is_column_metric=is_column_metric
            )

            regular_metrics_names = []
            column_metrics_names = []
            file_format = self.current_window.get("file_format")
            self.divide_metrics([self.show_metric.currentText()], column_metrics_names, regular_metrics_names)

            regular_metrics = [self.metric_factory.get(name, file_format) for name in regular_metrics_names]
            column_metrics = [self.metric_factory.get(name, file_format) for name in column_metrics_names]

            self.monitor_thread.set_arguments(regular_metrics, column_metrics, self.column_button.currentText(), self.time_interval_input.value())

            self.monitor_thread.start()
            self.calc_thread.start()
        except Exception as e:
            print(f"I got error updating threads {e}")
            self.shown_graph.clear_graph()

    def handle_invalid_json_path(self):
        self.stop_threads()
        QMessageBox.warning(self, "Invalid JSON Path",
                            "The specified JSON path was not found. Please select a valid path.")
        self.shown_graph.clear_graph()














app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()