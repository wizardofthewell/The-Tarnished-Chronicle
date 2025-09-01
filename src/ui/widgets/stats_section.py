# src/ui/widgets/stats_section.py

from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QStackedWidget
from .icon_header import IconHeader
from .stats_section_designs import DefaultStatsDesign, CompactStatsDesign

class StatsSectionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)

        self.header = IconHeader(None, "Gameplay Stats", is_expandable=True)
        main_layout.addWidget(self.header)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("statsCard")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(self.content_frame)

        self.content_widget = QStackedWidget()
        self.content_widget.setObjectName("statsContent")
        self.content_widget.setStyleSheet("#statsContent { background-color: transparent; }")
        content_layout.addWidget(self.content_widget)

        self._init_designs()

        self.header.toggle_button.clicked.connect(self.toggle_expanded)
        self.set_expanded(True)

    def _init_designs(self):
        self.default_design = DefaultStatsDesign()
        self.content_widget.addWidget(self.default_design)

    def toggle_expanded(self):
        self.set_expanded(not self.content_frame.isVisible())

    def set_expanded(self, is_expanded):
        self.content_frame.setVisible(is_expanded)
        self.header.set_expanded(is_expanded)

    def update_stats(self, stats):
        for i in range(self.content_widget.count()):
            design = self.content_widget.widget(i)
            design.update_stats(stats)

    def update_playtime(self, seconds: int):
        """Passes a live time update to the current design."""
        for i in range(self.content_widget.count()):
            design = self.content_widget.widget(i)
            if hasattr(design, 'update_playtime'):
                design.update_playtime(seconds)
