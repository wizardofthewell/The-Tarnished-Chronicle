# src/ui/widgets/unicode_icons.py
"""
Unicode-based icons for cross-platform compatibility.
These replace SVG icons that may not be available.
"""

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QSize

# Unicode symbols for various icons
ICONS = {
    'check': '✓',           # Check mark
    'x': '✗',               # X mark  
    'x-circle': '⊘',        # Circle with slash
    'eye': '👁',             # Eye
    'map-pin': '📍',         # Map pin
    'chevron-right': '▶',   # Right arrow
    'chevron-down': '▼',    # Down arrow
    'chevrons-up': '⬆',     # Double up arrow
    'chevrons-down': '⬇',   # Double down arrow
    # Sidebar icons
    'file-text': '📄',       # Document/file
    'user': '👤',            # User/person
    'filter': '⚙',          # Filter/gear
    'clock': '🕐',           # Clock
    'skull': '💀',           # Skull/deaths
    'info-circle': 'ℹ',     # Info
    'square': '☐',          # Empty checkbox
    'check-square': '☑',    # Checked checkbox
}

# Colors for status icons
COLORS = {
    'check': '#22c55e',     # Green
    'x': '#ef4444',         # Red
    'x-circle': '#6b7280',  # Gray
    'eye': '#3b82f6',       # Blue
    'map-pin': '#f59e0b',   # Amber
    'chevron': '#9ca3af',   # Gray
    'chevrons-up': '#22c55e',   # Green
    'chevrons-down': '#ef4444', # Red
    'file-text': '#eab308', # Yellow (matches app theme)
    'user': '#eab308',      # Yellow
    'filter': '#eab308',    # Yellow
    'clock': '#eab308',     # Yellow
    'skull': '#eab308',     # Yellow
    'info-circle': '#3b82f6', # Blue
    'square': '#9ca3af',    # Gray
    'check-square': '#22c55e', # Green
}


def create_unicode_pixmap(icon_name: str, size: QSize = QSize(16, 16), color: str = None) -> QPixmap:
    """
    Create a pixmap with a Unicode character rendered on it.
    
    Args:
        icon_name: Name of the icon (e.g., 'check', 'x', 'eye')
        size: Size of the pixmap
        color: Optional color override (hex string)
    
    Returns:
        QPixmap with the rendered Unicode character
    """
    symbol = ICONS.get(icon_name, '?')
    
    # Determine color
    if color is None:
        if 'chevron' in icon_name:
            color = COLORS.get('chevron', '#9ca3af')
        else:
            color = COLORS.get(icon_name, '#ffffff')
    
    # Create pixmap
    pixmap = QPixmap(size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    
    # Set font - use a size that fits well in the pixmap
    font = QFont()
    font.setPixelSize(int(size.height() * 0.85))
    font.setBold(True)
    painter.setFont(font)
    
    # Set color
    painter.setPen(QColor(color))
    
    # Draw centered
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, symbol)
    painter.end()
    
    return pixmap


def create_status_label(is_defeated: bool, size: QSize = QSize(16, 16)) -> QLabel:
    """Create a status label with check or X icon."""
    label = QLabel()
    icon_name = 'check' if is_defeated else 'x'
    label.setPixmap(create_unicode_pixmap(icon_name, size))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label


def create_icon_label(icon_name: str, size: QSize = QSize(16, 16), tooltip: str = None) -> QLabel:
    """Create a label with a Unicode icon."""
    label = QLabel()
    label.setPixmap(create_unicode_pixmap(icon_name, size))
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    if tooltip:
        label.setToolTip(tooltip)
    return label
