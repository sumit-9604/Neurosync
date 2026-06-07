"""
NeuroSync Desktop Agent — JARVIS HUD Theme
Full PyQt6 redesign matching the cyan-on-black Iron Man aesthetic.
"""

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStackedWidget, QFrame, QScrollArea,
    QTextEdit, QLineEdit, QProgressBar, QGridLayout, QSizePolicy,
    QGraphicsOpacityEffect
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QPointF,
    QRectF, QThread, pyqtSignal, QObject, QSize
)
from PyQt6.QtGui import (
    QColor, QPainter, QPen, QBrush, QFont, QFontDatabase,
    QLinearGradient, QPainterPath, QPolygonF, QPalette, QIcon,
    QRadialGradient, QConicalGradient
)
import random


# ─── THEME CONSTANTS ──────────────────────────────────────────────────────────

class Theme:
    BG         = QColor("#060d12")
    BG_CARD    = QColor("#0a1820")
    BG_PANEL   = QColor("#0d1f2d")
    CYAN       = QColor("#00FFFF")
    CYAN_DIM   = QColor("#00AAAA")
    CYAN_DARK  = QColor("#003344")
    AMBER      = QColor("#FFAA00")
    RED        = QColor("#FF4444")
    GREEN      = QColor("#00FF88")
    WHITE      = QColor("#E0F8FF")
    TEXT_SEC   = QColor("#4A8FA0")
    BORDER     = QColor("#0F3344")

    FONT_HUD  = "Share Tech Mono"
    FONT_UI   = "Rajdhani"
    FONT_FALL = "Courier New"


def hud_font(size=12, bold=False):
    f = QFont(Theme.FONT_HUD, size)
    if bold:
        f.setBold(True)
    if not QFontDatabase.families().__contains__(Theme.FONT_HUD):
        f = QFont(Theme.FONT_FALL, size)
    return f


def ui_font(size=13, bold=False):
    f = QFont(Theme.FONT_UI, size)
    if bold:
        f.setBold(True)
    if not QFontDatabase.families().__contains__(Theme.FONT_UI):
        f = QFont("Arial", size)
    return f


# ─── REUSABLE HUD WIDGETS ─────────────────────────────────────────────────────

class CornerBracket(QWidget):
    """Draws corner bracket decorations on a widget."""
    def __init__(self, parent=None, size=20, thickness=2, color=None):
        super().__init__(parent)
        self.sz = size
        self.thick = thickness
        self.color = color or Theme.CYAN
        self.setFixedSize(parent.size() if parent else QSize(400, 300))
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(self.color, self.thick)
        p.setPen(pen)
        w, h = self.width(), self.height()
        s = self.sz
        # top-left
        p.drawLine(0, s, 0, 0); p.drawLine(0, 0, s, 0)
        # top-right
        p.drawLine(w - s, 0, w, 0); p.drawLine(w, 0, w, s)
        # bottom-left
        p.drawLine(0, h - s, 0, h); p.drawLine(0, h, s, h)
        # bottom-right
        p.drawLine(w - s, h, w, h); p.drawLine(w, h - s, w, h)
        p.end()


