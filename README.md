# 🌐 Sysra Browser Lite 5.0

**Sysra Browser Lite** is a lightweight, modular desktop browser built with **Python + PyQt5**.  
It combines a clean browsing experience with built-in tools and a powerful plugin system.

Fast. Minimal. Hackable.


<img width="1200" height="799" alt="image" src="https://github.com/user-attachments/assets/aa60a39d-d88e-4f2d-8db0-8f0d9579e620" />


---

## ✨ Features

- 🧭 **Multi-tab Web Browser** (PyQt5 WebEngine)
- 🧩 **Plugin System** (drop-in Python apps)
- 🌐 **Built-in Translator** (Google Translate)
- 📝 **Notes Manager** (local, offline)
- 🧮 **Calculator**
- ⬇️ **Download Manager**
- 🚫 **Blocked Websites System**
- 🪟 **Split Screen Layout** (Browser + Tools)
- ⚡ **Low resource usage**

---

## 🧩 Plugin System

Sysra Browser Lite supports **custom Python plugins**.

Each plugin:
- Lives inside the `myapps/` folder
- Is written in pure Python
- Must expose an `AppWidget(QWidget)` class

### Example Plugin
```python
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Hello Sysra!"))
        self.setLayout(layout)
Plugins appear automatically inside the My Apps panel.

🔍 AnotherBrowser Plugin
AnotherBrowser is a mini browser plugin with a configurable search engine system.

Features
Embedded browser (QWebEngineView)

Custom search engines

Engine selection via dropdown

Split-screen integration

Search Engine Configuration
Edit or create:


myapps/search_engines.txt
Example:


google=https://www.google.com/search?q=
duckduckgo=https://duckduckgo.com/?q=
bing=https://www.bing.com/search?q=
yandex=https://yandex.com/search/?text=
brave=https://search.brave.com/search?q=
📦 Requirements
PyQt5
PyQtWebEngine
deep-translator
Install dependencies:


pip install -r requirements.txt

🚀 Run
python sysrabrowser.py

Or with a username:


python sysrabrowser.py SysraUser

🛡️ Privacy & Security
No tracking

No telemetry

No cloud sync

All notes stored locally

Camera & microphone permissions are controlled by the WebEngine



🧠 Philosophy
Sysra Browser Lite is built for:

Students

Developers

Power users

People who want control

No bloat.
No ads.
No nonsense.

🧑‍💻 Developer
muhabbetkusudev

GitHub: https://github.com/muhabbetkusudayi
Featured under Young Technology category

📄 License
Open Source – use it, modify it, break it, improve it.

Just don’t sell the soul.
