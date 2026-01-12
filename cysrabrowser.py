import sys
import os
import importlib.util
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel,
    QComboBox, QSplitter, QMessageBox, QFileDialog, QListWidget
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt
from deep_translator import GoogleTranslator

MODERN_STYLE = """
    QMainWindow { background-color: #121212; }
    QTabWidget::pane { border: 1px solid #2d2d2d; background: #1e1e1e; }
    QTabBar::tab {
        background: #1e1e1e; color: #b1b1b1; padding: 12px 25px;
        border-top-left-radius: 4px; border-top-right-radius: 4px;
        margin-right: 1px; min-width: 140px; font-family: 'Segoe UI';
    }
    QTabBar::tab:selected { background: #323639; color: #ffffff; border-bottom: 3px solid #8ab4f8; }
    
    QLineEdit {
        background-color: #202124; color: #ffffff; border: 1px solid #3c4043;
        border-radius: 20px; padding: 8px 18px; font-size: 14px;
    }
    QLineEdit:focus { border: 1px solid #8ab4f8; }
    
    QTextEdit, QListWidget {
        background-color: #202124; color: #ffffff; border: 1px solid #3c4043;
        border-radius: 8px; padding: 10px; font-size: 13px;
    }

    QPushButton {
        background-color: #3c4043; color: #ffffff; border-radius: 4px;
        padding: 8px 16px; font-weight: bold; border: none;
    }
    QPushButton:hover { background-color: #4f5256; }
    
    QComboBox { 
        background-color: #3c4043; color: #ffffff; border-radius: 4px; padding: 5px; 
        border: 1px solid #555;
    }
    QComboBox QAbstractItemView { background-color: #3c4043; color: #ffffff; }

    QLabel { color: #ffffff; font-weight: bold; font-family: 'Segoe UI'; }
    
    QStatusBar { background-color: #1e1e1e; color: #ffffff; border-top: 1px solid #2d2d2d; }
    
    QSplitter::handle { background-color: #121212; }
"""

HOME_HTML = os.path.join(os.path.dirname(__file__), "cysra_home.html")
NOTES_FILE = "cysra_notes.txt"

class BrowserTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        self.browser = QWebEngineView()
        
        # --- CSS & RENDERING FIX START ---
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        # --- CSS & RENDERING FIX END ---

        self.load_homepage()

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter address")
        self.url_bar.returnPressed.connect(self.navigate)

        nav = QHBoxLayout()
        nav_buttons = [
            ("←", self.browser.back), 
            ("→", self.browser.forward), 
            ("↻", self.browser.reload), 
            ("⌂", self.load_homepage)
        ]
        
        for symbol, func in nav_buttons:
            btn = QPushButton(symbol)
            btn.setFixedWidth(45)
            btn.clicked.connect(func)
            nav.addWidget(btn)

        nav.addWidget(self.url_bar)
        layout.addLayout(nav)
        layout.addWidget(self.browser)

        self.browser.urlChanged.connect(self.on_url_changed)
        self.browser.titleChanged.connect(self.update_title)

    def load_homepage(self):
        if os.path.exists(HOME_HTML):
            self.browser.setUrl(QUrl.fromLocalFile(HOME_HTML))
        else:
            self.browser.setHtml("<body style='background:#121212; color:white; text-align:center;'><h1>Home file missing</h1></body>")

    def on_url_changed(self, url):
        url_str = url.toString()
        if "sysra_home.html" in url_str:
            self.url_bar.setText("")
        else:
            self.url_bar.setText(url_str)
            if hasattr(self.main_window, 'history_widget'):
                self.main_window.history_widget.add_entry(url_str)

    def update_title(self, title):
        parent = self.parentWidget()
        while parent and not isinstance(parent, QTabWidget): parent = parent.parentWidget()
        if parent:
            idx = parent.indexOf(self)
            parent.setTabText(idx, (title[:15] + "..") if len(title) > 15 else (title if title else "Home"))

    def navigate(self):
        val = self.url_bar.text().strip()
        if not val:
            self.load_homepage()
            return
        url = val if val.startswith("http") else f"https://www.google.com/search?q={val.replace(' ', '+')}"
        self.browser.setUrl(QUrl(url))

class DownloadManager(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Downloads"))
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)
        
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.handle_download)

    def handle_download(self, item):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", item.downloadFileName())
        if path:
            item.setPath(path)
            item.accept()
            self.log.append(f"↓ {item.downloadFileName()}")
            item.finished.connect(lambda: self.log.append(f"✓ Finished"))

class HistoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("History"))
        self.list = QListWidget()
        layout.addWidget(self.list)
        btn = QPushButton("Clear List"); btn.clicked.connect(self.list.clear); layout.addWidget(btn)

    def add_entry(self, url):
        if "sysra_home.html" not in url:
            if not self.list.findItems(url, Qt.MatchExactly):
                self.list.insertItem(0, url)

class CalculatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Calculator"))
        self.display = QLineEdit(); self.display.setReadOnly(True); self.display.setAlignment(Qt.AlignRight)
        layout.addWidget(self.display)
        self.inp = QLineEdit(); self.inp.setPlaceholderText("Calculation..."); self.inp.returnPressed.connect(self.run)
        layout.addWidget(self.inp)
        btn = QPushButton("Calculate"); btn.clicked.connect(self.run); layout.addWidget(btn)

    def run(self):
        try: self.display.setText(str(eval(self.inp.text())))
        except: self.display.setText("Error")

class MyAppsWidget(QWidget):
    def __init__(self, main_window):
        super().__init__(); self.main_window = main_window
        layout = QVBoxLayout(self); layout.addWidget(QLabel("Apps"))
        self.app_list = QVBoxLayout(); layout.addLayout(self.app_list)
        btn = QPushButton("Refresh List"); btn.clicked.connect(self.refresh); layout.addWidget(btn)
        self.refresh()

    def refresh(self):
        for i in reversed(range(self.app_list.count())): 
            w = self.app_list.itemAt(i).widget()
            if w: w.setParent(None)
        path = os.path.join(os.path.dirname(__file__), "myapps")
        if not os.path.exists(path): os.mkdir(path)
        for f in [f for f in os.listdir(path) if f.endswith(".py")]:
            btn = QPushButton(f.replace(".py", ""))
            btn.clicked.connect(lambda checked, p=os.path.join(path, f): self.run_app(p))
            self.app_list.addWidget(btn)

    def run_app(self, path):
        spec = importlib.util.spec_from_file_location("mod", path)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        if hasattr(m, 'AppWidget'): self.main_window.add_plugin_tab(m.AppWidget(), os.path.basename(path))

class TranslateWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.addWidget(QLabel("Translator"))
        self.src = QComboBox(); self.tgt = QComboBox()
        langs = {"auto": "Detect", "en": "English", "tr": "Turkish"}
        for k, v in langs.items(): self.src.addItem(v, k); self.tgt.addItem(v, k)
        layout.addWidget(self.src); layout.addWidget(self.tgt)
        self.inp = QTextEdit(); self.inp.setPlaceholderText("Source text..."); layout.addWidget(self.inp)
        btn = QPushButton("Translate Text"); btn.clicked.connect(self.work); layout.addWidget(btn)
        self.out = QTextEdit(); self.out.setReadOnly(True); layout.addWidget(self.out)

    def work(self):
        try: self.out.setPlainText(GoogleTranslator(source=self.src.currentData(), target=self.tgt.currentData()).translate(self.inp.toPlainText()))
        except: self.out.setPlainText("Connection Error")

class NotesWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self); layout.addWidget(QLabel("Notes"))
        self.editor = QTextEdit(); layout.addWidget(self.editor)
        btn = QPushButton("Save Notes"); btn.clicked.connect(self.save); layout.addWidget(btn)
        if os.path.exists(NOTES_FILE):
            with open(NOTES_FILE, "r", encoding="utf-8") as f: self.editor.setPlainText(f.read())

    def save(self):
        with open(NOTES_FILE, "w", encoding="utf-8") as f: f.write(self.editor.toPlainText())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cysra Anome Browser Lite 6.0")
        self.setGeometry(50, 50, 1400, 900)
        self.setStyleSheet(MODERN_STYLE)

        splitter = QSplitter(Qt.Horizontal)
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(lambda i: self.tabs.count() > 1 and self.tabs.removeTab(i))
        
        self.sidebar = QTabWidget()
        self.history_widget = HistoryWidget()
        self.sidebar.addTab(self.history_widget, "History")
        self.sidebar.addTab(TranslateWidget(), "Translate")
        self.sidebar.addTab(NotesWidget(), "Notes")
        self.sidebar.addTab(CalculatorWidget(), "Calc")
        self.sidebar.addTab(MyAppsWidget(self), "Apps")
        self.sidebar.addTab(DownloadManager(), "Downloads")
        
        splitter.addWidget(self.tabs)
        splitter.addWidget(self.sidebar)
        splitter.setSizes([1050, 350])
        self.setCentralWidget(splitter)

        new_tab_btn = QPushButton("+")
        new_tab_btn.setFixedWidth(45)
        new_tab_btn.clicked.connect(self.add_new_tab)
        self.tabs.setCornerWidget(new_tab_btn, Qt.TopRightCorner)
        self.add_new_tab()

    def add_new_tab(self):
        tab = BrowserTab(self)
        idx = self.tabs.addTab(tab, "Home")
        self.tabs.setCurrentIndex(idx)

    def add_plugin_tab(self, widget, name):
        idx = self.sidebar.addTab(widget, name)
        self.sidebar.setCurrentIndex(idx)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())