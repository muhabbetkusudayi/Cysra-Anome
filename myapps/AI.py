from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel
)
from PyQt5.QtCore import Qt
from groq import Groq


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.client = Groq(api_key="GROQ_API_KEY") # replace your groq key... to work, search groq (NOT GROK) and create an account to get the key

        self.setWindowTitle("AI Assistant")
        self.resize(700, 500)

        main_layout = QVBoxLayout()

        # Header
        self.title = QLabel("AI Assistant for Cysra Anome")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        padding:10px;
        """)
        main_layout.addWidget(self.title)

        # Chat area
        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setStyleSheet("""
        QTextEdit {
            background:#1e1e1e;
            color:white;
            border-radius:8px;
            padding:10px;
            font-size:14px;
        }
        """)
        main_layout.addWidget(self.chat)

        # Input layout
        input_layout = QHBoxLayout()

        self.input = QTextEdit()
        self.input.setPlaceholderText("Ask something...")
        self.input.setFixedHeight(70)
        self.input.setStyleSheet("""
        QTextEdit {
            border-radius:6px;
            padding:6px;
            font-size:14px;
        }
        """)
        input_layout.addWidget(self.input)

        # Buttons
        btn_layout = QVBoxLayout()

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.ask_ai)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.chat.clear)

        btn_layout.addWidget(self.send_btn)
        btn_layout.addWidget(self.clear_btn)

        input_layout.addLayout(btn_layout)

        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

    def ask_ai(self):
        user_text = self.input.toPlainText().strip()
        if not user_text:
            return

        self.chat.append(f"<b>You:</b> {user_text}")

        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Your name is Cysra Anome AI."},
                {"role": "user", "content": user_text}
            ]
        )

        answer = completion.choices[0].message.content

        self.chat.append(f"<b>AI:</b> {answer}<br>")
        self.input.clear()