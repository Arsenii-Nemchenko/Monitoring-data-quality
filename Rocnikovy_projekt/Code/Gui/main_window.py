
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError
import sys

from src.database_manager import DBManager
from src.data_monitor import DataMonitor
from src.metric import *

class MonitoredFileWindow(QDialog):
    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db_manager = db_manager
        self.new_directory = None
        self.selected_column = []
        self.selected_regular = []
        self.column = db_manager.get_column_metrics()
        self.regular = db_manager.get_regular_metrics()
        self.setWindowTitle("New monitored file setup")
        self.resize(700, 300)

        main_layout = QVBoxLayout()
        base_layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_layout = QGridLayout()

        #Left layout
        self.name_label = QLabel("Name:")
        self.type_label = QLabel("File format:")

        self.name_text = QLineEdit()
        self.folder_button = QPushButton("Set folder")
        self.file_type_selector = QComboBox()
        self.add_button = QPushButton("Add")

        file_types = db_manager.get_file_types()
        for file_type in file_types:
            self.file_type_selector.addItem(file_type)

        self.folder_button.clicked.connect(self.get_working_directory)
        self.add_button.clicked.connect(self._handle_add_click)

        self.name_text.setPlaceholderText("Enter name")

        left_layout.addWidget(self.name_label, 0, 0)
        left_layout.addWidget(self.folder_button, 1, 0)
        left_layout.addWidget(self.type_label, 2, 0)
        left_layout.addWidget(self.add_button, 3, 0)

        left_layout.addWidget(self.name_text, 0, 1)
        left_layout.addWidget(self.file_type_selector, 2, 1)

        #Right layout
        self.metric_type_label = QLabel("Metric type:")
        self.time_interval_label = QLabel("Time interval (seconds):")
        self.select_metrics_label = QLabel("Select Metrics: ")

        # Metric type
        self.metric_type_selector = MultiSelectComboBox(["Regular", "Column"])
        right_layout.addWidget(self.metric_type_label, 0, 0)
        right_layout.addWidget(self.metric_type_selector, 0, 1)

        # Time interval
        self.time_interval_input_right = QSpinBox()
        self.time_interval_input_right.setMinimum(1)
        self.time_interval_input_right.setMaximum(3600)
        self.time_interval_input_right.setValue(10)
        right_layout.addWidget(self.time_interval_label, 1, 0)
        right_layout.addWidget(self.time_interval_input_right, 1, 1)

        # Select metrics
        self.select_metrics = MultiSelectComboBox([])
        self.select_metrics.on_selection_change = self._handle_selected_metrics
        right_layout.addWidget(self.select_metrics_label, 2, 0)
        right_layout.addWidget(self.select_metrics, 2, 1)

        #Data description
        layout = QHBoxLayout()
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Write a short description of the data here...")
        layout.addWidget(self.description_text)

        self.metric_type_selector.on_selection_change = self.update_select_metrics

        base_layout.addLayout(left_layout, 40)
        base_layout.addLayout(right_layout, 60)

        main_layout.addLayout(base_layout, 60)
        main_layout.addLayout(layout, 40)
        self.setLayout(main_layout)

    def get_working_directory(self):
        self.new_directory = QFileDialog.getExistingDirectory()

    def _handle_add_click(self):
        self.accept()

    def _handle_selected_metrics(self):
        selected_metrics =self.select_metrics.selected_options

        self.selected_column = []
        self.selected_regular = []


        for metric in selected_metrics:
            if metric in self.column:
                self.selected_column.append(metric)
            elif metric in self.regular:
                self.selected_regular.append(metric)


    def update_select_metrics(self):
        selected_types = self.metric_type_selector.selected_options

        options = []
        if "Regular" in selected_types and "Column" in selected_types:
            metrics = self.db_manager.get_regular_metrics() + self.db_manager.get_column_metrics()
            options = {m for m in metrics}
        elif "Regular" in selected_types:
            options = {m for m in self.db_manager.get_regular_metrics()}
        elif "Column" in selected_types:
            options = {m for m in self.db_manager.get_column_metrics()}

        final_options = []
        for option in options:
            if option == "DefinedPathCount" and self.file_type_selector.currentText().lower() != 'json':
                continue
            final_options.append(option)
        self.select_metrics.set_options(final_options)

