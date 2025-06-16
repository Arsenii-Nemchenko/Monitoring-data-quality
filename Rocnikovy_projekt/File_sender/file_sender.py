import os
import time
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget,
                             QLabel, QLineEdit, QPushButton, QFileDialog,
                             QSpinBox, QTextEdit, QHBoxLayout, QMessageBox)
from PyQt5.QtCore import QTimer, Qt


class FileSenderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Sender with Timestamp")
        self.setGeometry(100, 100, 600, 450)

        self.source_file = ""
        self.destination_dir = ""
        self.is_running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_file_with_timestamp)

        main_widget = QWidget()
        layout = QVBoxLayout()

        self.file_label = QLabel("Source file: Not selected")
        self.file_btn = QPushButton("Select File")
        self.file_btn.clicked.connect(self.select_source_file)

        self.dir_label = QLabel("Destination folder: Not selected")
        self.dir_btn = QPushButton("Select Folder")
        self.dir_btn.clicked.connect(self.select_destination_dir)

        interval_layout = QHBoxLayout()

        self.days_label = QLabel("Days:")
        self.days_input = QSpinBox()
        self.days_input.setRange(0, 30)
        self.days_input.setValue(0)

        self.hours_label = QLabel("Hours:")
        self.hours_input = QSpinBox()
        self.hours_input.setRange(0, 23)
        self.hours_input.setValue(0)

        self.minutes_label = QLabel("Minutes:")
        self.minutes_input = QSpinBox()
        self.minutes_input.setRange(0, 59)
        self.minutes_input.setValue(0)

        self.seconds_label = QLabel("Seconds:")
        self.seconds_input = QSpinBox()
        self.seconds_input.setRange(1, 59)
        self.seconds_input.setValue(30)

        interval_layout.addWidget(self.days_label)
        interval_layout.addWidget(self.days_input)
        interval_layout.addWidget(self.hours_label)
        interval_layout.addWidget(self.hours_input)
        interval_layout.addWidget(self.minutes_label)
        interval_layout.addWidget(self.minutes_input)
        interval_layout.addWidget(self.seconds_label)
        interval_layout.addWidget(self.seconds_input)

        self.prefix_label = QLabel("Filename prefix (e.g., catering_):")
        self.prefix_input = QLineEdit("file_")

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_sending)
        self.start_btn.setEnabled(False)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_sending)
        self.stop_btn.setEnabled(False)

        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_btn)
        layout.addWidget(self.dir_label)
        layout.addWidget(self.dir_btn)

        layout.addWidget(QLabel("Sending interval:"))
        layout.addLayout(interval_layout)

        layout.addWidget(self.prefix_label)
        layout.addWidget(self.prefix_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(QLabel("Event log:"))
        layout.addWidget(self.log_area)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def is_valid_file_type(self, filename):
        return filename.lower().endswith(('.json', '.csv', '.parquet'))

    def get_14_digit_timestamp(self):
        now = time.localtime()
        return time.strftime("%Y%m%d%H%M%S", now)

    def get_file_extension(self):
        return os.path.splitext(self.source_file)[1].lower()

    def get_interval_seconds(self):
        days = self.days_input.value()
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        seconds = self.seconds_input.value()
        return days * 86400 + hours * 3600 + minutes * 60 + seconds

    def select_source_file(self):
        try:
            file, _ = QFileDialog.getOpenFileName(self, "Select source file")
            if file:
                if not os.path.exists(file):
                    raise FileNotFoundError(f"File not found: {file}")
                if not os.access(file, os.R_OK):
                    raise PermissionError(f"No read access: {file}")
                if not self.is_valid_file_type(file):
                    raise ValueError("Only JSON, CSV, and Parquet files are supported")

                self.source_file = file
                self.file_label.setText(f"Source file: {os.path.basename(file)}")
                self.check_ready()
                self.log(f"Selected file: {file}")
        except Exception as e:
            self.show_error(f"File selection error: {str(e)}")

    def select_destination_dir(self):
        try:
            dir_path = QFileDialog.getExistingDirectory(self, "Select destination folder")
            if dir_path:
                if not os.path.exists(dir_path):
                    raise FileNotFoundError(f"Folder not found: {dir_path}")
                if not os.access(dir_path, os.W_OK):
                     raise PermissionError(f"No write access: {dir_path}")

                self.destination_dir = dir_path
                self.dir_label.setText(f"Destination folder: {dir_path}")
                self.check_ready()
                self.log(f"Selected folder: {dir_path}")
        except Exception as e:
            self.show_error(f"Folder selection error: {str(e)}")

    def check_ready(self):
        try:
            if self.source_file and self.destination_dir:
                if not os.path.exists(self.source_file):
                    raise FileNotFoundError("Source file missing")
                if not os.path.exists(self.destination_dir):
                    raise FileNotFoundError("Destination folder missing")
                if not self.is_valid_file_type(self.source_file):
                    raise ValueError("Invalid file type")
                self.start_btn.setEnabled(True)
            else:
                self.start_btn.setEnabled(False)
        except Exception as e:
            self.show_error(str(e))
            self.start_btn.setEnabled(False)

    def toggle_sending(self):
        try:
            if self.is_running:
                self.stop_sending()
            else:
                self.start_sending()
        except Exception as e:
            self.show_error(f"Toggle error: {str(e)}")

    def start_sending(self):
        try:
            if not os.path.exists(self.source_file):
                raise FileNotFoundError("Source file missing")
            if not os.path.exists(self.destination_dir):
                raise FileNotFoundError("Destination folder missing")
            if not os.access(self.destination_dir, os.W_OK):
                raise PermissionError("No write permission")
            if not self.is_valid_file_type(self.source_file):
                raise ValueError("Invalid file type")

            interval_seconds = self.get_interval_seconds()
            self.is_running = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.timer.start(interval_seconds * 1000)

            days = interval_seconds // 86400
            hours = (interval_seconds % 86400) // 3600
            minutes = (interval_seconds % 3600) // 60
            seconds = interval_seconds % 60

            interval_str = f"{days}d {hours}h {minutes}m {seconds}s"
            self.log(f"Started sending with interval: {interval_str}")
            self.send_file_with_timestamp()

        except Exception as e:
            self.show_error(f"Start error: {str(e)}")
            self.stop_sending()

    def stop_sending(self):
        try:
            self.is_running = False
            self.timer.stop()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.log("Sending stopped")
        except Exception as e:
            self.show_error(f"Stop error: {str(e)}")

    def send_file_with_timestamp(self):
        if not self.is_running:
            return

        try:
            if not os.path.exists(self.source_file):
                raise FileNotFoundError("Source file missing")
            if not os.path.exists(self.destination_dir):
                raise FileNotFoundError("Destination folder missing")
            if not os.access(self.destination_dir, os.W_OK):
                raise PermissionError("No write permission")
            if not self.is_valid_file_type(self.source_file):
                raise ValueError("Invalid file type")

            timestamp = self.get_14_digit_timestamp()
            prefix = self.prefix_input.text().strip() or "file_"
            file_ext = self.get_file_extension()
            filename = f"{prefix}{timestamp}{file_ext}"
            dest_path = os.path.join(self.destination_dir, filename)

            if os.path.exists(dest_path):
                raise FileExistsError(f"File exists: {filename}")

            shutil.copy2(self.source_file, dest_path)
            self.log(f"Sent: {filename}")

        except FileNotFoundError as e:
            self.show_error(str(e))
            self.stop_sending()
        except PermissionError as e:
            self.show_error(str(e))
            self.stop_sending()
        except FileExistsError as e:
            self.log(f"Warning: {str(e)} - retrying")
            time.sleep(1)
            self.send_file_with_timestamp()
        except shutil.SameFileError:
            self.log("Warning: Attempted self-copy")
        except Exception as e:
            self.show_error(f"Send error: {str(e)}")
            self.stop_sending()

    def log(self, message):
        try:
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            self.log_area.append(f"[{timestamp}] {message}")
        except Exception:
            pass

    def show_error(self, message):
        try:
            QMessageBox.critical(self, "Error", message)
            self.log(f"ERROR: {message}")
        except Exception:
            pass

    def closeEvent(self, event):
        try:
            if self.is_running:
                self.stop_sending()
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    try:
        app = QApplication([])
        window = FileSenderApp()
        window.show()
        app.exec_()
    except Exception as e:
        QMessageBox.critical(None, "Critical Error", f"Application crashed:\n{str(e)}")