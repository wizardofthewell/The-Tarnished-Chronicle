# src/services/update_checker.py

import requests
import threading
from PySide6.QtCore import QObject, Signal
from packaging.version import parse as parse_version

from ..config.app_config import APP_VERSION, MANIFEST_URL

class UpdateChecker(QObject):
    """
    Kontroluje na serveru, zda je k dispozici nová verze aplikace.
    Používá manifest ve formátu JSON.
    """
    # Signál, který nese celý slovník s informacemi o aktualizaci
    update_available = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._thread = None

    def check_for_updates(self):
        """
        Spustí kontrolu aktualizací v samostatném vlákně, aby neblokovala UI.
        """
        if self._thread and self._thread.is_alive():
            print("Update check already in progress.")
            return

        self._thread = threading.Thread(target=self._run_check)
        self._thread.daemon = True
        self._thread.start()

    def _run_check(self):
        """
        Stáhne manifest, porovná verze a v případě potřeby vyšle signál.
        """
        try:
            response = requests.get(MANIFEST_URL, timeout=10)
            response.raise_for_status()  # Vyvolá výjimku pro HTTP chyby 4xx/5xx
            manifest_data = response.json()
            
            latest_version_str = manifest_data.get("version")
            if not latest_version_str:
                print("Manifest does not contain 'version' key.")
                return

            current_version = parse_version(APP_VERSION)
            latest_version = parse_version(latest_version_str)

            if latest_version > current_version:
                print(f"New version available: {latest_version_str}")
                # Předáme celý manifest, aby UI mělo všechny potřebné informace
                self.update_available.emit(manifest_data)
            else:
                print(f"Application is up to date (current: {APP_VERSION}, latest: {latest_version_str}).")

        except requests.RequestException as e:
            print(f"Error during update check (network): {e}")
        except Exception as e:
            print(f"An unexpected error occurred during update check: {e}")