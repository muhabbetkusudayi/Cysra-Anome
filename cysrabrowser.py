import sys
import os
import json
import time
import importlib.util
import traceback
import gc
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLineEdit, QTextEdit, QLabel, QComboBox,
    QMessageBox, QFileDialog, QListWidget, QListWidgetItem, QFrame,
    QScrollArea, QSizePolicy, QProgressBar, QCheckBox, QRadioButton,
    QStatusBar, QShortcut, QDialog, QStackedWidget, QButtonGroup,
    QGraphicsDropShadowEffect, QAbstractItemView, QToolButton, QMenu
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineProfile, QWebEngineSettings, QWebEnginePage
)
from PyQt5.QtCore import (
    QUrl, Qt, QTimer, QObject, pyqtSignal, QSize, QPoint, QPropertyAnimation,
    QEasingCurve, QAbstractAnimation
)
from PyQt5.QtGui import (
    QColor, QFont, QKeySequence, QPainter, QPainterPath, QPixmap, QIcon
)

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_OK = True
except ImportError:
    TRANSLATOR_OK = False

_DIR       = os.path.dirname(os.path.abspath(__file__))
HOME_HTML  = os.path.join(_DIR, "cysra_home.html")
NOTES_FILE = os.path.join(_DIR, "cysra_notes.txt")
DATA_FILE  = os.path.join(_DIR, "cysra_data.json")
APPS_DIR   = os.path.join(_DIR, "myapps")

PALETTES = {
    "dark": {
        "bg":             "#202124",
        "toolbar":        "#292a2d",
        "tab_strip":      "#1a1b1e",
        "tab_bg":         "#2a2b2e",
        "tab_active":     "#202124",
        "tab_text":       "#9aa0a6",
        "tab_active_txt": "#e8eaed",
        "url_bg":         "#303134",
        "url_focus_bg":   "#1e1f22",
        "url_focus_bdr":  "#5b8dee",
        "btn_hover":      "#3c4043",
        "accent":         "#5b8dee",
        "accent2":        "#8ab4f8",
        "text":           "#e8eaed",
        "text2":          "#9aa0a6",
        "text3":          "#5f6368",
        "border":         "#3c4043",
        "card":           "#2d2e31",
        "icon_bar":       "#1a1b1e",
        "panel_bg":       "#1e1f22",
        "panel_hdr":      "#252629",
        "input_bg":       "#303134",
        "input_bdr":      "#5f6368",
        "success":        "#81c995",
        "warning":        "#fdd663",
        "danger":         "#f28b82",
        "scrollbar":      "#5f6368",
        "selection":      "#3b5595",
        "star_off":       "#9aa0a6",
        "star_on":        "#fdd663",
        "tag_bg":         "rgba(91,141,238,0.14)",
        "ext_colors":     ["#5b8dee","#81c995","#f28b82","#fdd663",
                           "#c58af9","#ff8bcb","#78d9ec","#ffb86c"],
    },
    "light": {
        "bg":             "#ffffff",
        "toolbar":        "#f1f3f4",
        "tab_strip":      "#dee1e6",
        "tab_bg":         "#dee1e6",
        "tab_active":     "#ffffff",
        "tab_text":       "#5f6368",
        "tab_active_txt": "#202124",
        "url_bg":         "#f1f3f4",
        "url_focus_bg":   "#ffffff",
        "url_focus_bdr":  "#1a73e8",
        "btn_hover":      "#e8eaed",
        "accent":         "#1a73e8",
        "accent2":        "#1558b0",
        "text":           "#202124",
        "text2":          "#5f6368",
        "text3":          "#9aa0a6",
        "border":         "#dadce0",
        "card":           "#f8f9fa",
        "icon_bar":       "#e8eaed",
        "panel_bg":       "#f1f3f4",
        "panel_hdr":      "#e8eaed",
        "input_bg":       "#ffffff",
        "input_bdr":      "#dadce0",
        "success":        "#188038",
        "warning":        "#f29900",
        "danger":         "#d93025",
        "scrollbar":      "#dadce0",
        "selection":      "#d2e3fc",
        "star_off":       "#5f6368",
        "star_on":        "#f29900",
        "tag_bg":         "rgba(26,115,232,0.10)",
        "ext_colors":     ["#1a73e8","#188038","#d93025","#f29900",
                           "#9334e6","#e91e8c","#129eaf","#e8710a"],
    },
}

_theme = "dark"

def p(k):
    return PALETTES[_theme][k]

def set_theme(name):
    global _theme
    _theme = name


