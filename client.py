import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QHBoxLayout, QComboBox
import csv

class DataCollectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.labels = ["Rooms", "Area", "Floor", "Location", "Link"]
        self.entry_widgets = {}

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Data Collector')
        self.setGeometry(100, 100, 400, 200)

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        for label in self.labels:
            entry_label = QLabel(label)
            entry_widget = QLineEdit()
            entry_layout = QHBoxLayout()
            entry_layout.addWidget(entry_label)
            entry_layout.addWidget(entry_widget)
            layout.addLayout(entry_layout)
            self.entry_widgets[label] = entry_widget

            # Add min-max labels and entry widgets for Area
            if label == "Area":
                min_label = QLabel("Min Area:")
                max_label = QLabel("Max Area:")
                min_entry = QLineEdit()
                max_entry = QLineEdit()

                min_max_layout = QHBoxLayout()
                min_max_layout.addWidget(min_label)
                min_max_layout.addWidget(min_entry)
                min_max_layout.addWidget(max_label)
                min_max_layout.addWidget(max_entry)

                layout.addLayout(min_max_layout)

        read_button = QPushButton("Read from CSV")
        read_button.clicked.connect(self.read_from_csv)

        layout.addWidget(read_button)

        self.setLayout(layout)

    def read_from_csv(self):
        with open("data.csv", mode="r", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                # Access the values based on the labels
                rooms = row[self.labels.index("Rooms")]
                area = row[self.labels.index("Area")]

                # You can use these values as needed
                print(f"Rooms: {rooms}, Area: {area}")

    def clear_entries(self):
        for label in self.entry_widgets:
            self.entry_widgets[label].clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataCollectorApp()
    window.show()
    sys.exit(app.exec_())
