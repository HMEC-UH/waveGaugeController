# gui_client_with_sum.py
import sys
import requests
from itertools import accumulate
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel,
    QRadioButton, QButtonGroup,
    QTableWidget, QTableWidgetItem
)
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.data_list = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Wave Gauge GUI Client")

        layout = QVBoxLayout()

        # — Input row —
        row = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("e.g. 42")
        row.addWidget(self.input_box)
        self.input_box.returnPressed.connect(self.send_value)

        self.metric_radio = QRadioButton("Metric")
        self.imperial_radio = QRadioButton("Imperial")
        self.metric_radio.setChecked(True)
        unitGrp = QButtonGroup(self)
        unitGrp.addButton(self.metric_radio)
        unitGrp.addButton(self.imperial_radio)
        row.addWidget(self.metric_radio)
        row.addWidget(self.imperial_radio)

        unitGrp.buttonToggled.connect(self.updateLabel)

        self.metricLabel = QLabel("Metric (mm)")

        if self.metric_radio.isChecked():
            self.metricLabel.setText("Enter Value [Metric (mm)]: ")
        else:
            self.metricLabel.setText("Enter Value [Imperial (inches)]: ")

        row.insertWidget(0, self.metricLabel)
        unitGrp.buttonToggled.connect(self.updateLabel)

        self.up_radio = QRadioButton("Up")
        self.down_radio = QRadioButton("Down")
        self.up_radio.setChecked(True)
        grp = QButtonGroup(self)
        grp.addButton(self.up_radio)
        grp.addButton(self.down_radio)
        row.addWidget(self.up_radio)
        row.addWidget(self.down_radio)

        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_value)
        row.addWidget(send_btn)

        layout.addLayout(row)
        layout.addWidget(QLabel(""))  # spacer
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # — Table of entries —
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(["Direction", "Value", "Displacement"])
        layout.addWidget(self.table)

        # — Total movement display 
        self.sum_label = QLabel("Total Movement: 0")
        layout.addWidget(self.sum_label)

        # — Live plot —
        self.figure = Figure(figsize=(3,2))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Total Displacement Over Time")
        self.ax.set_xlabel("Send #")
        self.ax.set_ylabel("Total Displacement")
        layout.addWidget(self.canvas)

        self.setLayout(layout)
    
    def updateLabel(self):
        if self.metric_radio.isChecked():
            self.metricLabel.setText("Enter Value [Metric (mm)]: ")
        else:
            self.metricLabel.setText("Enter Value [Imperial (inches)]: ")
            

    def send_value(self):
        txt = self.input_box.text().strip()
        if not txt.lstrip("-").isdigit():
            self.status_label.setText("Enter a valid integer.")
            return

        val = int(txt)
        signed = val if self.up_radio.isChecked() else -val

        if self.imperial_radio.isChecked():
            signed = int(signed * 25.4)

        # record locally first
        self.add_entry(signed)

        # then send to Arduino
        url = f"http://192.168.1.18/?value={signed}"
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                self.status_label.setText(f"{r.text}")
            else:
                self.status_label.setText(f"HTTP {r.status_code}")
        except Exception as e:
            self.status_label.setText(f"Send failed: {e}")
            

        self.input_box.clear()

    def add_entry(self, v):
    # 1) Update your internal data
        self.data_list.append(v)

        # 2) Table (now that data_list has the new entry)
        row = self.table.rowCount()
        self.table.insertRow(row)
        direction = "Up" if v >= 0 else "Down"
        cum = sum(self.data_list)
        self.table.setItem(row, 0, QTableWidgetItem(direction))
        self.table.setItem(row, 1, QTableWidgetItem(str(abs(v))))
        self.table.setItem(row, 2, QTableWidgetItem(str(cum)))
        self.table.scrollToBottom()

        # 3) Plot the cumulative series
        self.ax.clear()
        xs = list(range(1, len(self.data_list) + 1))
        ys = list(accumulate(self.data_list))      # [v1, v1+v2, v1+v2+v3, …]
        self.ax.plot(xs, ys, marker="o")
        self.ax.set_title("Total Displacement Over Time")
        self.ax.set_xlabel("Send #")
        self.ax.set_ylabel("Total Displacement")
        self.canvas.draw()

        # 4) Update the summary label
        self.sum_label.setText(f"Total Movement: {cum}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