def build_stylesheet():
    return """
QWidget {
    background: """ + p("bg") + """;
    color: """ + p("text") + """;
    font-family: -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    outline: none;
}
QMainWindow { background: """ + p("bg") + """; }

QTabWidget::pane { border: none; background: """ + p("bg") + """; }
QTabBar { background: """ + p("tab_strip") + """; }
QTabBar::tab {
    background: """ + p("tab_bg") + """;
    color: """ + p("tab_text") + """;
    padding: 0 16px;
    height: 36px;
    min-width: 80px;
    max-width: 200px;
    font-size: 12px;
    font-weight: 500;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: none;
    margin-right: 2px;
    margin-top: 4px;
}
QTabBar::tab:selected {
    background: """ + p("tab_active") + """;
    color: """ + p("tab_active_txt") + """;
    font-weight: 600;
    margin-top: 2px;
    height: 38px;
}
QTabBar::tab:hover:!selected {
    background: """ + p("btn_hover") + """;
    color: """ + p("text") + """;
}

QFrame#toolbar {
    background: """ + p("toolbar") + """;
    border-bottom: 1px solid """ + p("border") + """;
}
QFrame#iconBar {
    background: """ + p("icon_bar") + """;
    border-right: 1px solid """ + p("border") + """;
}
QFrame#slidePanel {
    background: """ + p("panel_bg") + """;
    border-right: 1px solid """ + p("border") + """;
}
QFrame#panelHeader {
    background: """ + p("panel_hdr") + """;
    border-bottom: 1px solid """ + p("border") + """;
}
QFrame#card {
    background: """ + p("card") + """;
    border: 1px solid """ + p("border") + """;
    border-radius: 10px;
}
QFrame#urlFrame {
    background: """ + p("url_bg") + """;
    border: 1.5px solid transparent;
    border-radius: 22px;
    min-height: 36px;
    max-height: 36px;
}

QPushButton {
    background: transparent;
    color: """ + p("text2") + """;
    border: none;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 500;
}
QPushButton:hover {
    background: """ + p("btn_hover") + """;
    color: """ + p("text") + """;
}
QPushButton:pressed { background: """ + p("border") + """; }

QPushButton#navBtn {
    border-radius: 18px;
    padding: 0;
    min-width: 34px;
    min-height: 34px;
    max-width: 34px;
    max-height: 34px;
    font-size: 16px;
    color: """ + p("text2") + """;
}
QPushButton#navBtn:hover {
    background: """ + p("btn_hover") + """;
    color: """ + p("text") + """;
}
QPushButton#navBtn:disabled { color: """ + p("border") + """; background: transparent; }

QPushButton#iconBtn {
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
    border-radius: 10px;
    padding: 0;
    font-size: 17px;
    color: """ + p("text3") + """;
}
QPushButton#iconBtn:hover {
    background: """ + p("btn_hover") + """;
    color: """ + p("text") + """;
}

QPushButton#accentBtn {
    background: """ + p("accent") + """;
    color: #ffffff;
    font-weight: 600;
    border-radius: 8px;
    padding: 7px 18px;
}
QPushButton#accentBtn:hover { background: """ + p("accent2") + """; }

QPushButton#starBtn {
    background: transparent;
    color: """ + p("star_off") + """;
    border: none;
    border-radius: 16px;
    min-width: 28px;
    max-width: 28px;
    min-height: 28px;
    max-height: 28px;
    padding: 0;
    font-size: 15px;
}
QPushButton#starBtn:hover { background: """ + p("btn_hover") + """; }

QPushButton#dangerBtn {
    color: """ + p("danger") + """;
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 6px;
}
QPushButton#dangerBtn:hover { background: """ + p("btn_hover") + """; }

QLineEdit {
    background: """ + p("input_bg") + """;
    color: """ + p("text") + """;
    border: 1px solid """ + p("input_bdr") + """;
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 13px;
    selection-background-color: """ + p("selection") + """;
}
QLineEdit:focus { border-color: """ + p("accent") + """; }

QLineEdit#urlInput {
    background: transparent;
    border: none;
    color: """ + p("text") + """;
    font-size: 14px;
    padding: 0;
    selection-background-color: """ + p("selection") + """;
}

QTextEdit {
    background: """ + p("input_bg") + """;
    color: """ + p("text") + """;
    border: 1px solid """ + p("input_bdr") + """;
    border-radius: 8px;
    padding: 8px;
    font-size: 13px;
    selection-background-color: """ + p("selection") + """;
}
QTextEdit:focus { border-color: """ + p("accent") + """; }

QListWidget {
    background: """ + p("input_bg") + """;
    color: """ + p("text") + """;
    border: 1px solid """ + p("border") + """;
    border-radius: 10px;
    padding: 4px;
    outline: none;
    font-size: 12px;
}
QListWidget::item {
    padding: 8px 10px;
    border-radius: 6px;
}
QListWidget::item:selected {
    background: """ + p("accent") + """;
    color: #ffffff;
}
QListWidget::item:hover:!selected { background: """ + p("btn_hover") + """; }

QComboBox {
    background: """ + p("input_bg") + """;
    color: """ + p("text") + """;
    border: 1px solid """ + p("input_bdr") + """;
    border-radius: 8px;
    padding: 6px 10px;
    font-size: 13px;
    min-height: 30px;
}
QComboBox:focus { border-color: """ + p("accent") + """; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background: """ + p("card") + """;
    color: """ + p("text") + """;
    border: 1px solid """ + p("border") + """;
    border-radius: 8px;
    selection-background-color: """ + p("accent") + """;
    outline: none;
    padding: 4px;
}

QLabel { background: transparent; color: """ + p("text") + """; }
QLabel#sectionHead {
    font-size: 11px;
    font-weight: 700;
    color: """ + p("text2") + """;
    letter-spacing: 0.6px;
}
QLabel#mutedLabel { color: """ + p("text2") + """; font-size: 12px; }
QLabel#badgeLabel {
    color: """ + p("accent") + """;
    font-size: 11px;
    font-weight: 700;
    background: """ + p("tag_bg") + """;
    border-radius: 4px;
    padding: 2px 8px;
}

QProgressBar {
    background: transparent;
    border: none;
    height: 3px;
    color: transparent;
    font-size: 0;
}
QProgressBar::chunk {
    background: """ + p("accent") + """;
    border-radius: 1px;
}

QScrollBar:vertical { background: transparent; width: 7px; margin: 2px; }
QScrollBar::handle:vertical {
    background: """ + p("scrollbar") + """;
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: """ + p("accent") + """; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 7px; margin: 2px; }
QScrollBar::handle:horizontal {
    background: """ + p("scrollbar") + """;
    border-radius: 3px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover { background: """ + p("accent") + """; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QStatusBar {
    background: """ + p("toolbar") + """;
    color: """ + p("text2") + """;
    border-top: 1px solid """ + p("border") + """;
    font-size: 11px;
    min-height: 20px;
    padding: 0 8px;
}
QStatusBar::item { border: none; }

QSplitter::handle { background: """ + p("border") + """; width: 1px; }

QCheckBox { color: """ + p("text") + """; spacing: 9px; }
QCheckBox::indicator {
    width: 15px; height: 15px;
    border: 1.5px solid """ + p("input_bdr") + """;
    border-radius: 3px;
    background: """ + p("input_bg") + """;
}
QCheckBox::indicator:checked {
    background: """ + p("accent") + """;
    border-color: """ + p("accent") + """;
}
QRadioButton { color: """ + p("text") + """; spacing: 9px; }
QRadioButton::indicator {
    width: 15px; height: 15px;
    border: 1.5px solid """ + p("input_bdr") + """;
    border-radius: 8px;
    background: """ + p("input_bg") + """;
}
QRadioButton::indicator:checked {
    background: """ + p("accent") + """;
    border-color: """ + p("accent") + """;
}

QMenu {
    background: """ + p("card") + """;
    color: """ + p("text") + """;
    border: 1px solid """ + p("border") + """;
    border-radius: 8px;
    padding: 4px;
}
QMenu::item { padding: 7px 16px; border-radius: 5px; }
QMenu::item:selected { background: """ + p("btn_hover") + """; }
QMenu::separator { background: """ + p("border") + """; height: 1px; margin: 3px 8px; }
"""


