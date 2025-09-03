# src/ui/widgets/empty_state_widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from ...utils import get_resource_path

class EmptyStateWidget(QWidget):
    """
    A widget to display when no save file or character is selected.
    It provides guidance to the user on the next steps.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("emptyStateWidget")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Icon
        self.icon_label = QLabel()
        icon_path = get_resource_path("assets/icons/file-text.svg")
        pixmap = QPixmap(icon_path)
        self.icon_label.setPixmap(pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        self.title_label = QLabel("Welcome to the ER Boss Checklist")
        self.title_label.setObjectName("emptyStateTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Instructional Text
        self.instruction_label = QLabel("To get started, please select your Elden Ring save file (.sl2 for Vanilla or .co2 for Seamless Coop).")
        self.instruction_label.setObjectName("emptyStateInstruction")
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setWordWrap(True)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.instruction_label)

        self.setLayout(layout)

    def set_state(self, state: str):
        """
        Updates the text and icon based on the current onboarding step.
        
        Args:
            state (str): Either 'select_file' or 'select_character'.
        """
        if state == "select_file":
            self.icon_label.setPixmap(QPixmap(get_resource_path("assets/icons/file-text.svg")).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.title_label.setText("Welcome to the ER Boss Checklist")
            self.instruction_label.setText("To get started, please select your Elden Ring save file (.sl2 for Vanilla or .co2 for Seamless Coop) using the left menu button.")
        elif state == "select_character":
            self.icon_label.setPixmap(QPixmap(get_resource_path("assets/icons/user.svg")).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.title_label.setText("Save File Loaded!")
            self.instruction_label.setText("Great! Now, please select a character from the dropdown list in the left menu to view their progress.") 