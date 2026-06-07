#!/usr/bin/env python3
"""
NeuroSync Desktop Agent - GUI
Run this instead of agent/main.py to get the dashboard window + system tray.
"""

import sys
import os
import threading
import asyncio
import logging
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QSystemTrayIcon, QMenu, QFrame, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap

# Add agent folder to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agent"))

from connection.websocket_client import WebSocketClient
from connection.device_info import get_device_info

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("neurosync_gui")

# ─── Qt Signals (thread-safe bridge) ────────────────────────
class AgentSignals(QObject):
    log        = pyqtSignal(str)
    status     = pyqtSignal(str)   # "Connected" | "Connecting..." | "Disconnected"
    command    = pyqtSignal(str)
    stats      = pyqtSignal(dict)

signals = AgentSignals()

# ─── Logging handler that emits to GUI ──────────────────────
class QtLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        signals.log.emit(msg)

qt_handler = QtLogHandler()
qt_handler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s", "%H:%M:%S"))
logging.getLogger().addHandler(qt_handler)

# ─── System stats ───────────────────────────────────────────
def get_stats() -> dict:
    import time
    cpu  = psutil.cpu_percent(interval=0.3)
    ram  = psutil.virtual_memory()
    disk = psutil.disk_usage("C:\\" if sys.platform == "win32" else "/")
    up   = int(time.time() - psutil.boot_time())
    return {
        "cpu":      round(cpu),
        "ram":      round(ram.percent),
        "ramUsed":  round(ram.used  / 1024**3, 1),
        "ramTotal": round(ram.total / 1024**3, 1),
        "disk":     round(disk.percent),
        "diskUsed": round(disk.used  / 1024**3),
        "diskTotal":round(disk.total / 1024**3),
        "uptime":   f"{up//3600}h {(up%3600)//60}m",
        "processes":len(psutil.pids()),
    }

# ─── Agent thread ────────────────────────────────────────────
def run_agent(url: str):
    async def _run():
        while True:
            try:
                signals.status.emit("Connecting...")
                client = WebSocketClient(url=url)
                signals.status.emit("Connected")
                await client.start()
            except Exception as e:
                signals.status.emit("Disconnected")
                logger.error(f"Agent error: {e}")
                await asyncio.sleep(5)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_run())

# ─── Stat card helper ────────────────────────────────────────
def make_card(label: str, color: str):
    frame = QFrame()
    frame.setObjectName("card")
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(14, 10, 14, 10)
    lbl = QLabel(label)
    lbl.setStyleSheet(f"color: #888; font-size: 11px; font-weight: bold;")
    val = QLabel("--")
    val.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold;")
    bar = QProgressBar()
    bar.setRange(0, 100)
    bar.setValue(0)
    bar.setTextVisible(False)
    bar.setFixedHeight(6)
    bar.setStyleSheet(f"""
        QProgressBar {{ background: #2A2A2A; border: none; border-radius: 3px; }}
        QProgressBar::chunk {{ background: {color}; border-radius: 3px; }}
    """)
    layout.addWidget(lbl)
    layout.addWidget(val)
    layout.addWidget(bar)
    return frame, val, bar

