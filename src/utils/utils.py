# src/utils.py

import os
import sys
from PySide6.QtCore import QSize, QByteArray, Qt, QFile, QIODevice
from PySide6.QtGui import QColor, QPixmap

def get_resource_path(relative_path):
    """
    Get path to resource.
    For dev, it's a file path. For packaged app, it's a Qt resource path.
    """
    # When using .qrc files, the path is relative to the root defined in the .qrc prefix.
    # We just need to prepend ":/" to the relative path.
    # The original logic for _MEIPASS is no longer needed for icons and JSONs.
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Packaged app: return Qt resource path
        return f":/{relative_path.replace(os.path.sep, '/')}"
    else:
        # Dev environment: return normal file system path
        return relative_path

def create_colored_pixmap(icon_path: str, color: QColor, size: QSize) -> QPixmap:
    """
    Loads an SVG icon from a file path or a Qt resource path,
    replaces its 'currentColor' with a specified QColor,
    and returns it as a scaled QPixmap.
    """
    try:
        qfile = QFile(icon_path)
        if not qfile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            raise IOError(f"Cannot open resource file: {icon_path}")

        svg_data = qfile.readAll().data().decode('utf-8')
        qfile.close()
        
        colored_svg_data = svg_data.replace('currentColor', color.name())
        byte_array = QByteArray(colored_svg_data.encode('utf-8'))
        
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array)
        
        return pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    except Exception as e:
        print(f"Error creating colored pixmap for {icon_path}: {e}")
        return QPixmap()
def format_seconds_to_hms(seconds: int) -> str:
    """Formats a duration in seconds to a HH:MM:SS string."""
    if not isinstance(seconds, (int, float)) or seconds < 0:
        return "--:--"
    
    h, rem = divmod(int(seconds), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def get_app_data_path():
    """Returns the path to the application's data directory."""
    # This function is moved here to prevent circular imports.
    from src.config.app_config import APP_DATA_DIR
    base_path = os.getenv('LOCALAPPDATA')
    if not base_path:
        base_path = os.path.expanduser("~")
    return os.path.join(base_path, APP_DATA_DIR)

def get_image_path(relative_path):
    """
    Get absolute path to a downloaded image asset.
    Works for dev (local files) and for packaged app (AppData files).
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Packaged app: images are in the AppData directory.
        base_path = get_app_data_path()
    else:
        # Dev environment: images are in the project root.
        base_path = os.path.abspath(".")
    
    # If the relative path starts with 'data/', strip it for the AppData case.
    if getattr(sys, 'frozen', False) and relative_path.startswith(('data/', 'data\\')):
        # Strip the 'data/' prefix.
        # Example: 'data/Bosses_locations/image.png' -> 'Bosses_locations/image.png'
        # Normalize path separators to be consistent with the current OS.
        normalized_path = relative_path.replace('/', os.path.sep).replace('\\', os.path.sep)
        
        path_parts = normalized_path.split(os.path.sep, 1)
        if len(path_parts) > 1:
            relative_path = path_parts[1]
        else:
            relative_path = ''

    return os.path.join(base_path, relative_path)