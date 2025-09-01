# src/ui/widgets/resizing_stacked_widget.py

from PySide6.QtWidgets import QStackedWidget, QSizePolicy
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QTimer

class ResizingStackedWidget(QStackedWidget):
    """
    A QStackedWidget that animates its size change to fit the current widget.
    This prevents the parent layout from jumping around when switching pages.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentChanged.connect(self._on_current_changed)
        # Allow the widget to shrink and expand vertically
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

    def _on_current_changed(self, index):
        # When the widget changes, we need to invalidate the old size hint
        # and tell the layout system to re-evaluate our size.
        self.updateGeometry()

    def sizeHint(self):
        if self.currentWidget():
            return self.currentWidget().sizeHint()
        return super().sizeHint()

    def minimumSizeHint(self):
        if self.currentWidget():
            return self.currentWidget().minimumSizeHint()
        return super().minimumSizeHint()