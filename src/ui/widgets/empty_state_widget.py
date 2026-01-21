# src/ui/widgets/empty_state_widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt, QSize

from ...utils import get_resource_path, create_colored_pixmap

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

        # Icon (use create_colored_pixmap for Unicode fallback support)
        self.icon_label = QLabel()
        icon_path = get_resource_path("assets/icons/file-text.svg")
        pixmap = create_colored_pixmap(icon_path, QColor(234, 179, 8), QSize(48, 48))
        self.icon_label.setPixmap(pixmap)
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
            pixmap = create_colored_pixmap(get_resource_path("assets/icons/file-text.svg"), QColor(234, 179, 8), QSize(48, 48))
            self.icon_label.setPixmap(pixmap)
            self.title_label.setText("Welcome to the ER Boss Checklist")
            self.instruction_label.setText("To get started, please select your Elden Ring save file (.sl2 for Vanilla or .co2 for Seamless Coop) using the left menu button.")
        elif state == "select_character":
            pixmap = create_colored_pixmap(get_resource_path("assets/icons/user.svg"), QColor(234, 179, 8), QSize(48, 48))
            self.icon_label.setPixmap(pixmap)
            self.title_label.setText("Save File Loaded!")
            self.instruction_label.setText("Great! Now, please select a character from the dropdown list in the left menu to view their progress.") 