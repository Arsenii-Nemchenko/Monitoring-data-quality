from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

from src.metric import *


class Color(QWidget):

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MultiSelectComboBox(QComboBox):
    def __init__(self, options, on_selection_change=None):
        super().__init__()
        self.setView(QListView())
        self.model = QStandardItemModel()
        self.setModel(self.model)

        self.options = options
        self.selected_options = set()
        self.last_selected = None
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

        self.regular_metrics =  [RecordCount(), EmptyRecordCount(), NullObjectCount(), EmptyObjectCount(),
                             DuplicateRecordCount()]

        self.column_metrics = [NullValuesCountColumn(), NullValuesCountJson(), DefinedPathCount(),
                                    UniqueValuesCountJson(), UniqueValuesCount(), AverageValue(), AverageValueJson()]



        layout = QGridLayout()

        layout1 = QVBoxLayout()
        layout1.addWidget(Color('blue'))
        layout2 = QVBoxLayout()

        layout2_1 = QHBoxLayout()

        self.metric_type_selector = MultiSelectComboBox(["Regular", "Column"], self.update_select_metrics)

        layout2_1.addWidget(QLabel("Metric Type:"))
        layout2_1.addWidget(self.metric_type_selector)

        time_interval_label = QLabel("Time Interval (seconds):")
        self.time_interval_input = QSpinBox()
        self.time_interval_input.setMinimum(1)
        self.time_interval_input.setMaximum(3600)
        self.time_interval_input.setValue(10)

        layout2_1.addWidget(time_interval_label)
        layout2_1.addWidget(self.time_interval_input)

        self.select_metrics = MultiSelectComboBox([], self.update_current_metric)
        self.select_metrics.setMinimumSize(150, 30)

        layout2_1.addWidget(QLabel("Select Metrics:"))
        layout2_1.addWidget(self.select_metrics)

        layout2_1.addWidget(Color('red'))


        layout2_2 = QVBoxLayout()
        self.last_selected_metric = QLabel("")
        layout2_2.addWidget(self.last_selected_metric)
        layout2_2.addWidget(Color('green'))

        layout2.addLayout(layout2_1)
        layout2.addLayout(layout2_2)

        layout.addLayout(layout1, 0, 0)
        layout.addLayout(layout2, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.update_select_metrics()

    def update_select_metrics(self):
        selected_types = self.metric_type_selector.selected_options
        self.select_metrics.clear()

        if "Regular" in selected_types and "Column" in selected_types:
            self.select_metrics.addItems({item.name for item in self.regular_metrics + self.column_metrics})
        elif "Regular" in selected_types:
            self.select_metrics.addItems({item.name for item in self.regular_metrics})
        elif "Column" in selected_types:
            self.select_metrics.addItems({item.name for item in self.column_metrics})

    def update_current_metric(self):
        last_selected = self.select_metrics.last_selected
        self.last_selected_metric.setText(f"The shown metric is : {last_selected if last_selected else 'None'}")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()