from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError
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


        #Pivot layout
        layout = QGridLayout()

        layout1 = QVBoxLayout()

        layout_header = QHBoxLayout()
        layout_header.setSpacing(5)
        layout_header.setAlignment(Qt.AlignmentFlag.AlignTop)
        header_name = QLabel("Add monitored file")
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
        layout_header.addWidget(header_name)
        layout_header.addWidget(plus_button)

        layout_buttons = QHBoxLayout()
        layout_buttons.setAlignment(Qt.AlignmentFlag.AlignTop)
        add_file_button = QPushButton("Add file")
        remove_file_button = QPushButton("Remove")
        layout_buttons.addWidget(add_file_button)
        layout_buttons.addWidget(remove_file_button)


        layout1.addLayout(layout_header)
        layout1.addLayout(layout_buttons)






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

        #To delete
        layout2_1.addWidget(Color('red'))

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
        layout2_2.addWidget(Color('green'))

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

        layout.addLayout(layout1, 0, 0)
        layout.addLayout(layout2, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.update_select_metrics()

    def update_select_metrics(self):
        selected_types = self.metric_type_selector.selected_options

        new_options = []
        if "Regular" in selected_types and "Column" in selected_types:
            options ={item.name for item in self.regular_metrics + self.column_metrics}
            new_options = options
            self.select_metrics.addItems(options)
        elif "Regular" in selected_types:
            options ={item.name for item in self.regular_metrics}
            new_options = options
            self.select_metrics.addItems(options)
        elif "Column" in selected_types:
            options ={item.name for item in self.column_metrics}
            new_options = options
            self.select_metrics.addItems(options)

        self.select_metrics.set_options(new_options)

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

    def validate_jsonpath(self):
        jsonpath = self.line_edit.text()
        try:
            parse(jsonpath)
            return True
        except JsonPathParserError:
            return False


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()