class ArcRing(QWidget):
    """Circular arc progress ring with tick marks."""
    def __init__(self, label="CPU", value=0, color=None, parent=None, size=120):
        super().__init__(parent)
        self._value = value
        self.label = label
        self.color = color or Theme.CYAN
        self.setFixedSize(size, size)
        self._anim_value = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def set_value(self, v):
        self._value = max(0, min(100, v))

    def _tick(self):
        diff = self._value - self._anim_value
        self._anim_value += diff * 0.08
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        r = min(w, h) / 2 - 10

        # background arc
        pen = QPen(Theme.CYAN_DARK, 4)
        p.setPen(pen)
        p.drawEllipse(QPointF(cx, cy), r, r)

        # tick marks
        tick_pen = QPen(self.color, 1)
        tick_pen.setColor(QColor(self.color.red(), self.color.green(), self.color.blue(), 60))
        p.setPen(tick_pen)
        for i in range(60):
            angle = math.radians(i * 6 - 90)
            inner = r - (4 if i % 5 == 0 else 2)
            x1 = cx + inner * math.cos(angle)
            y1 = cy + inner * math.sin(angle)
            x2 = cx + r * math.cos(angle)
            y2 = cy + r * math.sin(angle)
            p.drawLine(QPointF(x1, y1), QPointF(x2, y2))

        # value arc
        span = int(self._anim_value / 100 * 360 * 16)
        arc_pen = QPen(self.color, 4)
        arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        p.setPen(arc_pen)
        rect = QRectF(cx - r, cy - r, r * 2, r * 2)
        p.drawArc(rect, 90 * 16, -span)

        # center text
        p.setPen(QPen(self.color))
        p.setFont(hud_font(14, bold=True))
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(self._anim_value)}%")

        # label below center
        label_rect = QRectF(cx - r, cy + 10, r * 2, 20)
        p.setFont(ui_font(9))
        p.setPen(QPen(Theme.TEXT_SEC))
        p.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, self.label)

        p.end()


class HudCard(QFrame):
    """A card with corner brackets and left-side accent bar."""
    def __init__(self, parent=None, accent=None):
        super().__init__(parent)
        self.accent = accent or Theme.CYAN
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_CARD.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 4px;
            }}
        """)

    def paintEvent(self, e):
        super().paintEvent(e)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # left accent bar
        pen = QPen(self.accent, 3)
        p.setPen(pen)
        p.drawLine(0, 8, 0, self.height() - 8)

        # corner brackets
        s = 10
        pen2 = QPen(self.accent, 1)
        p.setPen(pen2)
        w, h = self.width(), self.height()
        p.drawLine(0, s, 0, 0); p.drawLine(0, 0, s, 0)
        p.drawLine(w - s, 0, w, 0); p.drawLine(w, 0, w, s)
        p.drawLine(0, h - s, 0, h); p.drawLine(0, h, s, h)
        p.drawLine(w - s, h, w, h); p.drawLine(w, h - s, w, h)
        p.end()


class ScanlineOverlay(QWidget):
    """Subtle scanline texture overlay."""
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(parent.size())

    def paintEvent(self, e):
        p = QPainter(self)
        p.setOpacity(0.04)
        pen = QPen(QColor("#00FFFF"), 1)
        p.setPen(pen)
        for y in range(0, self.height(), 3):
            p.drawLine(0, y, self.width(), y)
        p.end()


class HudButton(QPushButton):
    """JARVIS-style button with glow border."""
    def __init__(self, text, accent=None, parent=None):
        super().__init__(text, parent)
        self.accent = accent or Theme.CYAN
        self._hovered = False
        self.setFont(ui_font(11, bold=True))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()

    def _update_style(self):
        c = self.accent
        dim = QColor(c.red(), c.green(), c.blue(), 40)
        self.setStyleSheet(f"""
            QPushButton {{
                background: {'rgba(%d,%d,%d,60)' % (c.red(), c.green(), c.blue()) if self._hovered else 'transparent'};
                color: {c.name()};
                border: 1px solid {c.name()};
                border-radius: 2px;
                padding: 8px 16px;
                letter-spacing: 2px;
                text-transform: uppercase;
            }}
            QPushButton:pressed {{
                background: {'rgba(%d,%d,%d,100)' % (c.red(), c.green(), c.blue())};
            }}
        """)

    def enterEvent(self, e):
        self._hovered = True
        self._update_style()

    def leaveEvent(self, e):
        self._hovered = False
        self._update_style()


class HudLabel(QLabel):
    def __init__(self, text, size=11, color=None, mono=False, bold=False, parent=None):
        super().__init__(text, parent)
        self.setFont(hud_font(size, bold) if mono else ui_font(size, bold))
        c = color or Theme.WHITE
        self.setStyleSheet(f"color: {c.name()}; background: transparent;")


class StatusDot(QWidget):
    """Animated blinking status indicator."""
    def __init__(self, color=None, parent=None):
        super().__init__(parent)
        self.color = color or Theme.GREEN
        self.setFixedSize(10, 10)
        self._alpha = 255
        self._fade = -8
        t = QTimer(self)
        t.timeout.connect(self._blink)
        t.start(50)

    def _blink(self):
        self._alpha += self._fade
        if self._alpha <= 60 or self._alpha >= 255:
            self._fade *= -1
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        c = QColor(self.color.red(), self.color.green(), self.color.blue(), self._alpha)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(c)
        p.drawEllipse(1, 1, 8, 8)
        p.end()


class HudInput(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFont(hud_font(11))
        self.setStyleSheet(f"""
            QLineEdit {{
                background: {Theme.BG_CARD.name()};
                color: {Theme.CYAN.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 2px;
                padding: 8px 12px;
                selection-background-color: {Theme.CYAN_DARK.name()};
            }}
            QLineEdit:focus {{
                border-color: {Theme.CYAN.name()};
            }}
        """)


# ─── SIDEBAR NAV ──────────────────────────────────────────────────────────────

class NavButton(QPushButton):
    def __init__(self, text, icon_char="►", active=False, parent=None):
        super().__init__(parent)
        self.icon_char = icon_char
        self._active = active
        self.full_text = text
        self.setCheckable(True)
        self.setChecked(active)
        self.setFont(ui_font(11, bold=True))
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._update_style()

    def setActive(self, active):
        self._active = active
        self.setChecked(active)
        self._update_style()

    def _update_style(self):
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {Theme.CYAN_DARK.name()};
                    color: {Theme.CYAN.name()};
                    border: none;
                    border-left: 3px solid {Theme.CYAN.name()};
                    padding: 0 20px;
                    text-align: left;
                    letter-spacing: 2px;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {Theme.TEXT_SEC.name()};
                    border: none;
                    border-left: 3px solid transparent;
                    padding: 0 20px;
                    text-align: left;
                    letter-spacing: 2px;
                }}
                QPushButton:hover {{
                    background: {Theme.BG_CARD.name()};
                    color: {Theme.CYAN_DIM.name()};
                    border-left-color: {Theme.CYAN_DIM.name()};
                }}
            """)
        self.setText(f"  {self.full_text}")


