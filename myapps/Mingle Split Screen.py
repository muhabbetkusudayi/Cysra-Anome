

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("URLScreen")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.example.com"))

        layout.addWidget(self.browser)
        self.setLayout(layout)