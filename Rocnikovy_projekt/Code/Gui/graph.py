from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import timedelta


class GraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(5, 4), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot(self, timestamps, values, title, xlabel="Time", ylabel="Value", column=None):
        try:
            self.ax.clear()

            if not timestamps or not values:
                self.canvas.draw()
                return

            self.ax.plot(timestamps, values, marker='o')

            # Modify title to include column if provided
            full_title = f"{title} for {column}" if column else title
            self.ax.set_title(full_title)

            self.ax.set_xlabel(xlabel)
            self.ax.set_ylabel(ylabel)
            self.ax.grid(True)

            min_time = min(timestamps)
            max_time = max(timestamps)

            if min_time == max_time:
                max_time += timedelta(seconds=1)

            self.ax.set_xlim(min_time, max_time)

            total_seconds = (max_time - min_time).total_seconds()

            if total_seconds < 60:
                formatter = mdates.DateFormatter('%H:%M:%S.%f')
                self.ax.xaxis.set_major_formatter(formatter)

            elif total_seconds < 3600:
                formatter = mdates.DateFormatter('%H:%M:%S')
                self.ax.xaxis.set_major_formatter(formatter)

            elif total_seconds < 86400:
                formatter = mdates.DateFormatter('%H:%M')
                self.ax.xaxis.set_major_formatter(formatter)

            elif total_seconds < 2678400:
                formatter = mdates.DateFormatter('%d.%m')
                self.ax.xaxis.set_major_formatter(formatter)

            elif total_seconds < 31536000:
                formatter = mdates.DateFormatter('%b %Y')
                self.ax.xaxis.set_major_formatter(formatter)

            else:
                formatter = mdates.DateFormatter('%Y')
                self.ax.xaxis.set_major_formatter(formatter)

            self.ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            self.figure.autofmt_xdate()
            self.canvas.draw()
        except Exception as e:
            print(f"Graph exception: {e}")

    def clear_graph(self):
        self.ax.clear()
        self.ax.set_title("")
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.grid(False)
        self.canvas.draw()