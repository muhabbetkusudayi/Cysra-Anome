import sys
import os
import json
import time
import importlib.util
import traceback
import gc
import base64  
import ctypes  
from ctypes import wintypes  
from datetime import datetime
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor


class DNTInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"DNT", b"1")


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
    QEasingCurve, QAbstractAnimation, QThread
)
from PyQt5.QtGui import (
    QColor, QFont, QKeySequence, QPainter, QPainterPath, QPixmap, QIcon
)

_ICON_CACHE = {}


def get_svg_icon(path, color):
    cache_key = (path, color)
    if cache_key in _ICON_CACHE:
        return _ICON_CACHE[cache_key]

    if not os.path.exists(path):
        return QIcon()

    try:
        with open(path, "r", encoding="utf-8") as f:
            svg_data = f.read()

        if 'fill="currentColor"' in svg_data:
            svg_data = svg_data.replace('fill="currentColor"', f'fill="{color}"')
        if 'stroke="currentColor"' in svg_data:
            svg_data = svg_data.replace('stroke="currentColor"', f'stroke="{color}"')
        if 'fill="currentColor"' not in svg_data and 'stroke="currentColor"' not in svg_data:
            if "fill=" not in svg_data:
                svg_data = svg_data.replace("<svg", f'<svg fill="{color}"')
            if "stroke=" not in svg_data:
                svg_data = svg_data.replace("<svg", f'<svg stroke="{color}"')

        pm = QPixmap(QSize(64, 64))
        pm.fill(Qt.transparent)
        painter = QPainter(pm)
        painter.setRenderHint(QPainter.Antialiasing)
        from PyQt5.QtSvg import QSvgRenderer
        renderer = QSvgRenderer(svg_data.encode("utf-8"))
        renderer.render(painter)
        painter.end()

        icon = QIcon(pm)
        _ICON_CACHE[cache_key] = icon
        return icon
    except Exception:
        return QIcon()


_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_HTML = os.path.join(_DIR, "cysra_home.html")
NOTES_FILE = os.path.join(_DIR, "cysra_notes.txt")
DATA_FILE = os.path.join(_DIR, "cysra_data.json")
APPS_DIR = os.path.join(_DIR, "myapps")

PALETTES = {
    "dark": {
        "bg":             "#0b0b0e",
        "toolbar":        "rgba(26, 26, 30, 0.4)",
        "sidebar":        "rgba(19, 19, 23, 0.7)",
        "tab_strip":      "transparent",
        "tab_bg":         "transparent",
        "tab_active":     "rgba(255, 255, 255, 0.08)",
        "tab_text":       "#a0a0a5",
        "tab_active_txt": "#ffffff",
        "url_bg":         "rgba(255, 255, 255, 0.05)",
        "url_focus_bg":   "rgba(255, 255, 255, 0.1)",
        "url_focus_bdr":  "#7aa2f7",
        "btn_hover":      "rgba(255, 255, 255, 0.08)",
        "accent":         "#7aa2f7",
        "accent2":        "#9abcfc",
        "text":           "#c0caf5",
        "text2":          "#9499b8",
        "text3":          "#565f89",
        "border":         "rgba(255, 255, 255, 0.08)",
        "card":           "rgba(30, 30, 36, 0.6)",
        "icon_bar":       "transparent",
        "panel_bg":       "#131317",
        "panel_hdr":      "#1a1a1e",
        "input_bg":       "rgba(255, 255, 255, 0.05)",
        "input_bdr":      "rgba(255, 255, 255, 0.1)",
        "success":        "#9ece6a",
        "warning":        "#e0af68",
        "danger":         "#f7768e",
        "scrollbar":      "rgba(255, 255, 255, 0.1)",
        "selection":      "#364a82",
        "star_off":       "#565f89",
        "star_on":        "#e0af68",
        "tag_bg":         "rgba(122, 162, 247, 0.15)",
        "ext_colors":     ["#7aa2f7", "#9ece6a", "#f7768e", "#e0af68",
                           "#bb9af7", "#7dcfff", "#b4f9f8", "#ff9e64"],
    },
    "light": {
        "bg":             "#fdfdfe",
        "toolbar":        "rgba(255, 255, 255, 0.7)",
        "sidebar":        "rgba(255, 255, 255, 0.8)",
        "tab_strip":      "transparent",
        "tab_bg":         "transparent",
        "tab_active":     "#ffffff",
        "tab_text":       "#5f6368",
        "tab_active_txt": "#1a73e8",
        "url_bg":         "#f1f3f4",
        "url_focus_bg":   "#ffffff",
        "url_focus_bdr":  "#1a73e8",
        "btn_hover":      "rgba(0, 0, 0, 0.06)",
        "accent":         "#1a73e8",
        "accent2":        "#4285f4",
        "text":           "#202124",
        "text2":          "#5f6368",
        "text3":          "#9aa0a6",
        "border":         "rgba(0, 0, 0, 0.06)",
        "card":           "rgba(255, 255, 255, 0.8)",
        "icon_bar":       "transparent",
        "panel_bg":       "#ffffff",
        "panel_hdr":      "#f4f5f8",
        "input_bg":       "#ffffff",
        "input_bdr":      "#d8dee9",
        "success":        "#a3be8c",
        "warning":        "#ebcb8b",
        "danger":         "#bf616a",
        "scrollbar":      "rgba(0, 0, 0, 0.1)",
        "selection":      "#d8dee9",
        "star_off":       "#4c566a",
        "star_on":        "#ebcb8b",
        "tag_bg":         "rgba(94, 129, 172, 0.1)",
        "ext_colors":     ["#5e81ac", "#a3be8c", "#bf616a", "#ebcb8b",
                           "#b48ead", "#88c0d0", "#8fbcbb", "#d08770"],
    },
}

_theme = "dark"


def p(k):
    return PALETTES[_theme][k]


def set_theme(name):
    global _theme
    _theme = name


class MemoryManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.optimize)
        self.timer.start(30000)  # Perf: periodic cleanup.

    def optimize(self):
        gc.collect()  # Perf: reduce long-run memory growth.
        try:
            profile = QWebEngineProfile.defaultProfile()
            profile.clearHttpCache()  # Perf: clear cache occasionally for smoother behavior.
            profile.setHttpCacheMaximumSize(50 * 1024 * 1024)  # Perf: cap cache size.
        except Exception:
            pass


def _entropy_from_master(master_pwd):
    import hashlib  # Security: derive stable DPAPI entropy from master password.
    return hashlib.sha256((master_pwd or "").encode("utf-8")).digest()


def _dpapi_protect(plaintext_bytes, entropy):
    # Security: encrypt secrets at rest using OS-backed key storage (DPAPI).
    if plaintext_bytes is None:
        plaintext_bytes = b""

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

    def _blob_from_bytes(b):
        buf = (ctypes.c_byte * len(b)).from_buffer_copy(b)
        return DATA_BLOB(len(b), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))

    in_blob = _blob_from_bytes(plaintext_bytes)
    ent_blob = _blob_from_bytes(entropy or b"")
    out_blob = DATA_BLOB()

    if not ctypes.windll.crypt32.CryptProtectData(ctypes.byref(in_blob), None, ctypes.byref(ent_blob), None, None, 0, ctypes.byref(out_blob)):
        raise RuntimeError("CryptProtectData failed")
    try:
        out = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        return out
    finally:
        ctypes.windll.kernel32.LocalFree(out_blob.pbData)


