# src/ui/widgets/toggle_switch.py

from PySide6.QtCore import Property, QPointF, QRectF, QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QPainter, QBrush, QColor
from PySide6.QtWidgets import QAbstractButton

class ToggleSwitch(QAbstractButton):
    """A custom widget for a modern animated toggle switch."""
    def __init__(self, parent=None, bg_color="#4C566A", circle_color="#D8DEE9", active_color="#A3BE8C"):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(50, 26)
        self._bg_color = QColor(bg_color)
        self._circle_color = QColor(circle_color)
        self._active_color = QColor(active_color)
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(300)
        self.toggled.connect(self.start_animation)

    @Property(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def start_animation(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 23)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setPen(Qt.PenStyle.NoPen)
        rect = QRectF(0, 0, self.width(), self.height())
        bg_brush = QBrush(self._active_color if self.isChecked() else self._bg_color)
        p.setBrush(bg_brush)
        p.drawRoundedRect(rect, 13, 13)
        p.setBrush(QBrush(self._circle_color))
        p.drawEllipse(QPointF(self._circle_position + 10, self.height() / 2), 10, 10)