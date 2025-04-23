from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QComboBox, QListView


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

    def set_options(self, new_options, selected=None):
        self.model.clear()
        selected = set(selected) if selected else set()
        self.selected_options.clear()
        self.options = new_options
        self.last_selected = None

        for option in new_options:
            item = QStandardItem(option)
            item.setCheckable(True)
            if option in selected:
                item.setCheckState(Qt.Checked)
                self.selected_options.add(option)
            else:
                item.setCheckState(Qt.Unchecked)
            self.model.appendRow(item)

        self.update_display()

    def set_selected_options(self, selected):
        selected = set(selected)
        self.selected_options.clear()
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if item.text() in selected:
                item.setCheckState(Qt.CheckState.Checked)
                self.selected_options.add(item.text())
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
        self.update_display()