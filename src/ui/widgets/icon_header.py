# src/ui/widgets/icon_header.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from ...utils import create_colored_pixmap, get_resource_path
from .unicode_icons import create_unicode_pixmap

class IconHeader(QWidget):
    def __init__(self, icon_path, text, is_expandable=False, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        if icon_path:
            icon_label = QLabel()
            pixmap = create_colored_pixmap(icon_path, QColor(234, 179, 8), QSize(16, 16))
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(18, 18)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setObjectName("sidebarHeader")
        layout.addWidget(text_label)
        layout.addStretch()

        if is_expandable:
            self.toggle_button = QPushButton()
            self.toggle_button.setObjectName("expandCollapseButton")
            self.toggle_button.setCheckable(True)
            self.toggle_button.setFixedSize(20, 20)
            layout.addWidget(self.toggle_button)
            self.set_expanded(False)

    def set_expanded(self, is_expanded):
        if hasattr(self, 'toggle_button'):
            chevron_icon = 'chevron-down' if is_expanded else 'chevron-right'
            self.toggle_button.setIcon(QIcon(create_unicode_pixmap(chevron_icon, QSize(14, 14))))
            self.toggle_button.setChecked(is_expanded)