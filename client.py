import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout
import pandas as pd

def filltering_data(collected_data):
    for key, value in list(collected_data.items()):
        if value == "":
            del collected_data[key]
    return collected_data


def collect_matching_annoucments(collected_data):
    if "Location" in  list(collected_data.keys):
        data = pd.read_csv("nieruchomosci.csv")



class DataCollectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Data Collector')
        self.setGeometry(100, 100, 400, 300)

        # Declare the entry_widgets and other entry variables as instance attributes
        self.entry_widgets = {}
        self.min_entry = QLineEdit()
        self.max_entry = QLineEdit()
        self.min_size_entry = QLineEdit()
        self.max_size_entry = QLineEdit()

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        labels = ["Rooms", "Floor", "Location"]
        for label in labels:
            entry_label = QLabel(label)
            entry_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri; color: #333;")
            entry_widget = QLineEdit()
            entry_widget.setStyleSheet("font-size: 14pt; background-color: #f0f0f0; color: #333;")
            layout.addWidget(entry_label)
            layout.addWidget(entry_widget)
            self.entry_widgets[label] = entry_widget

        min_label = QLabel("Min Price:")
        min_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri; color: #333;")
        max_label = QLabel("Max Price:")
        max_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri; color: #333;")
        min_size_label = QLabel("Min Size:")
        min_size_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri; color: #333;")
        max_size_label = QLabel("Max Size:")
        max_size_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri; color: #333;")

        min_max_layout = QHBoxLayout()
        min_max_layout.addWidget(min_label)
        min_max_layout.addWidget(self.min_entry)
        min_max_layout.addWidget(max_label)
        min_max_layout.addWidget(self.max_entry)

        size_layout = QHBoxLayout()
        size_layout.addWidget(min_size_label)
        size_layout.addWidget(self.min_size_entry)
        size_layout.addWidget(max_size_label)
        size_layout.addWidget(self.max_size_entry)

        layout.addLayout(min_max_layout)
        layout.addLayout(size_layout)

        read_button = QPushButton("Read from CSV")
        read_button.setStyleSheet("font-size: 16pt; font-family: Cikkiri; background-color: #4CAF50; color: white;")
        read_button.clicked.connect(self.collect_data)

        layout.addWidget(read_button)

        self.setLayout(layout)

    def collect_data(self):
        collected_data = {}
        for label, widget in self.entry_widgets.items():
            collected_data[label] = widget.text()

        collected_data["Min Price"] = self.min_entry.text()
        collected_data["Max Price"] = self.max_entry.text()
        collected_data["Min Size"] = self.min_size_entry.text()
        collected_data["Max Size"] = self.max_size_entry.text()

        print(filltering_data(collected_data))





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataCollectorApp()
    ex.show()
    sys.exit(app.exec_())
