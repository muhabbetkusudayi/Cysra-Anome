
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.engines = {}
        self.load_engines()

        main_layout = QVBoxLayout()
        top_bar = QHBoxLayout()

        self.engine_box = QComboBox()
        for name in self.engines:
            self.engine_box.addItem(name)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search something...")
        self.search_bar.returnPressed.connect(self.search)

        self.search_btn = QPushButton("Go")
        self.search_btn.clicked.connect(self.search)

        top_bar.addWidget(self.engine_box)
        top_bar.addWidget(self.search_bar)
        top_bar.addWidget(self.search_btn)

        self.browser = QWebEngineView()

        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.browser)
        self.setLayout(main_layout)

        # default engine = google
        if "google" in self.engines:
            self.engine_box.setCurrentText("google")
            self.browser.setUrl(QUrl("https://www.google.com"))

    def load_engines(self):
        path = os.path.join(os.path.dirname(__file__), "search_engines.txt")
        if not os.path.exists(path):
            QMessageBox.warning(self, "Error", "search_engines.txt not found")
            return

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    name, url = line.strip().split("=", 1)
                    self.engines[name] = url

    def search(self):
        query = self.search_bar.text().strip()
        if not query:
            return

        engine = self.engine_box.currentText()
        base_url = self.engines.get(engine)

        if not base_url:
            return

        full_url = base_url + query.replace(" ", "+")
        self.browser.setUrl(QUrl(full_url))
