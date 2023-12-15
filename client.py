import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QHBoxLayout
import csv

class DataCollectorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Data Collector')
        self.setGeometry(100, 100, 400, 300)

        self.create_widgets()

    def create_widgets(self):
        layout = QVBoxLayout()

        labels = ["Rooms", "Floor", "Location"]
        self.entry_widgets = {}

        for label in labels:
            entry_label = QLabel(label)
            entry_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
            entry_widget = QLineEdit()
            layout.addWidget(entry_label)
            layout.addWidget(entry_widget)
            self.entry_widgets[label] = entry_widget

        # Add min-max labels and entry widgets for Price, and Min-Max Size
        min_label = QLabel("Min Price:")
        min_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
        max_label = QLabel("Max Price:")
        max_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
        min_size_label = QLabel("Min Size:")
        min_size_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
        max_size_label = QLabel("Max Size:")
        max_size_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
        min_entry = QLineEdit()
        max_entry = QLineEdit()
        min_size_entry = QLineEdit()
        max_size_entry = QLineEdit()

        min_max_layout = QHBoxLayout()
        min_max_layout.addWidget(min_label)
        min_max_layout.addWidget(min_entry)
        min_max_layout.addWidget(max_label)
        min_max_layout.addWidget(max_entry)

        size_layout = QHBoxLayout()
        size_layout.addWidget(min_size_label)
        size_layout.addWidget(min_size_entry)
        size_layout.addWidget(max_size_label)
        size_layout.addWidget(max_size_entry)

        layout.addLayout(min_max_layout)
        layout.addLayout(size_layout)

        #filter_label = QLabel("Filter by:")
        #filter_label.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
        #self.filter_combobox = QComboBox()
        #self.filter_combobox.addItems(["", "Transaction Type", "Location"])  # Add more filter options if needed
        #layout.addWidget(filter_label)
        #layout.addWidget(self.filter_combobox)


        read_button = QPushButton("Read from CSV")
        read_button.setStyleSheet("font-size: 16pt; font-family: Cikkiri;")
        read_button.clicked.connect(self.read_from_csv)

        layout.addWidget(read_button)

        self.setLayout(layout)

    def read_from_csv(self):
        # Implement your logic to read and process data from the CSV file
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DataCollectorApp()
    ex.show()
    sys.exit(app.exec_())
