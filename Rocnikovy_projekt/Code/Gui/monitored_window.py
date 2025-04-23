from PyQt5.QtWidgets import QVBoxLayout, QDialog, QHBoxLayout, QGridLayout, QLabel, QPushButton, QLineEdit, QComboBox, \
    QSpinBox, QTextEdit, QFileDialog

from Gui.multi_selected_combobox import MultiSelectComboBox
from src.database_manager import DBManager


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