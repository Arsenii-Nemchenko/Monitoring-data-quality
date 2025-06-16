from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, \
    QSpinBox, QTextEdit, QFileDialog, QToolTip

from .multi_selected_combobox import MultiSelectComboBox
from ..src.database_manager import DBManager


class MonitoredFileWindow(QDialog):
    def __init__(self, db_manager: DBManager):
        super().__init__()
        self.db_manager = db_manager
        self.new_directory = None
        self.selected_column = []
        self.selected_regular = []
        self.column = db_manager.get_column_metrics()
        self.regular = db_manager.get_regular_metrics()

        self.setWindowTitle("New Monitored File Setup")
        self.resize(800, 400)

        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        left_layout = QGridLayout()
        right_layout = QGridLayout()

        self.name_label = QLabel("Name:")
        self.name_text = QLineEdit()
        self.name_text.setPlaceholderText("Enter name*")

        self.folder_button = QPushButton("Set Folder*")

        self.type_label = QLabel("File Format:")
        self.file_type_selector = QComboBox()
        file_types = db_manager.get_file_types()
        for file_type in file_types:
            self.file_type_selector.addItem(file_type)

        self.folder_button.clicked.connect(self.get_working_directory)

        left_layout.addWidget(self.name_label, 0, 0)
        left_layout.addWidget(self.name_text, 0, 1)
        left_layout.addWidget(self.folder_button, 1, 0, 1, 2)
        left_layout.addWidget(self.type_label, 2, 0)
        left_layout.addWidget(self.file_type_selector, 2, 1)

        self.metric_type_label = QLabel("Metric Type:")
        self.metric_type_selector = MultiSelectComboBox(["Regular", "Column"])
        self.metric_type_selector.on_selection_change = self.update_select_metrics

        self.time_interval_label = QLabel("Time Interval (seconds):")
        self.time_interval_input_right = QSpinBox()
        self.time_interval_input_right.setRange(1, 3600)
        self.time_interval_input_right.setValue(10)

        self.select_metrics_label = QLabel("Select Metrics:")
        self.select_metrics = MultiSelectComboBox([])
        self.select_metrics.on_selection_change = self._handle_selected_metrics

        right_layout.addWidget(self.metric_type_label, 0, 0)
        right_layout.addWidget(self.metric_type_selector, 0, 1)
        right_layout.addWidget(self.time_interval_label, 1, 0)
        right_layout.addWidget(self.time_interval_input_right, 1, 1)
        right_layout.addWidget(self.select_metrics_label, 2, 0)
        right_layout.addWidget(self.select_metrics, 2, 1)

        top_layout.addLayout(left_layout, 40)
        top_layout.addLayout(right_layout, 60)

        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Write a short description of the data here...")
        self.add_button = QPushButton("Add monitoring")
        self.add_button.clicked.connect(self._handle_add_click)

        description_layout = QVBoxLayout()
        description_layout.addWidget(self.description_text)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button, alignment=Qt.AlignLeft)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(description_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_working_directory(self):
        self.new_directory = QFileDialog.getExistingDirectory()

    def _handle_add_click(self):
        if self.new_directory:
            if self.name_text.text().strip(" ") != "":
                if not len(self.select_metrics.selected_options) == 0:
                    self.accept()
                else:
                    self.select_metrics.setStyleSheet("border: 1px solid red;")
                    QToolTip.showText(self.select_metrics.mapToGlobal(QPoint(0, self.select_metrics.height())),
                                      "You have not chosen any metric")
            else:
                self.name_text.setStyleSheet("border: 1px solid red;")
                QToolTip.showText(self.name_text.mapToGlobal(QPoint(0, self.name_text.height())),
                                  "This field cannot be empty")
        else:
            self.folder_button.setStyleSheet("border: 1px solid red;")
            QToolTip.showText(self.folder_button.mapToGlobal(QPoint(0, self.folder_button.height())),
                              "You have not chosen a directory")

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