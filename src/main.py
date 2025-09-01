# src/main.py

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import QApplication
from src.services.asset_downloader import check_and_download_image_assets
from src.ui.main_window import BossChecklistApp
import resources_rc # Import the compiled resources

def main():
    # QApplication must be created before any UI elements like progress dialogs
    app = QApplication(sys.argv)

    # Check for image assets before creating the main window
    check_and_download_image_assets()

    window = BossChecklistApp()
    window.show()
    window.update_checker.check_for_updates()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()