# ─── SCREENS ──────────────────────────────────────────────────────────────────

class DashboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._start_updates()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # top header
        hdr = QHBoxLayout()
        title = HudLabel("SYSTEM STATUS", 16, Theme.CYAN, mono=True, bold=True)
        hdr.addWidget(title)
        hdr.addStretch()
        dot = StatusDot(Theme.GREEN)
        hdr.addWidget(dot)
        conn_label = HudLabel("CONNECTED", 10, Theme.GREEN, mono=True)
        hdr.addWidget(conn_label)
        layout.addLayout(hdr)

        # separator
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {Theme.BORDER.name()};")
        layout.addWidget(sep)

        # arc rings row
        rings_row = QHBoxLayout()
        rings_row.setSpacing(24)
        self.cpu_ring = ArcRing("CPU", 42, Theme.CYAN, size=130)
        self.ram_ring = ArcRing("RAM", 67, QColor("#4488FF"), size=130)
        self.disk_ring = ArcRing("DISK", 31, Theme.AMBER, size=130)
        self.net_ring = ArcRing("NET", 88, Theme.GREEN, size=130)
        for ring in [self.cpu_ring, self.ram_ring, self.disk_ring, self.net_ring]:
            rings_row.addWidget(ring, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(rings_row)

        # stats grid
        grid = QGridLayout()
        grid.setSpacing(12)
        stats = [
            ("UPTIME", "14:23:07", Theme.CYAN),
            ("PROCESSES", "247", Theme.WHITE),
            ("TEMP", "62°C", Theme.AMBER),
            ("PING", "12 ms", Theme.GREEN),
            ("DOWNLOAD", "3.2 MB/s", Theme.CYAN),
            ("UPLOAD", "0.8 MB/s", Theme.TEXT_SEC),
        ]
        for i, (lbl, val, color) in enumerate(stats):
            card = HudCard(accent=color)
            cv = QVBoxLayout(card)
            cv.setContentsMargins(14, 10, 14, 10)
            cv.setSpacing(2)
            cv.addWidget(HudLabel(lbl, 8, Theme.TEXT_SEC, mono=True))
            cv.addWidget(HudLabel(val, 16, color, mono=True, bold=True))
            grid.addWidget(card, i // 3, i % 3)
        layout.addLayout(grid)

        # activity log
        log_card = HudCard(accent=Theme.CYAN)
        log_layout = QVBoxLayout(log_card)
        log_layout.setContentsMargins(14, 10, 14, 10)
        log_layout.addWidget(HudLabel("ACTIVITY LOG", 9, Theme.TEXT_SEC, mono=True))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(hud_font(9))
        self.log_text.setStyleSheet(f"""
            QTextEdit {{
                background: transparent;
                color: {Theme.CYAN_DIM.name()};
                border: none;
            }}
        """)
        self.log_text.setMaximumHeight(80)
        sample_logs = [
            "[14:23:07] SYS  Agent initialized successfully",
            "[14:23:08] NET  WebSocket connection established",
            "[14:23:10] AUTH Google OAuth verified",
            "[14:23:12] SYS  Monitoring active — 4 cores tracked",
        ]
        self.log_text.setText("\n".join(sample_logs))
        log_layout.addWidget(self.log_text)
        layout.addWidget(log_card)

    def _start_updates(self):
        t = QTimer(self)
        t.timeout.connect(self._update_values)
        t.start(2000)

    def _update_values(self):
        self.cpu_ring.set_value(random.randint(20, 90))
        self.ram_ring.set_value(random.randint(50, 85))
        self.disk_ring.set_value(random.randint(25, 45))
        self.net_ring.set_value(random.randint(10, 95))


class MouseControlScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._mouse_x = 0
        self._mouse_y = 0

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        hdr = HudLabel("REMOTE CURSOR CONTROL", 16, Theme.CYAN, mono=True, bold=True)
        layout.addWidget(hdr)

        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {Theme.BORDER.name()};")
        layout.addWidget(sep)

        # trackpad
        trackpad_card = HudCard(accent=Theme.CYAN)
        tp_layout = QVBoxLayout(trackpad_card)
        tp_layout.setContentsMargins(14, 12, 14, 12)
        tp_layout.addWidget(HudLabel("TRACKPAD", 9, Theme.TEXT_SEC, mono=True))
        self.trackpad = TrackpadWidget()
        tp_layout.addWidget(self.trackpad)
        layout.addWidget(trackpad_card, stretch=2)

        # coords display
        coord_row = QHBoxLayout()
        self.coord_label = HudLabel("X: 000  Y: 000", 12, Theme.CYAN, mono=True)
        coord_row.addWidget(self.coord_label)
        coord_row.addStretch()
        layout.addLayout(coord_row)

        # buttons
        btn_grid = QGridLayout()
        btn_grid.setSpacing(8)
        buttons = [
            ("LEFT CLICK", Theme.CYAN),
            ("RIGHT CLICK", Theme.RED),
            ("SCROLL UP", Theme.GREEN),
            ("SCROLL DOWN", Theme.AMBER),
            ("MIDDLE CLICK", Theme.TEXT_SEC),
            ("DOUBLE CLICK", Theme.CYAN),
        ]
        for i, (lbl, color) in enumerate(buttons):
            b = HudButton(lbl, accent=color)
            btn_grid.addWidget(b, i // 3, i % 3)
        layout.addLayout(btn_grid)


class TrackpadWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self._pos = QPointF(0.5, 0.5)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.CrossCursor)

    def mouseMoveEvent(self, e):
        self._pos = QPointF(e.position().x() / self.width(),
                            e.position().y() / self.height())
        self.update()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # bg
        p.fillRect(0, 0, w, h, Theme.BG)

        # grid lines
        pen = QPen(QColor(0, 255, 255, 20), 1)
        p.setPen(pen)
        for x in range(0, w, 40):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            p.drawLine(0, y, w, y)

        # crosshair
        cx = int(self._pos.x() * w)
        cy = int(self._pos.y() * h)
        cross_pen = QPen(Theme.CYAN, 1)
        cross_pen.setStyle(Qt.PenStyle.DashLine)
        p.setPen(cross_pen)
        p.drawLine(cx, 0, cx, h)
        p.drawLine(0, cy, w, cy)

        # cursor dot
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(Theme.CYAN)
        p.drawEllipse(QPointF(cx, cy), 5, 5)

        # outer ring at cursor
        ring_pen = QPen(Theme.CYAN_DIM, 1)
        p.setPen(ring_pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawEllipse(QPointF(cx, cy), 15, 15)

        p.end()


class KeyboardScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        layout.addWidget(HudLabel("KEYBOARD INPUT", 16, Theme.CYAN, mono=True, bold=True))
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {Theme.BORDER.name()};")
        layout.addWidget(sep)

        # text input area
        input_card = HudCard(accent=Theme.CYAN)
        ic_layout = QVBoxLayout(input_card)
        ic_layout.setContentsMargins(14, 12, 14, 12)
        ic_layout.addWidget(HudLabel("TEXT TO SEND", 9, Theme.TEXT_SEC, mono=True))
        self.text_input = QTextEdit()
        self.text_input.setFont(hud_font(11))
        self.text_input.setStyleSheet(f"""
            QTextEdit {{
                background: {Theme.BG.name()};
                color: {Theme.CYAN.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 2px;
                padding: 8px;
            }}
        """)
        self.text_input.setMinimumHeight(80)
        ic_layout.addWidget(self.text_input)
        layout.addWidget(input_card)

        # send button
        send_btn = HudButton("TRANSMIT", Theme.CYAN)
        send_btn.setFixedHeight(42)
        layout.addWidget(send_btn)

        # special keys
        special_card = HudCard(accent=Theme.AMBER)
        sk_layout = QVBoxLayout(special_card)
        sk_layout.setContentsMargins(14, 10, 14, 10)
        sk_layout.addWidget(HudLabel("SPECIAL KEYS", 9, Theme.TEXT_SEC, mono=True))
        keys_row = QHBoxLayout()
        special_keys = ["ESC", "TAB", "ENTER", "CTRL+C", "CTRL+V", "ALT+F4"]
        for k in special_keys:
            b = HudButton(k, Theme.AMBER)
            b.setFixedHeight(36)
            keys_row.addWidget(b)
        sk_layout.addLayout(keys_row)
        layout.addWidget(special_card)
        layout.addStretch()


class AIAssistantScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        layout.addWidget(HudLabel("AI INTERFACE", 16, Theme.CYAN, mono=True, bold=True))
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {Theme.BORDER.name()};")
        layout.addWidget(sep)

        # chat area
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet(f"""
            QScrollArea {{
                background: {Theme.BG_CARD.name()};
                border: 1px solid {Theme.BORDER.name()};
                border-radius: 2px;
            }}
            QScrollBar:vertical {{
                background: {Theme.BG.name()};
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {Theme.CYAN_DIM.name()};
                border-radius: 3px;
            }}
        """)
        chat_inner = QWidget()
        self._chat_layout = QVBoxLayout(chat_inner)
        self._chat_layout.setSpacing(12)
        self._chat_layout.setContentsMargins(12, 12, 12, 12)
        self._chat_layout.addStretch()

        # sample messages
        self._add_message("JARVIS", "NeuroSync AI online. How can I assist?", is_ai=True)
        self._add_message("YOU", "Show system status.", is_ai=False)
        self._add_message("JARVIS", "All systems nominal. CPU at 42%, RAM at 67%. No anomalies detected.", is_ai=True)

        self.chat_area.setWidget(chat_inner)
        layout.addWidget(self.chat_area, stretch=1)

        # input row
        input_row = QHBoxLayout()
        self.msg_input = HudInput("ENTER COMMAND...")
        self.msg_input.returnPressed.connect(self._send_message)
        send_btn = HudButton("SEND", Theme.CYAN)
        send_btn.setFixedWidth(80)
        send_btn.clicked.connect(self._send_message)
        input_row.addWidget(self.msg_input)
        input_row.addWidget(send_btn)
        layout.addLayout(input_row)

    def _add_message(self, sender, text, is_ai=True):
        msg_card = HudCard(accent=Theme.CYAN if is_ai else Theme.AMBER)
        mv = QVBoxLayout(msg_card)
        mv.setContentsMargins(12, 8, 12, 8)
        mv.setSpacing(4)
        sender_label = HudLabel(sender, 8, Theme.CYAN if is_ai else Theme.AMBER, mono=True, bold=True)
        text_label = HudLabel(text, 11, Theme.WHITE)
        text_label.setWordWrap(True)
        mv.addWidget(sender_label)
        mv.addWidget(text_label)
        self._chat_layout.insertWidget(self._chat_layout.count() - 1, msg_card)

    def _send_message(self):
        text = self.msg_input.text().strip()
        if not text:
            return
        self._add_message("YOU", text, is_ai=False)
        self.msg_input.clear()
        # stub response
        QTimer.singleShot(500, lambda: self._add_message("JARVIS", "Processing your command...", is_ai=True))


class FileManagerScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        layout.addWidget(HudLabel("FILE SYSTEM", 16, Theme.CYAN, mono=True, bold=True))
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {Theme.BORDER.name()};")
        layout.addWidget(sep)

        # path bar
        path_row = QHBoxLayout()
        path_label = HudLabel("PATH:", 9, Theme.TEXT_SEC, mono=True)
        self.path_input = HudInput("/home/user/Documents")
        go_btn = HudButton("GO", Theme.CYAN)
        go_btn.setFixedWidth(60)
        path_row.addWidget(path_label)
        path_row.addWidget(self.path_input)
        path_row.addWidget(go_btn)
        layout.addLayout(path_row)

        # file list
        files_card = HudCard(accent=Theme.CYAN)
        fl = QVBoxLayout(files_card)
        fl.setContentsMargins(14, 10, 14, 10)
        fl.setSpacing(6)
        fl.addWidget(HudLabel("DIRECTORY CONTENTS", 9, Theme.TEXT_SEC, mono=True))

        sample_files = [
            ("📁", "Projects", "DIR", Theme.CYAN),
            ("📁", "Downloads", "DIR", Theme.CYAN),
            ("📄", "resume.pdf", "2.3 MB", Theme.WHITE),
            ("📄", "notes.txt", "12 KB", Theme.WHITE),
            ("⚙️", "config.json", "4 KB", Theme.AMBER),
        ]
        for icon, name, size, color in sample_files:
            row = QHBoxLayout()
            name_lbl = HudLabel(f"  {name}", 11, color, mono=True)
            size_lbl = HudLabel(size, 9, Theme.TEXT_SEC, mono=True)
            row.addWidget(HudLabel(icon, 11))
            row.addWidget(name_lbl)
            row.addStretch()
            row.addWidget(size_lbl)
            fl.addLayout(row)

        layout.addWidget(files_card, stretch=1)

        # action buttons
        act_row = QHBoxLayout()
        for lbl, color in [("UPLOAD", Theme.GREEN), ("DOWNLOAD", Theme.CYAN), ("DELETE", Theme.RED)]:
            act_row.addWidget(HudButton(lbl, color))
        layout.addLayout(act_row)


# ─── TOP BAR ──────────────────────────────────────────────────────────────────

class TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(52)
        self.setStyleSheet(f"background: {Theme.BG_CARD.name()}; border-bottom: 1px solid {Theme.BORDER.name()};")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)

        # logo / title
        logo = HudLabel("NEUROSYNC", 16, Theme.CYAN, mono=True, bold=True)
        layout.addWidget(logo)
        layout.addSpacing(8)
        version = HudLabel("v1.0 · JARVIS HUD", 9, Theme.TEXT_SEC, mono=True)
        layout.addWidget(version)
        layout.addStretch()

        # live clock
        self.clock_label = HudLabel("00:00:00", 14, Theme.CYAN, mono=True)
        layout.addWidget(self.clock_label)
        layout.addSpacing(20)

        # status indicators
        for lbl, color in [("AGENT", Theme.GREEN), ("NET", Theme.GREEN), ("AUTH", Theme.CYAN)]:
            dot = StatusDot(color)
            layout.addWidget(dot)
            layout.addWidget(HudLabel(lbl, 8, color, mono=True))
            layout.addSpacing(12)

        # window controls
        for sym, color in [("—", Theme.TEXT_SEC), ("□", Theme.TEXT_SEC), ("✕", Theme.RED)]:
            btn = QPushButton(sym)
            btn.setFixedSize(32, 32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {color.name()};
                    border: none;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background: {Theme.BORDER.name()};
                }}
            """)
            layout.addWidget(btn)

        self._clock_timer = QTimer()
        self._clock_timer.timeout.connect(self._update_clock)
        self._clock_timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        from datetime import datetime
        self.clock_label.setText(datetime.now().strftime("%H:%M:%S"))


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

class Sidebar(QWidget):
    page_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet(f"background: {Theme.BG_PANEL.name()}; border-right: 1px solid {Theme.BORDER.name()};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 16, 0, 16)
        layout.setSpacing(2)

        nav_items = [
            ("DASHBOARD", "◈"),
            ("MOUSE CTRL", "⊕"),
            ("KEYBOARD", "⌨"),
            ("AI ASSIST", "◉"),
            ("FILE SYS", "◧"),
        ]
        self._buttons = []
        for i, (text, icon) in enumerate(nav_items):
            btn = NavButton(text, icon, active=(i == 0))
            btn.clicked.connect(lambda _, idx=i: self._on_click(idx))
            self._buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # bottom info
        info = HudLabel("AGENT READY", 8, Theme.GREEN, mono=True)
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        build = HudLabel("BUILD 2024.06", 8, Theme.TEXT_SEC, mono=True)
        build.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(build)

    def _on_click(self, idx):
        for i, btn in enumerate(self._buttons):
            btn.setActive(i == idx)
        self.page_changed.emit(idx)


# ─── MAIN WINDOW ──────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NeuroSync — JARVIS HUD")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._drag_pos = None

        central = QWidget()
        central.setStyleSheet(f"background: {Theme.BG.name()};")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # top bar
        self.topbar = TopBar()
        root.addWidget(self.topbar)

        # body: sidebar + pages
        body = QHBoxLayout()
        body.setSpacing(0)
        body.setContentsMargins(0, 0, 0, 0)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self._switch_page)
        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background: transparent;")
        self.stack.addWidget(DashboardScreen())
        self.stack.addWidget(MouseControlScreen())
        self.stack.addWidget(KeyboardScreen())
        self.stack.addWidget(AIAssistantScreen())
        self.stack.addWidget(FileManagerScreen())
        body.addWidget(self.stack)

        root.addLayout(body)

    def _switch_page(self, idx):
        self.stack.setCurrentIndex(idx)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = e.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self._drag_pos and e.buttons() == Qt.MouseButton.LeftButton:
            self.move(e.globalPosition().toPoint() - self._drag_pos)

    def mouseReleaseEvent(self, e):
        self._drag_pos = None


# ─── ENTRY POINT ──────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # dark palette base
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, Theme.BG)
    palette.setColor(QPalette.ColorRole.WindowText, Theme.WHITE)
    palette.setColor(QPalette.ColorRole.Base, Theme.BG_CARD)
    palette.setColor(QPalette.ColorRole.AlternateBase, Theme.BG_PANEL)
    palette.setColor(QPalette.ColorRole.Text, Theme.WHITE)
    palette.setColor(QPalette.ColorRole.Button, Theme.BG_CARD)
    palette.setColor(QPalette.ColorRole.ButtonText, Theme.CYAN)
    palette.setColor(QPalette.ColorRole.Highlight, Theme.CYAN_DARK)
    palette.setColor(QPalette.ColorRole.HighlightedText, Theme.CYAN)
    app.setPalette(palette)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()