def _dpapi_unprotect(cipher_bytes, entropy):
    # Security: decrypt secrets at rest using OS-backed key storage (DPAPI).
    if cipher_bytes is None:
        return b""

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]

    def _blob_from_bytes(b):
        buf = (ctypes.c_byte * len(b)).from_buffer_copy(b)
        return DATA_BLOB(len(b), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))

    in_blob = _blob_from_bytes(cipher_bytes)
    ent_blob = _blob_from_bytes(entropy or b"")
    out_blob = DATA_BLOB()

    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, ctypes.byref(ent_blob), None, None, 0, ctypes.byref(out_blob)):
        raise RuntimeError("CryptUnprotectData failed")
    try:
        out = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        return out
    finally:
        ctypes.windll.kernel32.LocalFree(out_blob.pbData)


def safe_eval(expr):
    # UI: provide a safe limited evaluator for internal calculator/plugin use.
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
    # UI: generate colored circle avatars for extension lists.
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
        self._is_favorite = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 12, 0)
        layout.setSpacing(8)
        
        self.sec_label = QLabel()
        self.sec_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sec_label)

        self.url_input = QLineEdit()
        self.url_input.setObjectName("urlInput")
        self.url_input.setPlaceholderText("Search or enter web address")
        self.url_input.setStyleSheet("background: transparent; border: none; padding: 0;")
        self.url_input.returnPressed.connect(
            lambda: self.navigateRequested.emit(self.url_input.text().strip())
        )
        layout.addWidget(self.url_input, 1)

        self.star_btn = QPushButton("")
        self.star_btn.setFixedSize(28, 28)
        self.star_btn.setCursor(Qt.PointingHandCursor)
        self.star_btn.clicked.connect(lambda: self.favoriteToggled.emit())
        layout.addWidget(self.star_btn)

        def on_focus_in(ev):
            self.setProperty("focused", True)
            self.style().unpolish(self)
            self.style().polish(self)
            self.url_input.selectAll()
            QLineEdit.focusInEvent(self.url_input, ev)

        def on_focus_out(ev):
            self.setProperty("focused", False)
            self.style().unpolish(self)
            self.style().polish(self)
            QLineEdit.focusOutEvent(self.url_input, ev)

        self.url_input.focusInEvent = on_focus_in
        self.url_input.focusOutEvent = on_focus_out

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
        icons_path = os.path.join(_DIR, "icons")
        if on:
            icon_file = os.path.join(icons_path, "fav.svg")
            color = p("star_on")
        else:
            icon_file = os.path.join(icons_path, "fav_outline.svg")
            color = p("star_off")
        
        if os.path.exists(icon_file):
            self.star_btn.setIcon(get_svg_icon(icon_file, color))
            self.star_btn.setIconSize(QSize(18, 18))
        else:
            self.star_btn.setText("★" if on else "☆")

        self.star_btn.setStyleSheet(
            "QPushButton#starBtn{background:transparent;border:none;border-radius:14px;}"
            "QPushButton#starBtn:hover{background:" + p("btn_hover") + ";}"
        )
        tip = "Remove from Favorites" if on else "Add to Favorites (Ctrl+D)"
        self.star_btn.setToolTip(tip)

    def focus(self):
        self.url_input.selectAll()
        self.url_input.setFocus()