class MultiSelectComboBox(QComboBox):
    def __init__(self, options, on_selection_change=None):
        super().__init__()
        self.setView(QListView())
        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.options = options
        self.selected_options = set()
        self.last_selected = ""
        self.on_selection_change = on_selection_change

        for option in self.options:
            item = QStandardItem(option)
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.model.appendRow(item)

        self.activated.connect(self.handle_selection)
        self.update_display()

    def handle_selection(self, index):
        item = self.model.item(index)
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
            self.selected_options.discard(item.text())
        else:
            item.setCheckState(Qt.CheckState.Checked)
            self.selected_options.add(item.text())
            self.last_selected = item.text()

        self.update_display()

        if self.on_selection_change:
            self.on_selection_change()

    def update_display(self):
        self.setCurrentText(", ".join(self.selected_options) if self.selected_options else "Select Options")

    def set_options(self, new_options):
        self.model.clear()
        self.selected_options.clear()
        self.options = new_options
        self.last_selected = None

        for option in new_options:
            item = QStandardItem(option)
            item.setCheckable(True)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.model.appendRow(item)

        self.update_display()



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoring data quality")
        self.resize(1500, 500)

        self.regular_metrics =  [RecordCount(), EmptyRecordCount(), NullObjectCount(), EmptyObjectCount(),
                             DuplicateRecordCount()]

        self.column_metrics = [NullValuesCountColumn(), NullValuesCountJson(), DefinedPathCount(),
                                    UniqueValuesCountJson(), UniqueValuesCount(), AverageValue(), AverageValueJson()]

        self.database_manager = DBManager(self.regular_metrics + self.column_metrics)
        self.working_directories = []
        self.monitored_file_window = MonitoredFileWindow(self.database_manager)
        self.monitored_files = {}
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

        self.last_selected_metric = QLabel("Last selected: ")

        layout2_2 = QVBoxLayout()
        layout2_2.setContentsMargins(0, 0, 0, 0)
        layout2_2.setSpacing(10)

        self.show_metric = QComboBox()
        line_edit_metric = QLineEdit()
        line_edit_metric.setPlaceholderText("Show")
        self.show_metric.setLineEdit(line_edit_metric)

        self.show_metric.currentIndexChanged.connect(self.update_current_metric)

        layout2_2.addWidget(self.last_selected_metric)

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

        new_options = []
        if "Regular" in selected_types and "Column" in selected_types:
            options ={item for item in self.database_manager.get_regular_metrics() + self.database_manager.get_column_metrics()}
            new_options = options
            self.select_metrics.addItems(options)
        elif "Regular" in selected_types:
            options ={item for item in self.database_manager.get_regular_metrics()}
            new_options = options
            self.select_metrics.addItems(options)
        elif "Column" in selected_types:
            options ={item for item in self.database_manager.get_column_metrics()}
            new_options = options
            self.select_metrics.addItems(options)

        self.select_metrics.set_options(list(new_options))

    def update_shown_metric(self):
        selected_metrics = self.select_metrics.selected_options
        self.show_metric.clear()

        if selected_metrics:
            self.show_metric.addItems(selected_metrics)
        else:
            self.show_metric.addItem("Show")

        self.update_current_metric()

    def update_current_metric(self):
        text = self.show_metric.currentText()
        if text != "Show":
            self.last_selected_metric.setText(f"Last selected: {text}")
        else:
            last_selected = self.select_metrics.last_selected
            self.last_selected_metric.setText(f"Last selected: {last_selected if last_selected else 'None'}")
    #TODO
    def validate_jsonpath(self):
        jsonpath = self.line_edit.text()
        try:
            parse(jsonpath)
            return True
        except JsonPathParserError:
            return False

    #Working with directory
    def _get_working_directory(self):
        try:
            self.monitored_file_window = MonitoredFileWindow(self.database_manager)
            result = self.monitored_file_window.exec_()

            if result == QDialog.Accepted:
                data_description = self.monitored_file_window.description_text.toPlainText()
                metrics_selected = self.monitored_file_window.metric_type_selector.selected_options
                metric_types_selected = self.monitored_file_window.metric_type_selector.selected_options
                time_interval = self.monitored_file_window.time_interval_input_right.value()
                selected_column_metrics = self.monitored_file_window.selected_column
                selected_regular_metrics = self.monitored_file_window.selected_regular
                new_directory = self.monitored_file_window.new_directory
                name = self.monitored_file_window.name_text.text()
                file_format = self.monitored_file_window.file_type_selector.currentText().lower()

                self.monitored_files[name] = DataMonitor(name, new_directory, data_description, selected_regular_metrics, selected_column_metrics, file_format,self.database_manager)
                self.file_list.addItem(name)

                self.working_directories.append(new_directory)

                #Setting up the widgets according to the data
                self.metric_type_selector.selected_options = set(metric_types_selected)
                self.metric_type_selector.update_display()
                self.update_select_metrics()

                for i in range(0, len(self.metric_type_selector.options)):
                    if self.metric_type_selector.options[i] in metric_types_selected:
                        self.metric_type_selector.handle_selection(i)

                selected_help = selected_column_metrics + selected_regular_metrics
                self.select_metrics.selected_options = set(selected_help)
                self.select_metrics.update_display()
                for i in range(0, len(self.select_metrics.options)):
                    if self.select_metrics.options[i] in selected_help:
                        self.select_metrics.handle_selection(i)

                self.time_interval_input.setValue(time_interval)
        except OSError:
            pass








app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()