OPT_JS = """
(function(){
    if(window.__cysra__)return;
    window.__cysra__=true;
    var _r=new WeakMap(),_o=EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener=function(t,f,op){
        if(!_r.has(this))_r.set(this,{});
        var k=t+'|'+(f.name||f.toString().slice(0,80));
        if(_r.get(this)[k])return;
        _r.get(this)[k]=true;
        _o.call(this,t,f,op);
    };
    var prune=function(){
        document.querySelectorAll('[style*="display:none"],[style*="display: none"]').forEach(function(el){
            if(!el.id&&!el.className&&!el.children.length&&!el.innerHTML.trim())
                try{el.remove()}catch(e){}
        });
    };
    new MutationObserver(prune).observe(document.documentElement,{childList:true,subtree:true});
    prune();
    document.querySelectorAll('img').forEach(function(img){
        if(img._c)return;img._c=true;
        img.addEventListener('error',function(){
            if(!this._r){this._r=true;var s=this.src;this.src='';this.src=s;}
        });
    });
    if(!document.getElementById('__cysra_s__')){
        var s=document.createElement('style');
        s.id='__cysra_s__';
        s.textContent='html{overflow-x:hidden!important}*{box-sizing:border-box!important}';
        (document.head||document.documentElement).appendChild(s);
    }
})();
"""

SECRET_JS = """
(function(){
    if(window.__cysra_secret__)return;
    window.__cysra_secret__=true;
    ['localStorage','sessionStorage'].forEach(function(k){
        try{Object.defineProperty(window,k,{
            get:function(){return new Proxy({},{get:function(t,p){return p==='length'?0:null;},set:function(){return true;}});},
            configurable:true
        });}catch(e){}
    });
    try{navigator.sendBeacon=function(){return false;};}catch(e){}
})();
"""


def safe_eval(expr):
    allowed = {"abs": abs, "round": round, "min": min, "max": max,
               "sum": sum, "pow": pow, "int": int, "float": float, "len": len}
    try:
        code = compile(expr, "<calc>", "eval")
        for name in code.co_names:
            if name not in allowed:
                return "Error: name '" + name + "' not allowed"
        return eval(code, {"__builtins__": {}}, allowed)
    except Exception as exc:
        return "Error: " + str(exc)


def make_letter_pixmap(letter, color_hex, size=34):
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    painter = QPainter(pm)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.fillPath(path, QColor(color_hex))
    painter.setPen(QColor("#ffffff"))
    font = QFont("-apple-system", int(size * 0.38))
    font.setWeight(QFont.Bold)
    painter.setFont(font)
    from PyQt5.QtCore import QRect
    painter.drawText(QRect(0, 0, size, size), Qt.AlignCenter, letter.upper())
    painter.end()
    return pm


class DataStore(QObject):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._data = {"history": [], "favorites": []}
        self._load()

    def _load(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data = loaded
        except Exception:
            self._data = {"history": [], "favorites": []}

    def _save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            print("DataStore save error:", exc)

    def add_history(self, url, title=""):
        skip_patterns = ["cysra_home.html", "about:blank", "about:", "view-source:"]
        for pat in skip_patterns:
            if pat in url:
                return
        if not url:
            return
        self._data["history"] = [
            e for e in self._data.get("history", []) if e.get("url") != url
        ]
        self._data["history"].insert(0, {
            "url":   url,
            "title": title or url,
            "ts":    datetime.now().strftime("%d %b %H:%M"),
        })
        if len(self._data["history"]) > 2000:
            self._data["history"] = self._data["history"][:2000]
        self._save()
        self.changed.emit()

    def clear_history(self):
        self._data["history"] = []
        self._save()
        self.changed.emit()

    @property
    def history(self):
        return self._data.get("history", [])

    def add_favorite(self, url, title=""):
        favs = self._data.setdefault("favorites", [])
        if not any(f.get("url") == url for f in favs):
            favs.append({"url": url, "title": title or url})
            self._save()
            self.changed.emit()

    def remove_favorite(self, url):
        self._data["favorites"] = [
            f for f in self._data.get("favorites", []) if f.get("url") != url
        ]
        self._save()
        self.changed.emit()

    def is_favorite(self, url):
        return any(f.get("url") == url for f in self._data.get("favorites", []))

    @property
    def favorites(self):
        return self._data.get("favorites", [])


class SecurePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, src):
        pass

    def javaScriptAlert(self, url, msg):
        pass

    def certificateError(self, error):
        return False


class AddressBar(QFrame):
    navigateRequested = pyqtSignal(str)
    favoriteToggled   = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("urlFrame")
        self.setCursor(Qt.IBeamCursor)
        self._is_favorite = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 8, 0)
        layout.setSpacing(4)

        self.star_btn = QPushButton("☆")
        self.star_btn.setObjectName("starBtn")
        self.star_btn.setToolTip("Add to Favorites (Ctrl+D)")
        self.star_btn.setCursor(Qt.PointingHandCursor)
        self.star_btn.clicked.connect(self.favoriteToggled)
        layout.addWidget(self.star_btn)

        self.sec_label = QLabel()
        self.sec_label.setFixedWidth(36)
        self.sec_label.setAlignment(Qt.AlignCenter)
        self.sec_label.setStyleSheet(
            "font-size:10px;font-weight:700;background:transparent;padding:0 2px;"
            "color:" + p("text3") + ";"
        )
        layout.addWidget(self.sec_label)

        self.url_input = QLineEdit()
        self.url_input.setObjectName("urlInput")
        self.url_input.setPlaceholderText("Search or enter web address")
        self.url_input.returnPressed.connect(
            lambda: self.navigateRequested.emit(self.url_input.text().strip())
        )

        original_focus_in  = self.url_input.focusInEvent
        original_focus_out = self.url_input.focusOutEvent

        def on_focus_in(ev):
            self.setStyleSheet(
                "QFrame#urlFrame{background:" + p("url_focus_bg") + ";"
                "border:1.5px solid " + p("url_focus_bdr") + ";border-radius:22px;}"
            )
            self.url_input.selectAll()
            original_focus_in(ev)

        def on_focus_out(ev):
            self.setStyleSheet(
                "QFrame#urlFrame{background:" + p("url_bg") + ";"
                "border:1.5px solid transparent;border-radius:22px;}"
            )
            original_focus_out(ev)

        self.url_input.focusInEvent  = on_focus_in
        self.url_input.focusOutEvent = on_focus_out
        layout.addWidget(self.url_input, 1)

    def set_url(self, url_str, is_home=False):
        self.url_input.setText("" if is_home else url_str)
        scheme = QUrl(url_str).scheme() if url_str else ""
        if scheme == "https":
            self.sec_label.setText("HTTPS")
            self.sec_label.setStyleSheet(
                "font-size:10px;font-weight:700;background:transparent;"
                "color:" + p("success") + ";padding:0 2px;"
            )
        elif scheme == "http":
            self.sec_label.setText("HTTP")
            self.sec_label.setStyleSheet(
                "font-size:10px;font-weight:700;background:transparent;"
                "color:" + p("warning") + ";padding:0 2px;"
            )
        else:
            self.sec_label.setText("")
            self.sec_label.setStyleSheet(
                "font-size:10px;font-weight:700;background:transparent;"
                "color:" + p("text3") + ";padding:0 2px;"
            )

    def set_favorite(self, on):
        self._is_favorite = on
        self.star_btn.setText("★" if on else "☆")
        color = p("star_on") if on else p("star_off")
        self.star_btn.setStyleSheet(
            "QPushButton#starBtn{background:transparent;color:" + color + ";"
            "border:none;border-radius:16px;min-width:28px;max-width:28px;"
            "min-height:28px;max-height:28px;padding:0;font-size:15px;}"
            "QPushButton#starBtn:hover{background:" + p("btn_hover") + ";}"
        )
        tip = "Remove from Favorites" if on else "Add to Favorites (Ctrl+D)"
        self.star_btn.setToolTip(tip)

    def focus(self):
        self.url_input.selectAll()
        self.url_input.setFocus()


