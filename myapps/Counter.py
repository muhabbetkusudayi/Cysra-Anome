
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0
        layout = QVBoxLayout()
        self.label = QLabel(f"Count: {self.count}")
        layout.addWidget(self.label)
        self.btn = QPushButton("Increase")
        self.btn.clicked.connect(self.increment)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def increment(self):
        self.count += 1
        self.label.setText(f"Count: {self.count}")

