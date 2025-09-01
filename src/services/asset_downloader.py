# src/services/asset_downloader.py

import os
import sys
import requests
import zipfile
import shutil
from PySide6.QtWidgets import QProgressDialog, QMessageBox, QApplication
from PySide6.QtCore import Qt

from ..config.app_config import IMAGE_ASSETS_URL, APP_VERSION
from ..utils import get_app_data_path

def check_and_download_image_assets():
    """
    Checks if the image assets are present and up-to-date. If not, downloads and extracts them.
    Returns True if assets are ready, False if there was an unrecoverable error.
    """
    app_data_path = get_app_data_path()
    # The zip should contain the 'Bosses_locations' structure, not 'data/Bosses_locations'
    image_assets_path = os.path.join(app_data_path, "Bosses_locations")
    version_file = os.path.join(app_data_path, "image_assets_version.txt")

    # Check if the folder exists, is not empty, and the version file matches.
    if os.path.exists(image_assets_path) and os.path.exists(version_file) and os.listdir(image_assets_path):
        with open(version_file, 'r') as f:
            local_version = f.read().strip()
        if local_version == APP_VERSION:
            print("Image assets are up to date.")
            return True

    print("Image assets are missing or outdated. Starting download...")
    
    os.makedirs(app_data_path, exist_ok=True)

    progress = QProgressDialog("Downloading Boss Images...", "Cancel", 0, 100, None)
    progress.setWindowModality(Qt.WindowModality.ApplicationModal)
    progress.setWindowTitle("Downloading Images")
    progress.setMinimumDuration(0)
    progress.setValue(0)
    QApplication.processEvents()

    try:
        response = requests.get(IMAGE_ASSETS_URL, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        zip_path = os.path.join(app_data_path, "boss_locations.zip")

        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if progress.wasCanceled():
                    raise Exception("Download canceled by user.")
                f.write(chunk)
                downloaded_size += len(chunk)
                if total_size > 0:
                    progress.setValue(int((downloaded_size / total_size) * 100))
                QApplication.processEvents()
        
        progress.setLabelText("Extracting images...")
        progress.setValue(100)
        QApplication.processEvents()

        # The zip file should contain a top-level 'Bosses_locations' folder.
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(app_data_path)
        
        os.remove(zip_path)

        with open(version_file, 'w') as f:
            f.write(APP_VERSION)

        print("Image assets downloaded and extracted successfully.")
        progress.close()
        return True

    except Exception as e:
        progress.close()
        error_message = f"Failed to download or extract image assets: {e}\nBoss images will not be available."
        print(error_message)
        QMessageBox.critical(None, "Asset Error", error_message)
        # We return True because the app can function without images, unlike core data.
        return True