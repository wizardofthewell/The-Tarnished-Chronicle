# src/location_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox
)
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtCore import Qt
from ...utils import get_image_path

class LocationDialog(QDialog):
    """
    A simple dialog to display a boss's location image.
    """
    def __init__(self, boss_data, parent=None):
        super().__init__(parent)
        self.boss_data = boss_data
        self.setWindowTitle(f"Location: {self.boss_data.get('name', 'N/A')}")
        self.setObjectName("locationDialog")

        # --- DEBUG MODE ---
        print(f"DEBUG: LocationDialog.__init__ called for boss: {self.boss_data.get('name')}")

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        image_path = self.boss_data.get("location_image")
        image_label = QLabel()

        if image_path:
            # The 'location_image' field now contains the full relative path to the image.
            # We just need to pass it to get_image_path to get the absolute path.
            full_image_path = get_image_path(image_path)
            pixmap = QPixmap(full_image_path)
            
            if not pixmap.isNull():
                image_label.setPixmap(pixmap.scaledToWidth(870, Qt.TransformationMode.SmoothTransformation))
            else:
                error_path_display = full_image_path.replace('\\', '/')
                image_label.setText(f"Image not found at:\n{error_path_display}")
        else:
            image_label.setText("No location image available for this boss.")
        
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(image_label)

        # Description Label
        description = self.boss_data.get("description", "")
        if description:
            description_label = QLabel(description)
            description_label.setWordWrap(True)
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            description_label.setObjectName("descriptionLabel")
            main_layout.addWidget(description_label)

        # OK Button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        main_layout.addWidget(button_box, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)