class IconBar(QFrame):
    icon_clicked = pyqtSignal(str)

    ITEMS = [
        ("favorites",  "★",  "Favorites"),
        ("history",    "◷",  "History"),
        ("downloads",  "↓",  "Downloads"),
        ("extensions", "⊞",  "Extensions"),
        ("translate",  "⇄",  "Translate"),
        ("notes",      "✏",  "Notes"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("iconBar")
        self.setFixedWidth(52)
        self._active = None
        self._buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 10, 6, 10)
        layout.setSpacing(4)
        layout.setAlignment(Qt.AlignTop)

        for key, symbol, tooltip in self.ITEMS:
            btn = QPushButton(symbol)
            btn.setObjectName("iconBtn")
            btn.setToolTip(tooltip)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(40, 40)
            btn.clicked.connect(lambda checked=False, k=key: self._on_click(k))
            layout.addWidget(btn)
            self._buttons[key] = btn

        layout.addStretch()

    def _on_click(self, key):
        self.icon_clicked.emit(key)

    def set_active(self, key):
        self._active = key
        for k, btn in self._buttons.items():
            if k == key:
                btn.setStyleSheet(
                    "QPushButton#iconBtn{"
                    "background:" + p("tag_bg") + ";"
                    "color:" + p("accent") + ";"
                    "border-radius:10px;}"
                    "QPushButton#iconBtn:hover{"
                    "background:" + p("tag_bg") + ";"
                    "color:" + p("accent") + ";}"
                )
            else:
                btn.setStyleSheet(
                    "QPushButton#iconBtn{"
                    "background:transparent;"
                    "color:" + p("text3") + ";"
                    "border-radius:10px;}"
                    "QPushButton#iconBtn:hover{"
                    "background:" + p("btn_hover") + ";"
                    "color:" + p("text") + ";}"
                )

    def clear_active(self):
        self._active = None
        for btn in self._buttons.values():
            btn.setStyleSheet(
                "QPushButton#iconBtn{"
                "background:transparent;"
                "color:" + p("text3") + ";"
                "border-radius:10px;}"
                "QPushButton#iconBtn:hover{"
                "background:" + p("btn_hover") + ";"
                "color:" + p("text") + ";}"
            )


class FavoritesPage(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, store):
        super().__init__()
        self.store = store
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        self.list = QListWidget()
        self.list.setAlternatingRowColors(False)
        self.list.itemDoubleClicked.connect(
            lambda i: self.navigate.emit(i.data(Qt.UserRole))
        )
        lay.addWidget(self.list)

        hint = QLabel("Double-click to open · Right-click to remove")
        hint.setObjectName("mutedLabel")
        hint.setAlignment(Qt.AlignCenter)
        lay.addWidget(hint)

        store.changed.connect(self.refresh)
        self.refresh()

    def refresh(self):
        self.list.clear()
        for fav in self.store.favorites:
            item = QListWidgetItem()
            title = fav.get("title", "") or fav.get("url", "")
            if len(title) > 48:
                title = title[:46] + "…"
            item.setText(title)
            item.setToolTip(fav.get("url", ""))
            item.setData(Qt.UserRole, fav.get("url", ""))
            self.list.addItem(item)

    def contextMenuEvent(self, ev):
        item = self.list.itemAt(self.list.mapFromGlobal(ev.globalPos()))
        if not item:
            return
        url = item.data(Qt.UserRole)
        menu = QMenu(self)
        open_act   = menu.addAction("Open")
        remove_act = menu.addAction("Remove from Favorites")
        action = menu.exec_(ev.globalPos())
        if action == open_act:
            self.navigate.emit(url)
        elif action == remove_act:
            self.store.remove_favorite(url)


class HistoryPage(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, store):
        super().__init__()
        self.store = store
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        top = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter…")
        self.search.textChanged.connect(self._filter)
        top.addWidget(self.search)

        clr = QPushButton("Clear All")
        clr.setObjectName("dangerBtn")
        clr.clicked.connect(self._clear)
        top.addWidget(clr)
        lay.addLayout(top)

        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(
            lambda i: self.navigate.emit(i.data(Qt.UserRole))
        )
        lay.addWidget(self.list)

        hint = QLabel("Double-click to revisit")
        hint.setObjectName("mutedLabel")
        hint.setAlignment(Qt.AlignCenter)
        lay.addWidget(hint)

        store.changed.connect(self.refresh)
        self.refresh()

    def refresh(self):
        self.list.clear()
        for entry in self.store.history:
            item = QListWidgetItem()
            title = entry.get("title", "") or entry.get("url", "")
            if len(title) > 46:
                title = title[:44] + "…"
            item.setText(title + "\n" + entry.get("ts", ""))
            item.setData(Qt.UserRole, entry.get("url", ""))
            item.setToolTip(entry.get("url", ""))
            self.list.addItem(item)

    def _filter(self, text):
        t = text.lower()
        for i in range(self.list.count()):
            item = self.list.item(i)
            url  = (item.data(Qt.UserRole) or "").lower()
            txt  = item.text().lower()
            item.setHidden(bool(t) and t not in url and t not in txt)

    def _clear(self):
        reply = QMessageBox.question(
            self, "Clear History",
            "Delete all browsing history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.store.clear_history()


class DownloadsPage(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        top = QHBoxLayout()
        lbl = QLabel("Downloads")
        lbl.setObjectName("sectionHead")
        top.addWidget(lbl)
        top.addStretch()
        clr = QPushButton("Clear List")
        clr.setObjectName("dangerBtn")
        top.addWidget(clr)
        lay.addLayout(top)

        self.list = QListWidget()
        clr.clicked.connect(self.list.clear)
        lay.addWidget(self.list)

    def add_item(self, filename):
        item = QListWidgetItem("Downloading: " + filename)
        self.list.insertItem(0, item)
        return item

    def mark_done(self, item, filename):
        item.setText("Done: " + filename)


class ExtensionsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        top = QHBoxLayout()
        lbl = QLabel("Extensions")
        lbl.setObjectName("sectionHead")
        top.addWidget(lbl)
        top.addStretch()
        ref = QPushButton("Refresh")
        ref.clicked.connect(self.refresh)
        top.addWidget(ref)
        lay.addLayout(top)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        inner = QWidget()
        self._inner_lay = QVBoxLayout(inner)
        self._inner_lay.setSpacing(6)
        scroll.setWidget(inner)
        lay.addWidget(scroll)
        self.refresh()

    def refresh(self):
        while self._inner_lay.count():
            child = self._inner_lay.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not os.path.exists(APPS_DIR):
            try:
                os.makedirs(APPS_DIR)
            except Exception:
                pass

        try:
            files = sorted(f for f in os.listdir(APPS_DIR) if f.endswith(".py"))
        except Exception:
            files = []

        colors = p("ext_colors")

        if not files:
            hint = QLabel(
                "Put .py files with an AppWidget class\n"
                "in the  myapps/  folder."
            )
            hint.setObjectName("mutedLabel")
            hint.setAlignment(Qt.AlignCenter)
            hint.setWordWrap(True)
            self._inner_lay.addWidget(hint)
        else:
            for idx, fname in enumerate(files):
                name   = fname.replace(".py", "")
                color  = colors[idx % len(colors)]
                path   = os.path.join(APPS_DIR, fname)
                row    = self._make_row(name, color, path)
                self._inner_lay.addWidget(row)

        self._inner_lay.addStretch()

    def _make_row(self, name, color, path):
        btn = QPushButton()
        btn.setFixedHeight(52)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            "QPushButton{background:" + p("card") + ";border:1px solid " + p("border") + ";"
            "border-radius:10px;text-align:left;padding:0 12px;}"
            "QPushButton:hover{background:" + p("btn_hover") + ";border-color:" + p("accent") + ";}"
        )

        row_lay = QHBoxLayout(btn)
        row_lay.setContentsMargins(0, 0, 0, 0)
        row_lay.setSpacing(12)

        avatar = QLabel()
        avatar.setPixmap(make_letter_pixmap(name[0], color, 32))
        avatar.setFixedSize(32, 32)
        avatar.setAttribute(Qt.WA_TransparentForMouseEvents)
        row_lay.addWidget(avatar)

        lbl = QLabel(name)
        lbl.setStyleSheet("font-size:13px;font-weight:600;color:" + p("text") + ";background:transparent;")
        lbl.setAttribute(Qt.WA_TransparentForMouseEvents)
        row_lay.addWidget(lbl, 1)

        arrow = QLabel("›")
        arrow.setStyleSheet("color:" + p("text2") + ";font-size:18px;background:transparent;")
        arrow.setAttribute(Qt.WA_TransparentForMouseEvents)
        row_lay.addWidget(arrow)

        btn.clicked.connect(lambda _=False, p_=path, n=name, c=color: self._launch(p_, n, c, btn))
        return btn

    def _launch(self, path, name, color, source_btn):
        try:
            spec = importlib.util.spec_from_file_location("cysra_plugin", path)
            mod  = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "AppWidget"):
                widget = mod.AppWidget()
                dlg    = QDialog(self.mw, Qt.Dialog)
                dlg.setWindowTitle(name)
                dlg.setMinimumSize(400, 300)
                dlg.setStyleSheet(build_stylesheet())
                dlg_lay = QVBoxLayout(dlg)
                dlg_lay.setContentsMargins(0, 0, 0, 0)
                dlg_lay.addWidget(widget)
                dlg.show()
            else:
                QMessageBox.information(
                    self, name,
                    "This extension has no AppWidget class."
                )
        except Exception:
            QMessageBox.critical(self, "Extension Error", traceback.format_exc())


class TranslatePage(QWidget):
    LANGS = {
        "auto": "Auto Detect", "en": "English", "tr": "Turkish",
        "de": "German", "fr": "French", "es": "Spanish",
        "ru": "Russian", "zh-CN": "Chinese", "ar": "Arabic",
        "ja": "Japanese", "ko": "Korean", "pt": "Portuguese", "it": "Italian",
    }

    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        row = QHBoxLayout()
        row.setSpacing(6)
        self.src_combo = QComboBox()
        self.tgt_combo = QComboBox()
        for k, v in self.LANGS.items():
            self.src_combo.addItem(v, k)
            if k != "auto":
                self.tgt_combo.addItem(v, k)
        arrow = QLabel("→")
        arrow.setAlignment(Qt.AlignCenter)
        arrow.setFixedWidth(18)
        row.addWidget(self.src_combo, 1)
        row.addWidget(arrow)
        row.addWidget(self.tgt_combo, 1)
        lay.addLayout(row)

        self.src_text = QTextEdit()
        self.src_text.setPlaceholderText("Source text…")
        self.src_text.setMaximumHeight(110)
        lay.addWidget(self.src_text)

        go_btn = QPushButton("Translate")
        go_btn.setObjectName("accentBtn")
        go_btn.clicked.connect(self._go)
        lay.addWidget(go_btn)

        self.out_text = QTextEdit()
        self.out_text.setReadOnly(True)
        self.out_text.setPlaceholderText("Translation…")
        lay.addWidget(self.out_text, 1)

    def _go(self):
        if not TRANSLATOR_OK:
            self.out_text.setPlainText(
                "deep-translator not installed.\n"
                "Run:  pip install deep-translator"
            )
            return
        try:
            result = GoogleTranslator(
                source=self.src_combo.currentData(),
                target=self.tgt_combo.currentData()
            ).translate(self.src_text.toPlainText())
            self.out_text.setPlainText(result or "")
        except Exception as exc:
            self.out_text.setPlainText("Error: " + str(exc))


class NotesPage(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(8)

        top = QHBoxLayout()
        lbl = QLabel("Notes")
        lbl.setObjectName("sectionHead")
        top.addWidget(lbl)
        top.addStretch()
        save_btn = QPushButton("Save")
        save_btn.setObjectName("accentBtn")
        save_btn.setFixedHeight(28)
        save_btn.clicked.connect(self._save)
        top.addWidget(save_btn)
        lay.addLayout(top)

        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Write anything…")
        lay.addWidget(self.editor, 1)

        self._load()

    def _load(self):
        try:
            if os.path.exists(NOTES_FILE):
                with open(NOTES_FILE, encoding="utf-8") as f:
                    self.editor.setPlainText(f.read())
        except Exception as exc:
            print("Notes load error:", exc)

    def _save(self):
        try:
            text = self.editor.toPlainText()
            with open(NOTES_FILE, "w", encoding="utf-8") as f:
                f.write(text)
            QMessageBox.information(self, "Notes", "Notes saved successfully.")
        except Exception as exc:
            QMessageBox.critical(self, "Notes Error", "Could not save:\n" + str(exc))


class SlidePanel(QFrame):
    navigate = pyqtSignal(str)

    def __init__(self, store, downloads_page, main_window, parent=None):
        super().__init__(parent)
        self.setObjectName("slidePanel")
        self.setFixedWidth(0)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._header_lbl = QLabel("")
        self._header_lbl.setObjectName("sectionHead")
        hdr_frame = QFrame()
        hdr_frame.setObjectName("panelHeader")
        hdr_frame.setFixedHeight(42)
        hdr_lay = QHBoxLayout(hdr_frame)
        hdr_lay.setContentsMargins(16, 0, 10, 0)
        hdr_lay.addWidget(self._header_lbl)
        hdr_lay.addStretch()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(26, 26)
        close_btn.setStyleSheet(
            "QPushButton{background:transparent;color:" + p("text2") + ";"
            "border:none;border-radius:13px;font-size:13px;}"
            "QPushButton:hover{background:" + p("btn_hover") + ";color:" + p("text") + ";}"
        )
        close_btn.clicked.connect(self._request_close)
        hdr_lay.addWidget(close_btn)
        outer.addWidget(hdr_frame)

        self.stack = QStackedWidget()
        outer.addWidget(self.stack, 1)

        self._fav_page  = FavoritesPage(store)
        self._hist_page = HistoryPage(store)
        self._dl_page   = downloads_page
        self._ext_page  = ExtensionsPage(main_window)
        self._tr_page   = TranslatePage()
        self._note_page = NotesPage()

        self._pages = {
            "favorites":  (self._fav_page,  "Favorites"),
            "history":    (self._hist_page, "History"),
            "downloads":  (self._dl_page,   "Downloads"),
            "extensions": (self._ext_page,  "Extensions"),
            "translate":  (self._tr_page,   "Translate"),
            "notes":      (self._note_page, "Notes"),
        }

        for page, _ in self._pages.values():
            self.stack.addWidget(page)

        self._fav_page.navigate.connect(self.navigate)
        self._hist_page.navigate.connect(self.navigate)

        self._anim = QPropertyAnimation(self, b"maximumWidth")
        self._anim.setDuration(160)
        self._anim.setEasingCurve(QEasingCurve.OutCubic)

        self._open_width = 290
        self._is_open    = False
        self._close_cb   = None

    def set_close_callback(self, cb):
        self._close_cb = cb

    def _request_close(self):
        self.close_panel()
        if self._close_cb:
            self._close_cb()

    def show_page(self, key):
        if key not in self._pages:
            return
        page, label = self._pages[key]
        self._header_lbl.setText(label.upper())
        self.stack.setCurrentWidget(page)
        if not self._is_open:
            self._is_open = True
            self._anim.setStartValue(0)
            self._anim.setEndValue(self._open_width)
            self.setMaximumWidth(0)
            self.show()
            self._anim.start()

    def close_panel(self):
        if not self._is_open:
            return
        self._is_open = False
        self._anim.setStartValue(self._open_width)
        self._anim.setEndValue(0)
        self._anim.start()
        self._anim.finished.connect(self._on_close_done)

    def _on_close_done(self):
        try:
            self._anim.finished.disconnect(self._on_close_done)
        except Exception:
            pass
        if not self._is_open:
            self.hide()

    def is_open(self):
        return self._is_open

    def current_key(self):
        for key, (page, _) in self._pages.items():
            if self.stack.currentWidget() is page:
                return key
        return None


class BrowserTab(QWidget):
    titleChanged = pyqtSignal(str)
    urlChanged   = pyqtSignal(str)

    def __init__(self, main_window, store, secret=False, opt=False):
        super().__init__()
        self.mw     = main_window
        self.store  = store
        self.secret = secret
        self._opt   = opt
        self._build()
        self.load_home()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        bar = QFrame()
        bar.setObjectName("toolbar")
        bar.setFixedHeight(54)
        bl  = QHBoxLayout(bar)
        bl.setContentsMargins(10, 0, 10, 0)
        bl.setSpacing(4)

        for symbol, slot, tip in [
            ("←", lambda: self.view.back(),    "Back  (Alt+Left)"),
            ("→", lambda: self.view.forward(), "Forward  (Alt+Right)"),
            ("↺", lambda: self.view.reload(),  "Reload  (F5)"),
        ]:
            btn = QPushButton(symbol)
            btn.setObjectName("navBtn")
            btn.setToolTip(tip)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(slot)
            bl.addWidget(btn)

        bl.addSpacing(4)

        self.addr = AddressBar(self)
        self.addr.navigateRequested.connect(self._navigate_from_bar)
        self.addr.favoriteToggled.connect(self._toggle_favorite)
        bl.addWidget(self.addr, 1)

        bl.addSpacing(4)

        src_btn = QPushButton("{ }")
        src_btn.setObjectName("navBtn")
        src_btn.setToolTip("View Page Source  (Ctrl+U)")
        src_btn.setCursor(Qt.PointingHandCursor)
        src_btn.setStyleSheet(
            "QPushButton#navBtn{font-size:11px;font-weight:700;}"
        )
        src_btn.clicked.connect(self._view_source)
        bl.addWidget(src_btn)

        self.opt_btn = QPushButton("OPT")
        self.opt_btn.setObjectName("navBtn")
        self.opt_btn.setCheckable(True)
        self.opt_btn.setChecked(self._opt)
        self.opt_btn.setToolTip("Toggle Optimization Engine")
        self.opt_btn.setCursor(Qt.PointingHandCursor)
        self.opt_btn.setStyleSheet(
            "QPushButton#navBtn{font-size:10px;font-weight:700;}"
            "QPushButton#navBtn:checked{color:" + p("accent") + ";}"
        )
        self.opt_btn.toggled.connect(self._on_opt)
        bl.addWidget(self.opt_btn)

        root.addWidget(bar)

        self.prog = QProgressBar()
        self.prog.setFixedHeight(3)
        self.prog.setTextVisible(False)
        self.prog.setRange(0, 100)
        self.prog.setValue(0)
        root.addWidget(self.prog)

        if self.secret:
            profile = QWebEngineProfile(self)
        else:
            profile = QWebEngineProfile.defaultProfile()

        self.page = SecurePage(profile, self)
        self.view = QWebEngineView(self)
        self.view.setPage(self.page)

        s = self.view.settings()
        s.setAttribute(QWebEngineSettings.JavascriptEnabled,               True)
        s.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls,   True)
        s.setAttribute(QWebEngineSettings.AutoLoadImages,                  True)
        s.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows,        False)

        root.addWidget(self.view, 1)

        self.view.urlChanged.connect(self._url_changed)
        self.view.titleChanged.connect(self.titleChanged)
        self.view.loadStarted.connect(lambda: self.prog.setValue(10))
        self.view.loadProgress.connect(self.prog.setValue)
        self.view.loadFinished.connect(self._load_done)

    def _url_changed(self, url):
        s      = url.toString()
        is_h   = "cysra_home.html" in s or s in ("about:blank", "", "about:")
        self.addr.set_url(s, is_h)
        is_fav = self.store.is_favorite(s) if not is_h else False
        self.addr.set_favorite(is_fav)
        self.urlChanged.emit(s)
        if not self.secret and not is_h:
            title = self.view.title() or s
            self.store.add_history(s, title)

    def _load_done(self, ok):
        self.prog.setValue(100)
        QTimer.singleShot(300, lambda: self.prog.setValue(0))
        if not ok:
            self.view.setHtml(self._error_html())
            return
        if self._opt:
            self.page.runJavaScript(OPT_JS)
        if self.secret:
            self.page.runJavaScript(SECRET_JS)
        if "cysra_home.html" in self.view.url().toString():
            self._push_home_data()

    def _push_home_data(self):
        counts = {}
        for entry in self.store.history:
            url = entry.get("url", "")
            if url:
                counts[url] = counts.get(url, 0) + 1
        sorted_urls = sorted(counts.keys(), key=lambda u: counts[u], reverse=True)
        most_visited = []
        for url in sorted_urls[:3]:
            match = next((e for e in self.store.history if e.get("url") == url), None)
            if match:
                most_visited.append({
                    "url":   url,
                    "title": match.get("title", url),
                    "count": counts[url],
                })
        data = json.dumps({
            "favorites":    self.store.favorites,
            "most_visited": most_visited,
            "theme":        _theme,
        })
        self.page.runJavaScript(
            "(function(){window._CYSRA=" + data + ";"
            "if(typeof window.onCysraData==='function')"
            "window.onCysraData(window._CYSRA);})();"
        )

    def _navigate_from_bar(self, val):
        if not val:
            self.load_home()
            return
        if val.startswith(("http://", "https://", "file://", "view-source:")):
            url = val
        elif "." in val and " " not in val:
            url = "https://" + val
        else:
            url = "https://www.duckduckgo.com/search?q=" + val.replace(" ", "+")
        self.view.setUrl(QUrl(url))

    def _toggle_favorite(self):
        url  = self.view.url().toString()
        skip = ["cysra_home.html", "about:blank", "about:", ""]
        for pat in skip:
            if pat in url:
                return
        if self.store.is_favorite(url):
            self.store.remove_favorite(url)
            self.addr.set_favorite(False)
        else:
            title = self.view.title() or url
            self.store.add_favorite(url, title)
            self.addr.set_favorite(True)

    def _view_source(self):
        url = self.view.url().toString()
        if url and not url.startswith("view-source:"):
            self.view.setUrl(QUrl("view-source:" + url))

    def _on_opt(self, on):
        self._opt = on
        if on:
            self.page.runJavaScript(OPT_JS)

    def set_opt(self, on):
        self.opt_btn.setChecked(on)

    def load_home(self):
        if os.path.exists(HOME_HTML):
            self.view.setUrl(QUrl.fromLocalFile(HOME_HTML))
        else:
            self.view.setHtml(self._fallback_home())

    def navigate(self, url):
        self.addr.url_input.setText(url)
        self.view.setUrl(QUrl(url))

    def focus_address(self):
        self.addr.focus()

    def _fallback_home(self):
        return (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<style>*{margin:0;padding:0;box-sizing:border-box}"
            "body{background:" + p("bg") + ";color:" + p("text") + ";"
            "font-family:-apple-system,'Segoe UI',sans-serif;"
            "display:flex;flex-direction:column;align-items:center;"
            "justify-content:center;height:100vh;gap:20px;}"
            "h1{font-size:32px;font-weight:200;color:" + p("accent") + ";}"
            "p{color:" + p("text2") + ";font-size:13px;}"
            "input{background:" + p("input_bg") + ";color:" + p("text") + ";"
            "border:1px solid " + p("input_bdr") + ";border-radius:28px;"
            "padding:13px 22px;font-size:14px;width:500px;outline:none;font-family:inherit;}"
            "input:focus{border-color:" + p("accent") + ";}"
            "</style></head><body>"
            "<h1>Cysra Anome</h1>"
            "<p>Your browser. Your rules.</p>"
            "<input type='text' placeholder='Search or enter an address' id='q'"
            " onkeydown=\"if(event.key==='Enter')window.location="
            "'https://www.google.com/search?q='+encodeURIComponent(this.value)\">"
            "</body></html>"
        )

    def _error_html(self):
        return (
            "<!DOCTYPE html><html><head><meta charset='utf-8'>"
            "<style>body{background:" + p("bg") + ";color:" + p("text") + ";"
            "font-family:-apple-system,'Segoe UI',sans-serif;"
            "display:flex;flex-direction:column;align-items:center;"
            "justify-content:center;height:100vh;gap:10px;}"
            "h2{font-size:20px;font-weight:500;}p{color:" + p("text2") + ";font-size:13px;}"
            "</style></head><body>"
            "<h2>Page could not be loaded</h2>"
            "<p>Check the address or your connection and try again.</p>"
            "</body></html>"
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cysra Anome")
        self.setMinimumSize(900, 580)
        self.setGeometry(50, 50, 1440, 900)

        self.store   = DataStore()
        self._secret = False
        self._opt    = False

        self._dl_page = DownloadsPage()
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self._handle_download)

        self._build()
        self._shortcuts()
        self.setStyleSheet(build_stylesheet())
        self.add_tab()
        self.statusBar().showMessage("Ready")

    def _handle_download(self, item):
        try:
            suggested = item.path() if hasattr(item, "path") else ""
            if not suggested:
                suggested = item.downloadFileName() if hasattr(item, "downloadFileName") else "file"
            path, _ = QFileDialog.getSaveFileName(self, "Save File", suggested)
            if path:
                item.setPath(path)
                item.accept()
                dl_item = self._dl_page.add_item(os.path.basename(path))
                item.finished.connect(
                    lambda: self._dl_page.mark_done(dl_item, os.path.basename(path))
                )
                self.statusBar().showMessage("Downloading: " + os.path.basename(path), 3000)
            else:
                item.cancel()
        except Exception as exc:
            self.statusBar().showMessage("Download error: " + str(exc), 3000)

    def _build(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_lay = QHBoxLayout(central)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        self.icon_bar = IconBar(self)
        self.icon_bar.icon_clicked.connect(self._on_icon_clicked)
        main_lay.addWidget(self.icon_bar)

        self.slide_panel = SlidePanel(self.store, self._dl_page, self)
        self.slide_panel.navigate.connect(self._navigate_current)
        self.slide_panel.set_close_callback(self.icon_bar.clear_active)
        self.slide_panel.hide()
        main_lay.addWidget(self.slide_panel)

        browser_widget = QWidget()
        browser_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bw_lay = QVBoxLayout(browser_widget)
        bw_lay.setContentsMargins(0, 0, 0, 0)
        bw_lay.setSpacing(0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)

        corner   = QWidget()
        cor_lay  = QHBoxLayout(corner)
        cor_lay.setContentsMargins(0, 0, 8, 0)
        cor_lay.setSpacing(4)

        new_btn = QPushButton("+")
        new_btn.setObjectName("navBtn")
        new_btn.setFixedSize(30, 30)
        new_btn.setToolTip("New Tab  (Ctrl+T)")
        new_btn.setCursor(Qt.PointingHandCursor)
        new_btn.clicked.connect(self.add_tab)

        secret_btn = QPushButton("Secret")
        secret_btn.setObjectName("navBtn")
        secret_btn.setFixedHeight(28)
        secret_btn.setStyleSheet(
            "QPushButton#navBtn{font-size:11px;font-weight:600;"
            "min-width:52px;max-width:52px;border-radius:20px;}"
        )
        secret_btn.setToolTip("New Secret Tab  (Ctrl+Shift+N)")
        secret_btn.setCursor(Qt.PointingHandCursor)
        secret_btn.clicked.connect(lambda: self.add_tab(secret=True))

        self._theme_btn = QPushButton("Light")
        self._theme_btn.setObjectName("navBtn")
        self._theme_btn.setFixedHeight(28)
        self._theme_btn.setStyleSheet(
            "QPushButton#navBtn{font-size:11px;font-weight:600;"
            "min-width:46px;max-width:46px;border-radius:20px;}"
        )
        self._theme_btn.setToolTip("Switch Theme")
        self._theme_btn.setCursor(Qt.PointingHandCursor)
        self._theme_btn.clicked.connect(self._cycle_theme)

        for w in (new_btn, secret_btn, self._theme_btn):
            cor_lay.addWidget(w)
        self.tabs.setCornerWidget(corner, Qt.TopRightCorner)

        bw_lay.addWidget(self.tabs)
        main_lay.addWidget(browser_widget, 1)

        self.setStatusBar(QStatusBar())

    def _on_icon_clicked(self, key):
        if self.slide_panel.is_open() and self.slide_panel.current_key() == key:
            self.slide_panel.close_panel()
            self.icon_bar.clear_active()
        else:
            self.slide_panel.show_page(key)
            self.icon_bar.set_active(key)

    def _shortcuts(self):
        for seq, fn in [
            ("Ctrl+T",       self.add_tab),
            ("Ctrl+W",       lambda: self._close_tab(self.tabs.currentIndex())),
            ("Ctrl+Shift+N", lambda: self.add_tab(secret=True)),
            ("Ctrl+L",       self._focus_address),
            ("F5",           self._reload),
            ("Ctrl+R",       self._reload),
            ("Ctrl+U",       self._view_source),
            ("Alt+Left",     lambda: self._view_action("back")),
            ("Alt+Right",    lambda: self._view_action("forward")),
            ("Alt+Home",     self._go_home),
            ("Ctrl+D",       self._toggle_favorite),
            ("Ctrl+H",       lambda: self._on_icon_clicked("history")),
            ("Ctrl+J",       lambda: self._on_icon_clicked("downloads")),
        ]:
            QShortcut(QKeySequence(seq), self, fn)

    def _current_tab(self):
        t = self.tabs.currentWidget()
        return t if isinstance(t, BrowserTab) else None

    def _focus_address(self):
        t = self._current_tab()
        if t:
            t.focus_address()

    def _reload(self):
        t = self._current_tab()
        if t:
            t.view.reload()

    def _view_source(self):
        t = self._current_tab()
        if t:
            t._view_source()

    def _go_home(self):
        t = self._current_tab()
        if t:
            t.load_home()

    def _view_action(self, action):
        t = self._current_tab()
        if t:
            getattr(t.view, action)()

    def _toggle_favorite(self):
        t = self._current_tab()
        if t:
            t._toggle_favorite()

    def add_tab(self, secret=False):
        tab = BrowserTab(
            self, self.store,
            secret=(secret or self._secret),
            opt=self._opt
        )
        tab.titleChanged.connect(lambda title, ref=tab: self._update_title(ref, title))
        label = "Secret" if (secret or self._secret) else "New Tab"
        idx   = self.tabs.addTab(tab, label)
        self.tabs.setCurrentIndex(idx)
        return tab

    def _update_title(self, tab, title):
        idx = self.tabs.indexOf(tab)
        if idx < 0:
            return
        short = (title[:20] + "…") if len(title) > 20 else (title or "New Tab")
        self.tabs.setTabText(idx, short)
        if self.tabs.currentIndex() == idx:
            self.setWindowTitle(title + "  —  Cysra Anome 7.0")

    def _close_tab(self, idx):
        if self.tabs.count() <= 1:
            t = self.tabs.widget(0)
            if isinstance(t, BrowserTab):
                t.load_home()
            return
        w = self.tabs.widget(idx)
        self.tabs.removeTab(idx)
        if w:
            w.deleteLater()

    def _navigate_current(self, url):
        t = self._current_tab()
        if t:
            t.navigate(url)
        else:
            new_tab = self.add_tab()
            QTimer.singleShot(100, lambda: new_tab.navigate(url))

    def _cycle_theme(self):
        themes = list(PALETTES.keys())
        idx    = themes.index(_theme)
        next_t = themes[(idx + 1) % len(themes)]
        set_theme(next_t)
        self.setStyleSheet(build_stylesheet())
        self._theme_btn.setText("Dark" if next_t == "light" else "Light")
        self.statusBar().showMessage("Theme: " + next_t.capitalize(), 2000)
        for i in range(self.tabs.count()):
            t = self.tabs.widget(i)
            if isinstance(t, BrowserTab) and "cysra_home.html" in t.view.url().toString():
                t._push_home_data()

    def closeEvent(self, ev):
        gc.collect()
        super().closeEvent(ev)


if __name__ == "__main__":
    os.environ.setdefault(
        "QTWEBENGINE_CHROMIUM_FLAGS",
        "--disable-gpu-sandbox --no-sandbox --disable-dev-shm-usage"
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps,    True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    try:
        win = MainWindow()
        win.show()
        sys.exit(app.exec_())
    except Exception:
        traceback.print_exc()
        sys.exit(1)