# ─── Main Window ────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self, backend_url: str, device_info: dict):
        super().__init__()
        self.backend_url  = backend_url
        self.device_info  = device_info
        self.setWindowTitle("NeuroSync Desktop Agent")
        self.setMinimumSize(720, 560)
        self.setStyleSheet("""
            QMainWindow, QWidget { background: #121212; color: #FFF; font-family: 'Segoe UI', Arial; }
            QFrame#card { background: #1E1E1E; border-radius: 12px; border: 1px solid #2A2A2A; }
            QPushButton {
                background: #1E1E1E; color: #00FF66;
                border: 1px solid #00FF66; border-radius: 8px;
                padding: 8px 16px; font-size: 13px;
            }
            QPushButton:hover { background: #00FF66; color: #000; }
            QPushButton#danger { color: #FF4444; border-color: #FF4444; }
            QPushButton#danger:hover { background: #FF4444; color: #FFF; }
            QTextEdit {
                background: #0A0A0A; color: #00FF66;
                border: 1px solid #1E1E1E; border-radius: 8px;
                font-family: Consolas, monospace; font-size: 12px; padding: 8px;
            }
            QLabel { color: #FFF; }
        """)
        self._build_ui()
        self._setup_tray()
        self._connect_signals()
        QTimer.singleShot(500, self._start_stats_timer)

    # ── UI ──────────────────────────────────────────────────
    def _build_ui(self):
        w = QWidget()
        self.setCentralWidget(w)
        root = QVBoxLayout(w)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        # Header
        hdr = QHBoxLayout()
        title = QLabel("🧠 NeuroSync")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #00FF66;")
        hdr.addWidget(title)
        hdr.addStretch()
        self.status_lbl = QLabel("⚪ Disconnected")
        self.status_lbl.setStyleSheet("color: #888; font-size: 13px;")
        hdr.addWidget(self.status_lbl)
        root.addLayout(hdr)

        # Device info
        info_lbl = QLabel(
            f"🖥  {self.device_info.get('hostname','PC')}  •  "
            f"{self.device_info.get('os','')} {self.device_info.get('os_version','')}  •  "
            f"ID: {self.device_info.get('device_id','')}"
        )
        info_lbl.setStyleSheet("color: #555; font-size: 12px;")
        root.addWidget(info_lbl)

        # Stat cards
        row = QHBoxLayout()
        row.setSpacing(10)
        self.cpu_card  = make_card("CPU",    "#00FF66")
        self.ram_card  = make_card("RAM",    "#1E90FF")
        self.disk_card = make_card("DISK",   "#FFA500")
        self.up_card   = make_card("UPTIME", "#AA88FF")
        for card, _, __ in [self.cpu_card, self.ram_card, self.disk_card, self.up_card]:
            row.addWidget(card)
        root.addLayout(row)

        # Last command
        cmd_frame = QFrame()
        cmd_frame.setObjectName("card")
        cmd_row = QHBoxLayout(cmd_frame)
        cmd_row.setContentsMargins(16, 10, 16, 10)
        cmd_row.addWidget(QLabel("Last command:"))
        self.cmd_lbl = QLabel("—")
        self.cmd_lbl.setStyleSheet("color: #00FF66; font-size: 13px;")
        cmd_row.addWidget(self.cmd_lbl)
        cmd_row.addStretch()
        root.addWidget(cmd_frame)

        # Log
        log_hdr = QLabel("Activity Log")
        log_hdr.setStyleSheet("color: #888; font-size: 12px; font-weight: bold;")
        root.addWidget(log_hdr)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        root.addWidget(self.log)

        # Buttons
        btns = QHBoxLayout()
        clear = QPushButton("Clear Log")
        clear.clicked.connect(self.log.clear)
        hide = QPushButton("Minimize to Tray")
        hide.clicked.connect(self.hide)
        quit_btn = QPushButton("Quit")
        quit_btn.setObjectName("danger")
        quit_btn.clicked.connect(QApplication.quit)
        btns.addWidget(clear)
        btns.addWidget(hide)
        btns.addStretch()
        btns.addWidget(quit_btn)
        root.addLayout(btns)

    def _setup_tray(self):
        px = QPixmap(32, 32)
        px.fill(QColor("#00FF66"))
        self.tray = QSystemTrayIcon(QIcon(px), self)
        self.tray.setToolTip("NeuroSync Agent")
        menu = QMenu()
        menu.setStyleSheet("background:#1E1E1E; color:white;")
        menu.addAction("Show", self.show)
        menu.addSeparator()
        menu.addAction("Quit", QApplication.quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(
            lambda r: self.show() if r == QSystemTrayIcon.ActivationReason.DoubleClick else None
        )
        self.tray.show()

    def _connect_signals(self):
        signals.log.connect(self._append_log)
        signals.status.connect(self._set_status)
        signals.command.connect(lambda c: self.cmd_lbl.setText(c))

    def _start_stats_timer(self):
        self._timer = QTimer()
        self._timer.timeout.connect(self._refresh_stats)
        self._timer.start(3000)
        self._refresh_stats()

    # ── Slots ────────────────────────────────────────────────
    def _append_log(self, text):
        self.log.append(text)
        sb = self.log.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _set_status(self, status):
        dot   = {"Connected": "🟢", "Connecting...": "🟡"}.get(status, "⚪")
        color = {"Connected": "#00FF66", "Connecting...": "#FFA500"}.get(status, "#888")
        self.status_lbl.setText(f"{dot} {status}")
        self.status_lbl.setStyleSheet(f"color: {color}; font-size: 13px;")

    def _refresh_stats(self):
        s = get_stats()
        for (_, val, bar), key in [
            (self.cpu_card,  "cpu"),
            (self.ram_card,  "ram"),
            (self.disk_card, "disk"),
        ]:
            val.setText(f"{s[key]}%")
            bar.setValue(s[key])
        up_val = self.up_card[1]
        up_val.setText(s["uptime"])

    def closeEvent(self, e):
        e.ignore()
        self.hide()
        self.tray.showMessage("NeuroSync", "Running in system tray.", QSystemTrayIcon.MessageIcon.Information, 2000)


# ─── Entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

    url         = os.getenv("BACKEND_WS_URL", "ws://localhost:8000/ws")
    device_info = get_device_info()

    app    = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow(backend_url=url, device_info=device_info)
    window.show()

    # Start agent in background thread
    t = threading.Thread(target=run_agent, args=(url,), daemon=True)
    t.start()

    sys.exit(app.exec())