class TabItemWidget(QWidget):
    closeRequested = pyqtSignal()
    
    def __init__(self, title, fav_icon=None, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(18, 18)
        self.icon_label.setScaledContents(True)
        if fav_icon:
            self.icon_label.setPixmap(fav_icon.pixmap(18, 18))
        else:
            self.icon_label.setStyleSheet("background: palette(mid); border-radius: 4px;")
        layout.addWidget(self.icon_label)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("background: transparent; border: none; font-weight: 500;")
        layout.addWidget(self.title_label, 1)
        
        self.close_btn = QPushButton()
        self.close_btn.setObjectName("tabCloseBtn")
        self.close_btn.setFixedSize(20, 20)
        close_icon = os.path.join(_DIR, "icons", "close.svg")
        if os.path.exists(close_icon):
            self.close_btn.setIcon(get_svg_icon(close_icon, p("text3")))
            self.close_btn.setIconSize(QSize(10, 10))
        else:
            self.close_btn.setText("×")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        self.close_btn.clicked.connect(self.closeRequested.emit)
        layout.addWidget(self.close_btn)

    def set_title(self, title):
        self.title_label.setText(title)
        
    def set_icon(self, icon):
        if icon:
            self.icon_label.setPixmap(icon.pixmap(18, 18))


def build_stylesheet():
    # UI: use format template to avoid accidental triple-quote termination.
    return (
        """
QWidget {{
    background: {bg};
    color: {text};
    font-family: 'Inter', -apple-system, sans-serif;
    font-size: 13px;
    outline: none;
}}
/* UI consistency: normalize common form controls so light/white mode never falls back to hard-to-read defaults */
QLineEdit, QTextEdit, QComboBox {{
    background: {input_bg};
    color: {text};
    border: 1px solid {input_bdr};
    border-radius: 16px;
    padding: 10px 12px;
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border-color: {accent};
}}
QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {text3};
}}
/* UI consistency: ensure section headers and accent buttons remain readable in white mode */
QLabel#sectionHead {{ background: transparent; color: {accent}; }}
QPushButton#accentBtn {{
    background: {accent};
    color: #ffffff;
    border: none;
    border-radius: 16px;
    font-weight: 700;
}}
QPushButton#accentBtn:hover {{ background: {accent2}; }}
QPushButton#accentBtn:pressed {{ background: {accent}; }}
QPushButton#dangerBtn {{ background: {danger}; color: #ffffff; font-weight: 700; }}
QPushButton#dangerBtn:hover {{ background: {danger}cc; }}
QLabel#mutedLabel {{ color: {text3}; background: transparent; }}
QMainWindow {{ background: {bg}; }}

QFrame#sidebar {{
    background: {sidebar};
    border-right: 1px solid {border};
}}

QFrame#tabPanel {{
    background: {sidebar};
    border-left: 1px solid {border};
    border-top-left-radius: 20px;
    border-bottom-left-radius: 20px;
}}

QWidget#tabPanelHeader {{
    background: transparent;
}}

QListWidget#tabList {{
    background: transparent;
    border: none;
    padding: 12px;
}}
QListWidget#tabList::item {{
    background: transparent;
    color: {tab_text};
    border-radius: 20px;
    margin-bottom: 4px;
    padding: 0;
}}
QListWidget#tabList::item:selected {{
    background: {tab_active};
    color: {tab_active_txt};
}}
QListWidget#tabList::item:hover:!selected {{
    background: {btn_hover};
}}

QPushButton#tabCloseBtn {{
    border-radius: 10px;
    background: transparent;
    color: {text3};
    font-size: 16px;
    padding: 0;
}}
QPushButton#tabCloseBtn:hover {{
    background: {danger};
    color: #ffffff;
}}

QFrame#toolbar {{
    background: {toolbar};
    border-bottom: 1px solid {border};
    border-radius: 24px;
    margin: 6px 10px;
}}
QFrame#iconBar {{
    background: transparent;
    border: none;
}}
QFrame#slidePanel {{
    background: {panel_bg};
    border-right: 1px solid {border};
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
}}
QFrame#panelHeader {{
    background: {panel_hdr};
    border-bottom: 1px solid {border};
}}
QFrame#card {{
    background: {card};
    border: 1px solid {border};
    border-radius: 24px;
}}
QFrame#urlFrame {{
    background: {url_bg};
    border: 1px solid transparent;
    border-radius: 24px;
}}
QFrame#urlFrame[focused="true"] {{
    border-color: {accent};
    background: {url_focus_bg};
}}

QPushButton {{
    background: transparent;
    color: {text2};
    border: none;
    border-radius: 16px;
    padding: 10px 18px;
}}
QPushButton:hover {{ background: {btn_hover}; color: {text}; }}
QPushButton:pressed {{ background: {btn_hover}; }}

QToolButton#navBtn {{
    background: transparent;
    border: none;
    border-radius: 18px;
}}
QToolButton#navBtn:hover {{ background: {btn_hover}; }}

QPushButton#iconBtn {{
    border-radius: 14px;
    background: transparent;
    color: {text3};
    padding: 0;
}}
QPushButton#iconBtn:hover {{
    background: {btn_hover};
}}
QPushButton#iconBtn[active="true"] {{
    background: {tag_bg};
    color: {accent};
    border: 1.5px solid {accent}26;
}}

QProgressBar {{ background: transparent; height: 2px; }}
QProgressBar::chunk {{ background: {accent}; }}

QScrollBar:vertical {{ background: transparent; width: 4px; }}
QScrollBar::handle:vertical {{ background: {scrollbar}; border-radius: 2px; }}

QMenu {{
    background: {card};
    border: 1px solid {border};
    border-radius: 20px;
    padding: 8px;
}}
QMenu::item {{ padding: 10px 24px; border-radius: 12px; }}
QMenu::item:selected {{ background: {btn_hover}; }}
"""
    ).format(
        bg=p("bg"),
        toolbar=p("toolbar"),
        sidebar=p("sidebar"),
        tab_active=p("tab_active"),
        tab_text=p("tab_text"),
        tab_active_txt=p("tab_active_txt"),
        url_bg=p("url_bg"),
        url_focus_bg=p("url_focus_bg"),
        btn_hover=p("btn_hover"),
        accent=p("accent"),
        accent2=p("accent2"),
        text=p("text"),
        text2=p("text2"),
        text3=p("text3"),
        border=p("border"),
        card=p("card"),
        panel_bg=p("panel_bg"),
        panel_hdr=p("panel_hdr"),
        input_bg=p("input_bg"),
        input_bdr=p("input_bdr"),
        danger=p("danger"),
        scrollbar=p("scrollbar"),
        tag_bg=p("tag_bg"),
    )


OPT_JS = """
(function(){
    if(window.__cysra__)return;
    window.__cysra__=true;
    // Perf: throttle DOM pruning to animation frames to avoid running on every mutation synchronously.
    var _sched=false;
    var prune=function(){
        document.querySelectorAll('[style*="display:none"],[style*="display: none"]').forEach(function(el){
            if(!el.id&&!el.className&&!el.children.length&&!el.innerHTML.trim())
                try{el.remove()}catch(e){}
        });
    };
    var _run=function(){_sched=false;prune();};
    var schedule=function(){if(_sched)return;_sched=true;requestAnimationFrame(_run);};
    new MutationObserver(schedule).observe(document.documentElement,{childList:true,subtree:true});
    schedule();
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
    // Relaxed security JS to avoid breaking sites
    try{navigator.sendBeacon=function(){return false;};}catch(e){}
})();
"""


class DataStore(QObject):
    changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._data = {"history": [], "favorites": [], "passwords": [], "master_pwd": None}
        self._mp_entropy = None  # Security: decryption only available after successful unlock.
        self._load()

    def _load(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, encoding="utf-8") as f:
                    self._data = json.load(f)
        except Exception:
            self._data = {"history": [], "favorites": [], "passwords": [], "master_pwd": None}

    def _save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as exc:
            print("DataStore save error:", exc)

    def add_history(self, url, title=""):
        # Perf/UI: cap history and avoid storing internal pages.
        skip_patterns = ["cysra_home.html", "about:blank", "about:", "view-source:"]
        for pat in skip_patterns:
            if pat in (url or ""):
                return
        if not url:
            return
        self._data["history"] = [e for e in self._data.get("history", []) if e.get("url") != url]
        self._data["history"].insert(0, {"url": url, "title": title or url, "ts": datetime.now().strftime("%d %b %H:%M")})
        if len(self._data["history"]) > 2000:
            self._data["history"] = self._data["history"][:2000]
        self._save()
        self.changed.emit()

    def clear_history(self):
        # UI: allow user to clear browsing history.
        self._data["history"] = []
        self._save()
        self.changed.emit()

    @property
    def history(self):
        return self._data.get("history", [])

    def add_favorite(self, url, title=""):
        # UI: store favorites used by AddressBar and home data.
        favs = self._data.setdefault("favorites", [])
        if not any(f.get("url") == url for f in favs):
            favs.append({"url": url, "title": title or url})
            self._save()
            self.changed.emit()

    def remove_favorite(self, url):
        self._data["favorites"] = [f for f in self._data.get("favorites", []) if f.get("url") != url]
        self._save()
        self.changed.emit()

    def is_favorite(self, url):
        return any(f.get("url") == url for f in self._data.get("favorites", []))

    @property
    def favorites(self):
        return self._data.get("favorites", [])

    def add_password(self, site, user, pwd):
        if not self._mp_entropy:
            return  # Security: never store/reveal passwords unless master is unlocked.
        ct = _dpapi_protect((pwd or "").encode("utf-8"), self._mp_entropy)
        enc_pwd = {"v": 1, "enc": "dpapi", "ct": base64.b64encode(ct).decode("utf-8")}  # Security: encrypted JSON payload.
        self._data.setdefault("passwords", []).append({"site": site, "user": user, "pwd": enc_pwd})
        self._save()
        self.changed.emit()

    def remove_password(self, site, user):
        self._data["passwords"] = [p for p in self._data.get("passwords", []) if not (p.get("site") == site and p.get("user") == user)]
        self._save()
        self.changed.emit()

    @property
    def passwords(self):
        if not self._mp_entropy:
            return []  # Security: do not expose stored secrets without unlocking.
        out = []
        for p_ in self._data.get("passwords", []):
            dec = ""
            try:
                blob = p_.get("pwd")
                if isinstance(blob, dict) and blob.get("enc") == "dpapi":
                    ct = base64.b64decode((blob.get("ct") or "").encode("utf-8"))
                    dec = _dpapi_unprotect(ct, self._mp_entropy).decode("utf-8", errors="replace")
                elif isinstance(blob, str):
                    dec = base64.b64decode(blob.encode("utf-8")).decode("utf-8", errors="replace")  # Security: legacy migration read.
            except Exception:
                dec = ""
            out.append({"site": p_.get("site", ""), "user": p_.get("user", ""), "pwd": dec})
        return out

    def set_master_pwd(self, pwd):
        import hashlib
        self._data["master_pwd"] = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
        self._save()

    def check_master_pwd(self, pwd):
        import hashlib
        if not self._data.get("master_pwd"):
            return True
        return hashlib.sha256(pwd.encode("utf-8")).hexdigest() == self._data["master_pwd"]

    @property
    def has_master_pwd(self):
        # Security: indicate whether a master password has been set.
        return bool(self._data.get("master_pwd"))

    def unlock_master(self, pwd):
        # Security: unlock enables decryption in memory and migrates legacy stored entries.
        if not self.check_master_pwd(pwd):
            return False
        self._mp_entropy = _entropy_from_master(pwd)
        self._migrate_passwords_if_needed()
        return True

    def lock_master(self):
        # Security: wipe in-memory decryption capability.
        self._mp_entropy = None

    def _migrate_passwords_if_needed(self):
        # Security: convert legacy base64 entries to DPAPI-encrypted payloads after successful unlock.
        if not self._mp_entropy:
            return
        changed = False
        for p_ in self._data.get("passwords", []):
            blob = p_.get("pwd")
            if isinstance(blob, dict) and blob.get("enc") == "dpapi":
                continue
            if isinstance(blob, str):
                try:
                    plain = base64.b64decode(blob.encode("utf-8")).decode("utf-8", errors="replace")
                except Exception:
                    plain = ""
                ct = _dpapi_protect(plain.encode("utf-8"), self._mp_entropy)
                p_["pwd"] = {"v": 1, "enc": "dpapi", "ct": base64.b64encode(ct).decode("utf-8")}
                changed = True
        if changed:
            self._save()


class ExtensionsPage(QWidget):
    navigate = pyqtSignal(str)

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

        store_btn = QPushButton("  Open Chrome Web Store")
        store_icon = os.path.join(_DIR, "icons", "extensions.svg")
        if os.path.exists(store_icon):
            store_btn.setIcon(get_svg_icon(store_icon, p("accent")))
            store_btn.setIconSize(QSize(16, 16))
        store_btn.setObjectName("accentBtn")
        store_btn.setCursor(Qt.PointingHandCursor)
        store_btn.setFixedHeight(36)
        store_btn.setStyleSheet(
            "QPushButton{background:" + p("tag_bg") + ";color:" + p("accent") + ";"
            "border:1px solid " + p("accent") + "40;border-radius:12px;"
            "padding:0 14px;font-size:12px;font-weight:600;text-align:left;}"
            "QPushButton:hover{background:" + p("accent") + "20;}"
        )
        store_btn.clicked.connect(lambda: self.navigate.emit("https://chromewebstore.google.com/"))
        lay.addWidget(store_btn)

        hint2 = QLabel("Extensions from Google Chrome Web Store doesnt working due to technical limitations, but you can create custom ones by putting .py files with an AppWidget class in the myapps/ folder.")
        hint2.setObjectName("mutedLabel")
        hint2.setWordWrap(True)
        hint2.setStyleSheet("font-size:10px;color:" + p("text3") + ";background:transparent;")
        lay.addWidget(hint2)

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
            hint = QLabel("Put .py files with an AppWidget class\nin the  myapps/  folder.")
            hint.setObjectName("mutedLabel")
            hint.setAlignment(Qt.AlignCenter)
            hint.setWordWrap(True)
            self._inner_lay.addWidget(hint)
        else:
            for idx, fname in enumerate(files):
                name = fname.replace(".py", "")
                color = colors[idx % len(colors)]
                path = os.path.join(APPS_DIR, fname)
                row = self._make_row(name, color, path)
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

        btn.clicked.connect(lambda _=False, p_=path, n=name, c=color: self._launch(p_, n, c))
        return btn

    def _launch(self, path, name, color):
        try:
            spec = importlib.util.spec_from_file_location("cysra_plugin", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if hasattr(mod, "AppWidget"):
                widget = mod.AppWidget()
                dlg = QDialog(self.mw, Qt.Dialog)
                dlg.setWindowTitle(name)
                dlg.setMinimumSize(400, 300)
                dlg.setStyleSheet(build_stylesheet())
                dlg_lay = QVBoxLayout(dlg)
                dlg_lay.setContentsMargins(0, 0, 0, 0)
                dlg_lay.addWidget(widget)
                dlg.show()
            else:
                QMessageBox.information(self, name, "This extension has no AppWidget class.")
        except Exception:
            QMessageBox.critical(self, "Extension Error", traceback.format_exc())


class PasswordManagerPage(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self._authed = False
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(12, 10, 12, 10)
        self.lay.setSpacing(8)

        top = QHBoxLayout()
        lbl = QLabel("Password Manager")
        lbl.setObjectName("sectionHead")
        top.addWidget(lbl)
        top.addStretch()
        ref = QPushButton("Refresh")
        ref.clicked.connect(self.refresh)
        top.addWidget(ref)
        self.lay.addLayout(top)

        self.list = QListWidget()
        self.lay.addWidget(self.list)

        self.refresh()

    def refresh(self):
        while self.lay.count():
            item = self.lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

        if not self._authed:
            self._show_auth()
        else:
            self._show_manager()

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

    def on_show(self):
        self._authed = False
        self.store.lock_master()  # Security: always re-lock secrets when page is shown.
        self.refresh()

    def _show_auth(self):
        lbl = QLabel("Password Manager")
        lbl.setObjectName("sectionHead")
        self.lay.addWidget(lbl)
        if not self.store.has_master_pwd:
            msg = QLabel("Setup a Master Password to protect your data.")
            msg.setWordWrap(True)
            self.lay.addWidget(msg)
            pwd_in = QLineEdit()
            pwd_in.setPlaceholderText("Create Master Password")
            pwd_in.setEchoMode(QLineEdit.Password)
            pwd_in.returnPressed.connect(lambda: self._setup(pwd_in.text()))
            self.lay.addWidget(pwd_in)
            btn = QPushButton("Set Password")
            btn.setObjectName("accentBtn")
            btn.clicked.connect(lambda: self._setup(pwd_in.text()))
            self.lay.addWidget(btn)
        else:
            msg = QLabel("Enter Master Password to unlock.")
            self.lay.addWidget(msg)
            pwd_in = QLineEdit()
            pwd_in.setPlaceholderText("Master Password")
            pwd_in.setEchoMode(QLineEdit.Password)
            pwd_in.returnPressed.connect(lambda: self._auth(pwd_in.text()))
            self.lay.addWidget(pwd_in)
            btn = QPushButton("Unlock")
            btn.setObjectName("accentBtn")
            btn.clicked.connect(lambda: self._auth(pwd_in.text()))
            self.lay.addWidget(btn)
        self.lay.addStretch()

    def _setup(self, pwd):
        if pwd:
            self.store.set_master_pwd(pwd)
            self._authed = self.store.unlock_master(pwd)  # Security: unlock immediately after creating master.
            self.refresh()

    def _auth(self, pwd):
        if self.store.unlock_master(pwd):
            self._authed = True
            self.refresh()
        else:
            QMessageBox.warning(self, "Auth", "Invalid Master Password")

    def _show_manager(self):
        lbl = QLabel("Passwords")
        lbl.setObjectName("sectionHead")
        self.lay.addWidget(lbl)
        self.list = QListWidget()
        for p_ in self.store.passwords:
            item = QListWidgetItem(f"{p_.get('site','')} | {p_.get('user','')}")
            item.setToolTip("Double-click to delete")
            item.setData(Qt.UserRole, (p_.get("site", ""), p_.get("user", "")))
            self.list.addItem(item)
        self.lay.addWidget(self.list)
        form = QHBoxLayout()
        self.site_in = QLineEdit()
        self.site_in.setPlaceholderText("Site")
        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("User")
        self.pwd_in = QLineEdit()
        self.pwd_in.setPlaceholderText("Pass")
        self.pwd_in.setEchoMode(QLineEdit.Password)
        add_btn = QPushButton("Add")
        add_btn.setObjectName("accentBtn")
        add_btn.clicked.connect(self._add)
        form.addWidget(self.site_in)
        form.addWidget(self.user_in)
        form.addWidget(self.pwd_in)
        form.addWidget(add_btn)
        self.lay.addLayout(form)
        hint = QLabel("Double-click to remove")
        hint.setObjectName("mutedLabel")
        hint.setAlignment(Qt.AlignCenter)
        self.lay.addWidget(hint)
        self.list.itemDoubleClicked.connect(self._remove)

    def _add(self):
        site, user, pwd = self.site_in.text(), self.user_in.text(), self.pwd_in.text()
        if site and user and pwd:
            self.store.add_password(site, user, pwd)
            self.refresh()

    def _remove(self, item):
        site, user = item.data(Qt.UserRole)
        self.store.remove_password(site, user)
        self.refresh()


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


class SettingsPage(QWidget):
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(20)

        # ── Appearance ───────────────────────────────────────────────────
        app_lbl = QLabel("Appearance")
        app_lbl.setObjectName("sectionHead")
        app_lbl.setStyleSheet(
            "font-size:10px;font-weight:800;letter-spacing:1px;"
            "color:" + p("accent") + ";background:transparent;"
        )
        lay.addWidget(app_lbl)

        theme_row = QFrame()
        theme_row.setObjectName("card")
        theme_row.setStyleSheet(
            "QFrame#card{background:" + p("card") + ";border:1px solid "
            + p("border") + ";border-radius:16px;}"
        )
        tr_lay = QVBoxLayout(theme_row)
        tr_lay.setContentsMargins(16, 12, 16, 12)
        tr_lay.setSpacing(10)

        tr_title = QLabel("Theme")
        tr_title.setStyleSheet("font-size:12px;font-weight:700;color:" + p("text") + ";background:transparent;")
        tr_lay.addWidget(tr_title)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self._dark_btn  = QPushButton("  Dark")
        self._light_btn = QPushButton("  Light")
        
        icons_path = os.path.join(_DIR, "icons")
        self._moon_icon = os.path.join(icons_path, "moon.svg")
        self._sun_icon  = os.path.join(icons_path, "sun.svg")
        
        for btn, theme_name in [(self._dark_btn, "dark"), (self._light_btn, "light")]:
            btn.setFixedHeight(38)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setIconSize(QSize(16, 16))
            btn.setCheckable(False)
            btn.clicked.connect(lambda _, t=theme_name: self.theme_changed.emit(t))
        self._update_theme_btns()

        btn_row.addWidget(self._dark_btn)
        btn_row.addWidget(self._light_btn)
        tr_lay.addLayout(btn_row)
        lay.addWidget(theme_row)

        # ── About ────────────────────────────────────────────────────────
        about_lbl = QLabel("About")
        about_lbl.setObjectName("sectionHead")
        about_lbl.setStyleSheet(
            "font-size:10px;font-weight:800;letter-spacing:1px;"
            "color:" + p("accent") + ";background:transparent;"
        )
        lay.addWidget(about_lbl)

        about_row = QFrame()
        about_row.setObjectName("card")
        about_row.setStyleSheet(
            "QFrame#card{background:" + p("card") + ";border:1px solid "
            + p("border") + ";border-radius:16px;}"
        )
        ar_lay = QVBoxLayout(about_row)
        ar_lay.setContentsMargins(16, 12, 16, 12)
        ar_lay.setSpacing(4)
        name_lbl = QLabel("Cysra Anome  7.2")
        name_lbl.setStyleSheet("font-weight:700;font-size:13px;color:" + p("text") + ";background:transparent;")
        built_lbl = QLabel("Built on PyQt5 + Chromium")
        built_lbl.setStyleSheet("font-size:11px;color:" + p("text3") + ";background:transparent;")
        ar_lay.addWidget(name_lbl)
        ar_lay.addWidget(built_lbl)
        lay.addWidget(about_row)

        lay.addStretch()

    def _update_theme_btns(self):
        active_style = (
            "background:" + p("accent") + ";color:#ffffff;"
            "border:none;border-radius:12px;font-weight:700;font-size:12px;"
            "text-align:center;padding:0 12px;"
        )
        inactive_style = (
            "background:" + p("card") + ";color:" + p("text2") + ";"
            "border:1px solid " + p("border") + ";border-radius:12px;font-size:12px;"
            "text-align:center;padding:0 12px;"
        )
        hover_style = (
            "QPushButton:hover{background:" + p("btn_hover") + ";color:" + p("text") + ";}"
            "QPushButton:pressed{background:" + p("btn_hover") + ";}"
        )
        
        self._dark_btn.setStyleSheet((active_style if _theme == "dark" else inactive_style) + hover_style)
        self._light_btn.setStyleSheet((active_style if _theme == "light" else inactive_style) + hover_style)
        
        dark_color = "#ffffff" if _theme == "dark" else p("accent")
        light_color = "#ffffff" if _theme == "light" else p("accent")
        
        if os.path.exists(self._moon_icon):
            self._dark_btn.setIcon(get_svg_icon(self._moon_icon, dark_color))
        if os.path.exists(self._sun_icon):
            self._light_btn.setIcon(get_svg_icon(self._sun_icon, light_color))

    def refresh_theme(self):
        self._update_theme_btns()


class DownloadsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._items = []
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
        clr.clicked.connect(self._clear_list)
        lay.addWidget(self.list)

    def _clear_list(self):
        self.list.clear()
        self._items.clear()

    def add_item(self, download_item):
        filename = os.path.basename(download_item.path())
        item = QListWidgetItem()
        self.list.insertItem(0, item)
        self._items.append((item, download_item))
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(5, 5, 5, 5)
        
        name_lbl = QLabel(filename)
        name_lbl.setStyleSheet("font-weight: bold;")
        layout.addWidget(name_lbl)
        
        prog = QProgressBar()
        prog.setRange(0, 100)
        prog.setValue(0)
        prog.setFixedHeight(4)
        prog.setTextVisible(False)
        layout.addWidget(prog)
        
        status_lbl = QLabel("Starting...")
        status_lbl.setStyleSheet("font-size: 10px; color: " + p("text3") + ";")
        layout.addWidget(status_lbl)
        
        item.setSizeHint(container.sizeHint())
        self.list.setItemWidget(item, container)
        
        def update_progress(received, total):
            try:
                if not prog.isVisible(): return
                if total > 0:
                    val = int((received / total) * 100)
                    prog.setValue(val)
                    status_lbl.setText(f"{val}% - {received//1024}KB / {total//1024}KB")
                else:
                    status_lbl.setText(f"{received//1024}KB downloaded")
            except RuntimeError:
                pass

        def finished():
            try:
                if not prog.isVisible(): return
                prog.setValue(100)
                prog.hide()
                status_lbl.setText("Completed")
                status_lbl.setStyleSheet("font-size: 10px; color: " + p("success") + ";")
            except RuntimeError:
                pass

        download_item.downloadProgress.connect(update_progress)
        download_item.finished.connect(finished)
        return item


class DownloadThread(QThread):
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, download_item):
        super().__init__()
        self.download_item = download_item
        self.target_path = download_item.path()

    def run(self):
        try:
            import requests
            url = self.download_item.url().toString()
            headers = {}
            
            retries = 3
            success = False
            
            while retries > 0 and not success:
                try:
                    with requests.get(url, stream=True, timeout=30, headers=headers) as r:
                        r.raise_for_status()
                        total_size = int(r.headers.get('content-length', 0))
                        downloaded = 0
                        
                        with open(self.target_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    self.progress.emit(downloaded, total_size)
                            f.flush()
                            os.fsync(f.fileno())
                        success = True
                except Exception as e:
                    retries -= 1
                    if retries == 0:
                        self.error.emit(str(e))
                        return
                    time.sleep(2)
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class IconBar(QFrame):
    icon_clicked = pyqtSignal(str)
    ITEMS = [
        ("history",  "history",    "History"),
        ("dl",       "downloads",  "Downloads"),
        ("pass",     "lock",       "Passwords"),
        ("ext",      "extensions", "Extensions"),
        ("settings", "settings",   "Settings"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("iconBar")
        self._active = None
        self._buttons = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # UI: flush sidebar.
        layout.setSpacing(0)
        layout.addStretch(1)

        inner = QWidget()
        inner.setAttribute(Qt.WA_TranslucentBackground)
        inner_lay = QVBoxLayout(inner)
        inner_lay.setContentsMargins(8, 0, 8, 0)  # UI: symmetric padding.
        inner_lay.setSpacing(4)
        inner_lay.setAlignment(Qt.AlignHCenter)

        icons_dir = os.path.join(_DIR, "icons")
        for key, svg_name, label_text in self.ITEMS:
            btn = QPushButton()
            btn.setObjectName("iconBtn")
            btn.setProperty("active", False)
            btn.setToolTip(label_text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(52, 52)
            btn.setIconSize(QSize(26, 26))

            icon_path = os.path.join(icons_dir, f"{svg_name}.svg")
            if os.path.exists(icon_path):
                btn.setIcon(get_svg_icon(icon_path, p("accent")))
            else:
                btn.setText(label_text[0])
                btn.setStyleSheet("font-size:20px; font-weight:700;")

            inner_lay.addWidget(btn, 0, Qt.AlignHCenter)
            self._buttons[key] = (btn, icon_path)
            btn.clicked.connect(lambda checked=False, k=key: self._on_click(k))

        layout.addWidget(inner, 0, Qt.AlignHCenter)
        layout.addStretch(1)

    def _on_click(self, key):
        self.icon_clicked.emit(key)

    def refresh_icons(self):
        # UI: refresh SVG icon color on theme change.
        for key, (btn, icon_path) in self._buttons.items():
            if os.path.exists(icon_path):
                btn.setIcon(get_svg_icon(icon_path, p("accent")))

    def set_active(self, key):
        self._active = key
        for k, (btn, icon_path) in self._buttons.items():
            is_active = (k == key)
            btn.setProperty("active", is_active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            if os.path.exists(icon_path):
                btn.setIcon(get_svg_icon(icon_path, p("accent")))

    def clear_active(self):
        self._active = None
        for k, (btn, icon_path) in self._buttons.items():
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            if os.path.exists(icon_path):
                btn.setIcon(get_svg_icon(icon_path, p("accent")))


class HistoryPage(QWidget):
    navigate = pyqtSignal(str)

    def __init__(self, store):
        super().__init__()
        self.store = store
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 10, 12, 10)  # UI: consistent slide-panel spacing.
        lay.setSpacing(8)

        top = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter…")
        self.search.textChanged.connect(self._filter)
        top.addWidget(self.search)

        clr = QPushButton("Clear All")
        clr.setObjectName("dangerBtn")  # UI: readable in light mode.
        clr.clicked.connect(self._clear)
        top.addWidget(clr)
        lay.addLayout(top)

        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(lambda i: self.navigate.emit(i.data(Qt.UserRole)))
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
        t = (text or "").lower()
        for i in range(self.list.count()):
            item = self.list.item(i)
            url = (item.data(Qt.UserRole) or "").lower()
            txt = (item.text() or "").lower()
            item.setHidden(bool(t) and t not in url and t not in txt)

    def _clear(self):
        reply = QMessageBox.question(
            self, "Clear History",
            "Delete all browsing history?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.store.clear_history()


class SlidePanel(QFrame):
    navigate = pyqtSignal(str)

    def __init__(self, store, downloads_page, main_window, parent=None):
        super().__init__(parent)
        self.mw = main_window
        self.setObjectName("slidePanel")
        self.setFixedWidth(0)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._header_lbl = QLabel("")
        self._header_lbl.setStyleSheet(
            "font-weight: 800; font-size: 11px; letter-spacing: 1.5px;"
            "color: " + p("accent") + "; background: transparent;"
        )
        hdr = QFrame()
        hdr.setObjectName("panelHeader")
        hdr.setFixedHeight(44)
        hdr_lay = QHBoxLayout(hdr)
        hdr_lay.setContentsMargins(16, 0, 10, 0)
        hdr_lay.setSpacing(8)
        hdr_lay.addWidget(self._header_lbl)
        hdr_lay.addStretch()
        close_btn = QPushButton()
        close_btn.setFixedSize(28, 28)
        close_icon_path = os.path.join(_DIR, "icons", "close.svg")
        if os.path.exists(close_icon_path):
            close_btn.setIcon(get_svg_icon(close_icon_path, p("accent")))
            close_btn.setIconSize(QSize(14, 14))
        else:
            close_btn.setText("✕")
        close_btn.setStyleSheet(
            "QPushButton{background:transparent;color:" + p("text2") + ";"
            "border:none;border-radius:14px;font-size:13px;}"
            "QPushButton:hover{background:" + p("btn_hover") + ";color:" + p("text") + ";}"
        )
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self._request_close)
        hdr_lay.addWidget(close_btn)
        outer.addWidget(hdr)

        self.stack = QStackedWidget()
        outer.addWidget(self.stack, 1)

        self._hist_page = HistoryPage(store)
        self._dl_page   = downloads_page
        self._pass_page = PasswordManagerPage(store)
        self._ext_page  = ExtensionsPage(main_window)
        self._tr_page   = TranslatePage()
        self._note_page = NotesPage()
        self._set_page  = SettingsPage()

        self._pages = {
            "history":   (self._hist_page, "History"),
            "dl":        (self._dl_page,   "Downloads"),
            "pass":      (self._pass_page, "Passwords"),
            "ext":       (self._ext_page,  "Extensions"),
            "translate": (self._tr_page,   "Translate"),
            "notes":     (self._note_page, "Notes"),
            "settings":  (self._set_page,  "Settings"),
        }

        for page, _ in self._pages.values():
            self.stack.addWidget(page)

        self._hist_page.navigate.connect(self.navigate)
        self._ext_page.navigate.connect(self.navigate)
        self._set_page.theme_changed.connect(self._apply_theme)

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
        if hasattr(page, "on_show"):
            page.on_show()
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

    def _apply_theme(self, theme_name):
        self.mw._set_theme(theme_name)
        if hasattr(self, "_set_page"):
            self._set_page.refresh_theme()


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
        if self.secret:
            profile = QWebEngineProfile(self)
        else:
            profile = QWebEngineProfile.defaultProfile()

        self.page = SecurePage(profile, self)
        self.view = QWebEngineView(self)
        self.view.setPage(self.page)
        self.view.page().fullScreenRequested.connect(self._handle_fullscreen)
        if self.secret:
            profile.downloadRequested.connect(self.mw._handle_download)
        else:
            profile.downloadRequested.connect(self.mw._handle_download)

        s = self.view.settings()
        s.setAttribute(QWebEngineSettings.JavascriptEnabled,               True)
        s.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls,   True)
        s.setAttribute(QWebEngineSettings.AutoLoadImages,                  True)
        s.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows,        True)
        s.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard,    True)
        s.setAttribute(QWebEngineSettings.LinksIncludedInFocusChain,       True)
        s.setAttribute(QWebEngineSettings.FocusOnNavigationEnabled,        True)
        s.setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture,    False)
        s.setAttribute(QWebEngineSettings.FullScreenSupportEnabled,        True)
        s.setAttribute(QWebEngineSettings.LocalStorageEnabled,             True)
        s.setAttribute(QWebEngineSettings.PluginsEnabled,                  True)
        s.setAttribute(QWebEngineSettings.ScrollAnimatorEnabled,           True)
        s.setAttribute(QWebEngineSettings.ErrorPageEnabled,                True)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        bar = QFrame()
        bar.setObjectName("toolbar")
        bar.setFixedHeight(48)
        bl  = QHBoxLayout(bar)
        bl.setContentsMargins(8, 0, 8, 0)
        bl.setSpacing(4)

        icons_path = os.path.join(_DIR, "icons")

        nav_items = [
            ("back",    "back.svg",    self.view.back),
            ("forward", "forward.svg", self.view.forward),
            ("reload",  "reload.svg",  self.view.reload),
            ("home",    "home.svg",    self.load_home),
        ]
        self._nav_btns = {}  # key -> (btn, icon_path)
        for key, icon_name, fn in nav_items:
            btn = QToolButton()
            btn.setObjectName("navBtn")
            btn.setFixedSize(32, 32)
            btn.setCursor(Qt.PointingHandCursor)
            icon_file = os.path.join(icons_path, icon_name)
            if os.path.exists(icon_file):
                btn.setIcon(get_svg_icon(icon_file, p("accent")))
            else:
                btn.setText(key[0].upper())
            btn.clicked.connect(fn)
            bl.addWidget(btn)
            self._nav_btns[key] = (btn, icon_file)

        self.addr = AddressBar(self)
        self.addr.navigateRequested.connect(self.navigate)
        self.addr.favoriteToggled.connect(self._toggle_favorite)
        bl.addWidget(self.addr, 1)

        self.code_btn = QToolButton()
        self.code_btn.setObjectName("navBtn")
        self.code_btn.setFixedSize(32, 32)
        btn_icon = os.path.join(icons_path, "code.svg")
        if os.path.exists(btn_icon):
            self.code_btn.setIcon(get_svg_icon(btn_icon, p("accent")))
        self.code_btn.clicked.connect(self._view_source)
        bl.addWidget(self.code_btn)

        self.opt_btn = QToolButton()
        self.opt_btn.setObjectName("navBtn")
        self.opt_btn.setFixedSize(32, 32)
        opt_icon = os.path.join(icons_path, "opt.svg")
        if os.path.exists(opt_icon):
            self.opt_btn.setIcon(get_svg_icon(opt_icon, p("accent")))
        self.opt_btn.setCheckable(True)
        self.opt_btn.toggled.connect(self._on_opt)
        bl.addWidget(self.opt_btn)

        self.dl_btn = QToolButton()
        self.dl_btn.setObjectName("navBtn")
        self.dl_btn.setFixedSize(32, 32)
        dl_icon = os.path.join(icons_path, "downloads.svg")
        if os.path.exists(dl_icon):
            self.dl_btn.setIcon(get_svg_icon(dl_icon, p("accent")))
        self.dl_btn.setToolTip("Downloads  (Ctrl+J)")
        self.dl_btn.clicked.connect(lambda: self.mw._on_icon_clicked("dl"))
        bl.addWidget(self.dl_btn)

        root.addWidget(bar)

        self.prog = QProgressBar()
        self.prog.setFixedHeight(3)
        self.prog.setTextVisible(False)
        self.prog.setRange(0, 100)
        self.prog.setValue(0)
        root.addWidget(self.prog)

        root.addWidget(self.view, 1)

        self.view.urlChanged.connect(self._url_changed)
        self.view.titleChanged.connect(self.titleChanged)
        self.view.loadStarted.connect(lambda: self.prog.setValue(10))
        self.view.loadProgress.connect(self.prog.setValue)
        self.view.loadFinished.connect(self._load_done)

    def _refresh_icons(self):
        """Re-render all toolbar SVG icons with current theme colors."""
        icons_path = os.path.join(_DIR, "icons")
        for key, (btn, icon_file) in self._nav_btns.items():
            if os.path.exists(icon_file):
                btn.setIcon(get_svg_icon(icon_file, p("accent")))
                btn.setIconSize(QSize(18, 18))
        for btn, svg_name in [
            (self.code_btn, "code.svg"),
            (self.opt_btn,  "opt.svg"),
            (self.dl_btn,   "downloads.svg"),
        ]:
            icon_file = os.path.join(icons_path, svg_name)
            if os.path.exists(icon_file):
                btn.setIcon(get_svg_icon(icon_file, p("accent")))
                btn.setIconSize(QSize(18, 18))

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
        
        # Ensure DOM events are properly dispatched for interactive elements
        self.page.runJavaScript("""
            (function() {
                if (window.__cysra_patch_applied) return;
                window.__cysra_patch_applied = true;
                
                document.addEventListener('click', function(e) {
                    let target = e.target;
                    while (target && target !== document) {
                        if (target.tagName === 'BUTTON' || target.tagName === 'A' || target.onclick || target.getAttribute('role') === 'button') {
                            // Ensure the event propagates correctly if it's a dynamic element
                            if (!e.isTrusted) return; 
                        }
                        target = target.parentNode;
                    }
                }, true);
            })();
        """)

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
        if not url: return
        if not url.startswith(("http://", "https://", "file://", "view-source:")):
            if "." in url and " " not in url:
                url = "https://" + url
            else:
                url = "https://www.google.com/search?q=" + url.replace(" ", "+")
        self.addr.url_input.setText(url)
        self.view.setUrl(QUrl(url))

    def _handle_fullscreen(self, request):
        request.accept()
        if request.toggleOn():
            self.mw.showFullScreen()
        else:
            self.mw.showNormal()

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
        self.setWindowTitle("Cysra Anome 7.2 Biscuit")
        self.setMinimumSize(1000, 650)
        self.setGeometry(50, 50, 1440, 900)

        self.store = DataStore()
        self._secret = False
        self._opt = False

        self._dl_page = DownloadsPage()
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self._handle_download)

        self.memory_manager = MemoryManager(self)

        self._build()
        self._shortcuts()
        self.setStyleSheet(build_stylesheet())
        self.add_tab()
        self._load_extensions()

    def _handle_download(self, item):
        try:
            suggested = item.path() if hasattr(item, "path") else ""
            if not suggested:
                suggested = item.downloadFileName() if hasattr(item, "downloadFileName") else "file"
            path, _ = QFileDialog.getSaveFileName(self, "Save File", suggested)
            if path:
                item.setPath(path)
                item.accept()
                
                dl_item = self._dl_page.add_item(item)
                
                thread = DownloadThread(item)
                item._thread = thread
                
                container = self._dl_page.list.itemWidget(dl_item)
                prog = container.findChild(QProgressBar)
                status_lbl = container.findChildren(QLabel)[1]
                
                def on_progress(received, total):
                    if total > 0:
                        val = int((received / total) * 100)
                        prog.setValue(val)
                        status_lbl.setText(f"{val}% - {received//1024}KB / {total//1024}KB")
                    else:
                        status_lbl.setText(f"{received//1024}KB downloaded")
                
                def on_finished():
                    prog.setValue(100)
                    prog.hide()
                    status_lbl.setText("Completed")
                    status_lbl.setStyleSheet("font-size: 10px; color: " + p("success") + ";")
                
                def on_error(err):
                    status_lbl.setText(f"Error: {err}")
                    status_lbl.setStyleSheet("font-size: 10px; color: " + p("danger") + ";")

                thread.progress.connect(on_progress)
                thread.finished.connect(on_finished)
                thread.error.connect(on_error)
                thread.start()
            else:
                item.cancel()
        except Exception:
            pass

    def _build(self):
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self._on_tab_switched)

        central = QWidget()
        self.setCentralWidget(central)
        main_lay = QHBoxLayout(central)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        # ── LEFT PANEL: Icon buttons only, big & centered ──────────────
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(76)
        side_lay = QVBoxLayout(self.sidebar)
        side_lay.setContentsMargins(0, 0, 0, 0)
        side_lay.setSpacing(0)

        self.icon_bar = IconBar(self)
        self.icon_bar.icon_clicked.connect(self._on_icon_clicked)
        side_lay.addWidget(self.icon_bar, 1)

        main_lay.addWidget(self.sidebar)

        # ── SLIDE PANEL (panel that slides in from left) ───────────────
        self.slide_panel = SlidePanel(self.store, self._dl_page, self)
        self.slide_panel.navigate.connect(self._navigate_current)
        self.slide_panel.set_close_callback(self.icon_bar.clear_active)
        self.slide_panel.hide()
        main_lay.addWidget(self.slide_panel)

        # ── CENTER: Browser tabs ───────────────────────────────────────
        main_lay.addWidget(self.tabs, 1)

        # ── RIGHT PANEL: Tab list + New Tab button ─────────────────────
        self.tab_panel = QFrame()
        self.tab_panel.setObjectName("tabPanel")
        self.tab_panel.setFixedWidth(220)
        tp_lay = QVBoxLayout(self.tab_panel)
        tp_lay.setContentsMargins(0, 0, 0, 0)
        tp_lay.setSpacing(0)

        # Header row: label + new tab button
        hdr_w = QWidget()
        hdr_w.setObjectName("tabPanelHeader")
        hdr_w.setFixedHeight(52)
        hdr_lay = QHBoxLayout(hdr_w)
        hdr_lay.setContentsMargins(16, 0, 10, 0)
        hdr_lay.setSpacing(8)

        logo = QLabel("ANOME 7.2")
        logo.setStyleSheet(
            "font-weight:800;font-size:14px;letter-spacing:2px;"
            "color:" + p("accent") + ";background:transparent;"
        )
        hdr_lay.addWidget(logo)
        hdr_lay.addStretch()

        self.new_btn = QToolButton()
        self.new_btn.setObjectName("navBtn")
        self.new_btn.setFixedSize(32, 32)
        self.new_btn.setIconSize(QSize(16, 16))
        plus_icon = os.path.join(_DIR, "icons", "plus.svg")
        if os.path.exists(plus_icon):
            self.new_btn.setIcon(get_svg_icon(plus_icon, p("accent")))
        else:
            self.new_btn.setText("+")
            self.new_btn.setStyleSheet("font-size:18px;font-weight:300;")
        self.new_btn.setCursor(Qt.PointingHandCursor)
        self.new_btn.setToolTip("New Tab  (Ctrl+T)")
        self.new_btn.clicked.connect(self.add_tab)
        hdr_lay.addWidget(self.new_btn)

        tp_lay.addWidget(hdr_w)

        # Divider
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("background:" + p("border") + ";max-height:1px;border:none;")
        tp_lay.addWidget(div)

        self.tab_list = QListWidget()
        self.tab_list.setObjectName("tabList")
        self.tab_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tab_list.currentRowChanged.connect(self.tabs.setCurrentIndex)
        tp_lay.addWidget(self.tab_list, 1)

        main_lay.addWidget(self.tab_panel)

    def _on_tab_switched(self, idx):
        self.tab_list.blockSignals(True)
        self.tab_list.setCurrentRow(idx)
        self.tab_list.blockSignals(False)
        tab = self.tabs.widget(idx)
        if isinstance(tab, BrowserTab):
            self.setWindowTitle(tab.view.title() + "  —  Cysra Anome 7.2 Biscuit")

    def add_tab(self, secret=False):
        tab = BrowserTab(self, self.store, secret=(secret or self._secret), opt=self._opt)
        tab.titleChanged.connect(lambda title, ref=tab: self._update_tab_ui(ref, title))
        idx = self.tabs.addTab(tab, "New Tab")
        item = QListWidgetItem(self.tab_list)
        item.setSizeHint(QSize(0, 48))
        tw = TabItemWidget("New Tab")
        tw.closeRequested.connect(lambda: self._close_tab(self.tabs.indexOf(tab)))
        self.tab_list.addItem(item)
        self.tab_list.setItemWidget(item, tw)
        self.tabs.setCurrentIndex(idx)
        return tab

    def _update_tab_ui(self, tab, title):
        idx = self.tabs.indexOf(tab)
        if idx >= 0:
            item = self.tab_list.item(idx)
            if item:
                tw = self.tab_list.itemWidget(item)
                if tw:
                    tw.set_title(title if title else "New Tab")
            if self.tabs.currentIndex() == idx:
                self.setWindowTitle((title if title else "New Tab") + "  —  Cysra Anome 7.2 Biscuit")

    def _close_tab(self, idx):
        if self.tabs.count() <= 1:
            return
        w = self.tabs.widget(idx)
        self.tabs.removeTab(idx)
        self.tab_list.takeItem(idx)
        if w:
            w.deleteLater()

    def _load_extensions(self):
        extensions_dir = os.path.join(_DIR, "extensions")
        if not os.path.exists(extensions_dir):
            os.makedirs(extensions_dir)
        for ext_name in os.listdir(extensions_dir):
            ext_path = os.path.join(extensions_dir, ext_name)
            if os.path.isdir(ext_path):
                QWebEngineProfile.defaultProfile().installExtension(ext_path)

    def _on_icon_clicked(self, key):
        if self.slide_panel.is_open() and self.slide_panel.current_key() == key:
            self.slide_panel.close_panel()
            self.icon_bar.clear_active()
        else:
            self.slide_panel.show_page(key)
            self.icon_bar.set_active(key)

    def _cycle_theme(self):
        themes = list(PALETTES.keys())
        idx    = themes.index(_theme)
        next_t = themes[(idx + 1) % len(themes)]
        self._set_theme(next_t)

    def _set_theme(self, theme_name):
        set_theme(theme_name)
        self.setStyleSheet(build_stylesheet())
        # Refresh all SVG icons in the icon bar with new theme colors
        self.icon_bar.refresh_icons()
        # Refresh the slide panel header label color
        if hasattr(self, "slide_panel"):
            lbl = self.slide_panel._header_lbl
            lbl.setStyleSheet(
                "font-weight: 800; font-size: 11px; letter-spacing: 1.5px;"
                "color: " + p("accent") + "; background: transparent;"
            )
        # Refresh nav button icons in all tabs
        for i in range(self.tabs.count()):
            t = self.tabs.widget(i)
            if isinstance(t, BrowserTab):
                t._refresh_icons()
                if "cysra_home.html" in t.view.url().toString():
                    t._push_home_data()

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
            ("Ctrl+J",       lambda: self._on_icon_clicked("dl")),
        ]:
            QShortcut(QKeySequence(seq), self, fn)

    def _current_tab(self):
        idx = self.tabs.currentIndex()
        if idx < 0: return None
        t = self.tabs.widget(idx)
        return t if isinstance(t, BrowserTab) else None

    def _focus_address(self):
        t = self._current_tab()
        if t: t.focus_address()

    def _reload(self):
        t = self._current_tab()
        if t: t.view.reload()

    def _view_source(self):
        t = self._current_tab()
        if t: t._view_source()

    def _go_home(self):
        t = self._current_tab()
        if t: t.load_home()

    def _view_action(self, action):
        t = self._current_tab()
        if t: getattr(t.view, action)()

    def _toggle_favorite(self):
        t = self._current_tab()
        if t: t._toggle_favorite()

    def _navigate_current(self, url):
        t = self._current_tab()
        if t: t.navigate(url)
        else:
            new_tab = self.add_tab()
            QTimer.singleShot(100, lambda: new_tab.navigate(url))

    def closeEvent(self, ev):
        gc.collect()
        super().closeEvent(ev)


if __name__ == "__main__":
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