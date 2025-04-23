import os
import pandas as pd
import pyarrow.parquet as pq
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from Gui.monitored_window import MonitoredFileWindow
from Gui.multi_selected_combobox import MultiSelectComboBox
from src.database_manager import DBManager
from src.data_monitor import DataMonitor
from src.metric import *
from graph import GraphWidget



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoring data quality")
        self.resize(1500, 500)

        regular_metrics =  [RecordCount(), RecordCountJson(), EmptyRecordCount(), NullObjectCount(), EmptyObjectCount(),
                             DuplicateRecordCount()]

        column_metrics = [NullValuesCountColumn(), NullValuesCountJson(), DefinedPathCount(),
                                    UniqueValuesCountJson(), UniqueValuesCount(), AverageValue(), AverageValueJson()]

        self.database_manager = DBManager(regular_metrics + column_metrics)
        self.current_monitoring = None
        self.current_window = None
        self.current_columns = []
        self.working_directories = []
        self.monitored_file_window = MonitoredFileWindow(self.database_manager)
        self.monitored_files = {}
        self.monitored_file_windows = {}
        #Pivot layout
        layout = QHBoxLayout()

        layout1 = QVBoxLayout()

        layout_header = QHBoxLayout()
        layout_header.setSpacing(5)
        layout_header.setAlignment(Qt.AlignRight)
        header_name = QLabel("Add monitored file")


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
        layout_header.addWidget(self.remove_file_button, 50)
        layout_header.addWidget(header_name, 30)
        layout_header.addWidget(plus_button, 20)

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
        self.select_metrics = MultiSelectComboBox([], self.update_shown_metric)
        self.select_metrics.setMinimumSize(150, 30)

        layout2_1.addWidget(QLabel("Select Metrics:"))
        layout2_1.addWidget(self.select_metrics)

        #Calculate metric
        self.calculate_button = QPushButton("Calculate")
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

        #TODO this connects behavior i wanted before, think about it
        #self.show_metric.currentIndexChanged.connect(self.update_current_metric)

        layout2_2.addWidget(self.shown_graph)

        #Shown metric layout
        layout_shown_metric = QHBoxLayout()
        layout_shown_metric.setContentsMargins(0, 0, 0, 0)
        layout_shown_metric.setSpacing(10)


        self.column_button = QComboBox()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Column")
        self.column_button.setLineEdit(self.line_edit)

        #LATER WILL BE CHANGED, SO FAR VALIDATES ONLY JSON
        #LOGIC WILL BE CHANGED
        self.line_edit.editingFinished.connect(self.validate_jsonpath)

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
        if selected_item:
            name = selected_item.text()
            if name in self.monitored_files:
                temp = self.monitored_files[name]
                directory = temp.folder
                self.working_directories.remove(directory)
                del self.monitored_files[name]

            row = self.file_list.row(selected_item)
            self.file_list.takeItem(row)

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
            if not self.current_monitoring is None and option == "DefinedPathCount" and self.current_monitoring.file_format.value.lower() != 'json':
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
    #TODO think about this part
    #     self.update_current_metric()
    #
    # def update_current_metric(self):
    #     text = self.show_metric.currentText()
    #     if text != "Show":
    #         self.last_selected_metric.setText(f"Last selected: {text}")
    #     else:
    #         last_selected = self.select_metrics.last_selected
    #         self.last_selected_metric.setText(f"Last selected: {last_selected if last_selected else 'None'}")

    def validate_jsonpath(self):
        pattern = r'^\$(\.\*|\.\w[\w\s]*|\[\"[^\"]+\"\]|\[\d+\]|\[\*\])+$'
        return bool(re.fullmatch(pattern, self.line_edit.text()))

    #Working with directory
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
                         "regular_metrics": selected_regular_metrics, "directory": new_directory, "name": name, "file_format": file_format}
                self.monitored_file_windows[name] = state
                self.monitored_files[name] = DataMonitor(name, new_directory, data_description, selected_regular_metrics, selected_column_metrics,
                                                         file_format,self.database_manager, self.column_button.currentText())
                self.file_list.addItem(name)

                self.working_directories.append(new_directory)

                #Setting up the widgets according to the data
                if self.current_window is None:
                    self.current_monitoring = self.monitored_files.get(name)
                    self.current_window = state
                    self.load_interface(metric_types_selected, selected_column_metrics, selected_regular_metrics, time_interval)
        except OSError:
            pass

    def load_columns_from_directory(self):
        result = []
        for filename in os.listdir(self.current_monitoring.folder):
            file_path = os.path.join(self.current_monitoring.folder, filename)
            try:
                if self.current_monitoring.file_format == FileType.CSV and filename.endswith(".csv"):
                    df = pd.read_csv(file_path, nrows=1)
                    result = result + df.columns.tolist()
                elif self.current_monitoring.file_format == FileType.PARQUET and filename.endswith(".parquet"):
                    table = pq.read_table(file_path)
                    result = result + table.schema.names
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
        return result

    def reload_current_directory(self, item):
        self.save_changes()
        print(item.text())
        self.current_monitoring = self.monitored_files.get(item.text())
        self.current_window = self.monitored_file_windows.get(item.text())

        metric_types_selected = self.current_window.get("metric_types")
        time_interval = self.current_window.get("time")
        selected_column_metrics = self.current_window.get("column_metrics")
        selected_regular_metrics = self.current_window.get("regular_metrics")

        self.load_interface(metric_types_selected, selected_column_metrics, selected_regular_metrics, time_interval)

        self.current_columns = self.load_columns_from_directory()
        self.column_button.clear()
        self.column_button.addItems(self.current_columns)

    def load_interface(self, metric_types_selected, selected_column_metrics, selected_regular_metrics, time_interval):
        self.metric_type_selector.set_selected_options(metric_types_selected)
        self.update_select_metrics()

        selected_help = selected_column_metrics + selected_regular_metrics
        self.select_metrics.set_selected_options(selected_help)


        self.time_interval_input.setValue(time_interval)

    def save_changes(self):
        self.current_window["metric_types"] = set(self.metric_type_selector.selected_options)
        self.current_window["time"] = self.time_interval_input.value()

        selected_metrics = self.select_metrics.selected_options

        selected_column = []
        selected_regular = []
        self.divide_metrics(selected_metrics, selected_column, selected_regular)
        self.current_window["column_metrics"] = selected_column
        self.current_window["regular_metrics"] = selected_regular

    def divide_metrics(self, selected, selected_column, selected_regular):
        column = self.database_manager.get_column_metrics()

        for metric in selected:
            if metric in column:
                selected_column.append(metric)
            else:
                selected_regular.append(metric)

    def plot_metric_graph(self):
        metric_name = self.show_metric.currentText()

        data = [batch_file.get_metric_value(metric_name) for batch_file in self.current_monitoring.batch_files]
        if not data:
            raise AttributeError(f"No data available for {metric_name} metric!")

        timestamps, values = zip(*data)
        self.graph_widget.plot(timestamps, values, title=f"{metric_name} over Time")

    def calculate(self):
        name = self.current_window.get("name")
        directory = self.current_window.get("directory")
        data_description = self.current_window.get("description")
        regular_metrics = []
        column_metrics = []
        file_format = self.current_window.get("file_format")
        self.divide_metrics(self.select_metrics.selected_options, column_metrics, regular_metrics)

        processed_files = self.current_monitoring.processed_files
        data_batch_files = self.current_monitoring.batch_files
        self.current_monitoring = DataMonitor(name ,directory, data_description,
                                              regular_metrics, column_metrics, file_format, self.database_manager, self.column_button.currentText())
        self.current_monitoring.processed_files = processed_files
        self.current_monitoring.batch_files = data_batch_files
        #Probably not needed
        self.monitored_files[name] = self.current_monitoring

        self.current_monitoring.start_monitoring()
        self.plot_metric_graph()













app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()