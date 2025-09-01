# src/ui/widgets/footer.py

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget
from PySide6.QtGui import QIcon, QColor
from PySide6.QtCore import Qt
from ...config.app_config import APP_VERSION
from ...utils import format_seconds_to_hms

class FooterWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("footer")
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 5, 15, 5)

        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setObjectName("versionLabel")
        layout.addWidget(version_label)

        layout.addStretch()

        credit_label = QLabel('Made with <span style="color: #ff0000;">♥</span> by <a href="https://github.com/RysanekDavid" style="color: #5B90C5;">Davosso</a>')
        credit_label.setObjectName("creditLabel")
        credit_label.setOpenExternalLinks(True)
        layout.addWidget(credit_label)

    def update_monitoring_status(self, active: bool, text: str = ""):
        # This functionality is no longer displayed, but we keep the method
        # in case it's needed in the future, to avoid breaking the app logic.
        pass

    def update_stats(self, stats: dict):
        # This functionality is no longer displayed.
        pass

    def update_time(self, seconds: int):
        # This functionality is no longer displayed.
        pass
