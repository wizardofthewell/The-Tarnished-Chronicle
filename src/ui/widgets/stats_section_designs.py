# src/ui/widgets/stats_section_designs.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from .icon_header import IconHeader
from ...utils import format_seconds_to_hms, get_resource_path

class BaseStatsDesign(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def update_stats(self, stats_data):
        raise NotImplementedError

class DefaultStatsDesign(BaseStatsDesign):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("defaultStats")
        self.setStyleSheet("""
            #defaultStats {
                background-color: transparent;
            }
        """)
        
        # Main container layout
        main_container = QHBoxLayout(self)
        main_container.setContentsMargins(0, 0, 0, 0)
        
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.grid_layout.setSpacing(10)
        
        main_container.addLayout(self.grid_layout)

        # Table Header
        headers = ["", "Live", "Defeated", "Total"]
        for i, header_text in enumerate(headers):
            header_label = QLabel(header_text)
            header_label.setObjectName("statsTableHeader")
            self.grid_layout.addWidget(header_label, 0, i, Qt.AlignmentFlag.AlignCenter)

        # Table Rows
        self.base_game_labels = self._create_row("Base Game", 1)
        self.dlc_labels = self._create_row("DLC", 2)
        self.total_labels = self._create_row("Total", 3)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setObjectName("statsDivider")
        self.grid_layout.addWidget(divider, 4, 0, 1, 4)

        # General Stats
        self.playtime_label = self._create_general_stat(get_resource_path("assets/icons/clock.svg"), "Playtime:", 5)
        self.deaths_label = self._create_general_stat(get_resource_path("assets/icons/skull-and-crossbones.svg"), "Deaths:", 6)

    def _create_general_stat(self, icon_path, name, row):
        header = IconHeader(icon_path, name, is_expandable=False)
        value_label = QLabel("--")
        self.grid_layout.addWidget(header, row, 0, 1, 3)
        self.grid_layout.addWidget(value_label, row, 3, Qt.AlignmentFlag.AlignRight)
        return value_label

    def _create_row(self, name, row):
        name_label = QLabel(name)
        live_label = QLabel("0")
        defeated_label = QLabel("0")
        total_label = QLabel("0")
        
        live_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        defeated_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout.addWidget(name_label, row, 0)
        self.grid_layout.addWidget(live_label, row, 1)
        self.grid_layout.addWidget(defeated_label, row, 2)
        self.grid_layout.addWidget(total_label, row, 3)
        
        return {"name": name_label, "live": live_label, "defeated": defeated_label, "total": total_label}

    def update_stats(self, stats):
        # General stats
        playtime = stats.get("seconds_played", 0)
        self.playtime_label.setText(format_seconds_to_hms(playtime))
        self.deaths_label.setText(str(stats.get("deaths", "--")))

        # Boss counts
        boss_counts = stats.get("boss_counts", {})
        
        base_counts = boss_counts.get("base", {})
        dlc_counts = boss_counts.get("dlc", {})
        total_counts = boss_counts.get("total", {})

        show_base_row = base_counts.get("total", 0) > 0
        show_dlc_row = dlc_counts.get("total", 0) > 0
        show_total_row = show_base_row and show_dlc_row

        # Base Game Row
        for widget in self.base_game_labels.values():
            widget.setVisible(show_base_row)
        if show_base_row:
            self.base_game_labels["live"].setText(str(base_counts.get("live", 0)))
            self.base_game_labels["defeated"].setText(str(base_counts.get("defeated", 0)))
            self.base_game_labels["total"].setText(str(base_counts.get("total", 0)))

        # DLC Row
        for widget in self.dlc_labels.values():
            widget.setVisible(show_dlc_row)
        if show_dlc_row:
            self.dlc_labels["live"].setText(str(dlc_counts.get("live", 0)))
            self.dlc_labels["defeated"].setText(str(dlc_counts.get("defeated", 0)))
            self.dlc_labels["total"].setText(str(dlc_counts.get("total", 0)))

        # Total Row
        for widget in self.total_labels.values():
            widget.setVisible(show_total_row)
        if show_total_row:
            self.total_labels["live"].setText(str(total_counts.get("live", 0)))
            self.total_labels["defeated"].setText(str(total_counts.get("defeated", 0)))
            self.total_labels["total"].setText(str(total_counts.get("total", 0)))

    def update_playtime(self, seconds: int):
        """Updates only the playtime label."""
        if seconds < 0:
            self.playtime_label.setText("--:--:--")
        else:
            self.playtime_label.setText(format_seconds_to_hms(seconds))

class CompactStatsDesign(BaseStatsDesign):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("compactStats")
        self.setStyleSheet("""
            #compactStats {
                background-color: transparent;
            }
        """)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(4)

        self.playtime_label = self._create_stat_label(get_resource_path("assets/icons/clock.svg"), "Playtime")
        self.deaths_label = self._create_stat_label(get_resource_path("assets/icons/skull-and-crossbones.svg"), "Deaths")
        self.bosses_label = self._create_stat_label(None, "Bosses")

    def _create_stat_label(self, icon_path, name):
        layout = QHBoxLayout()
        header = IconHeader(icon_path, name, is_expandable=False)
        value_label = QLabel("--")
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(header)
        layout.addWidget(value_label)
        self.layout.addLayout(layout)
        return value_label

    def update_stats(self, stats):
        playtime = stats.get("seconds_played", 0)
        self.playtime_label.setText(format_seconds_to_hms(playtime))
        self.deaths_label.setText(str(stats.get("deaths", "--")))
        
        boss_counts = stats.get("boss_counts", {}).get("total", {})
        defeated = boss_counts.get("defeated", 0)
        live = boss_counts.get("live", 0)
        total = boss_counts.get("total", 0)
        self.bosses_label.setText(f"{defeated}/{live}/{total}")