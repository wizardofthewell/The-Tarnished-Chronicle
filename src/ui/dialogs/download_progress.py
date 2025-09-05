# src/ui/dialogs/download_progress.py

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtCore import Qt, Signal, Slot

class DownloadProgressDialog(QDialog):
    """Dialog showing download progress for updates"""
    
    # Signal emitted when user cancels
    cancelled = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Downloading Update")
        self.setModal(True)
        self.setFixedWidth(400)
        
        # Prevent closing with X button during download
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)
        
        # Layout
        layout = QVBoxLayout()
        
        # Status label
        self.status_label = QLabel("Preparing download...")
        layout.addWidget(self.status_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Size label
        self.size_label = QLabel("")
        self.size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.size_label)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.on_cancel)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)
        self._cancelled = False
    
    @Slot(int)
    def update_progress(self, value):
        """Update progress bar value (0-100)"""
        self.progress_bar.setValue(value)
        if value >= 100:
            self.status_label.setText("Download complete! Verifying...")
            self.cancel_button.setEnabled(False)
    
    @Slot(str)
    def update_status(self, status):
        """Update status message"""
        self.status_label.setText(status)
    
    @Slot(int, int)
    def update_size(self, downloaded, total):
        """Update size label with downloaded/total MB"""
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        self.size_label.setText(f"{downloaded_mb:.1f} MB / {total_mb:.1f} MB")
    
    def on_cancel(self):
        """Handle cancel button click"""
        self._cancelled = True
        self.cancelled.emit()
        self.close()
    
    def is_cancelled(self):
        """Check if download was cancelled"""
        return self._cancelled
    
    @Slot()
    def set_completed(self):
        """Set dialog to completed state"""
        self.status_label.setText("Update downloaded! Click 'Install Now' to begin installation.")
        self.progress_bar.setValue(100)
        self.cancel_button.setText("Install Now")
        self.cancel_button.setEnabled(True)
        self.cancel_button.clicked.disconnect()
        self.cancel_button.clicked.connect(self.accept)