# src/boss_stats_dialog.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QGroupBox, QFormLayout, QDialogButtonBox, QWidget, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from ...utils import get_resource_path
from ..widgets.unicode_icons import create_unicode_pixmap

class BossStatsDialog(QDialog):
    """
    A dialog window to display detailed statistics (resistances and negations) for a boss.
    """
    def __init__(self, boss_data, parent=None):
        super().__init__(parent)
        self.boss_data = boss_data
        self.setWindowTitle(f"Details: {self.boss_data.get('name', 'N/A')}")
        self.setMinimumWidth(500)
        self.setObjectName("bossStatsDialog")

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Boss Name Title
        boss_name_label = QLabel(self.boss_data.get('name', 'N/A'))
        boss_name_label.setObjectName("dialogTitle")
        boss_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(boss_name_label)

        stats = self.boss_data.get("stats", {})

        # Special case for Radagon & Elden Beast
        if "phases" in stats:
            for phase_stats in stats["phases"]:
                phase_name = phase_stats.get("Encounter Name", "Phase")
                main_layout.addWidget(self._create_stats_widget(phase_name, phase_stats))
        else:
            # Default behavior for all other bosses
            main_layout.addWidget(self._create_stats_widget(self.boss_data.get('name', 'N/A'), stats))

        # Legend
        legend_layout = QHBoxLayout()
        legend_layout.setContentsMargins(10, 10, 10, 10)
        legend_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        weak_widget = QWidget()
        weak_widget.setObjectName("weakLegend")
        weak_layout = QHBoxLayout(weak_widget)
        weak_layout.setContentsMargins(8, 4, 8, 4)
        weak_widget.setStyleSheet("#weakLegend {border: 1px solid rgb(127, 204, 8); border-radius: 5px; padding: 5px;}")
        weak_icon = QLabel()
        weak_icon.setPixmap(create_unicode_pixmap('chevrons-down', QSize(16, 16)))
        weak_label = QLabel("Weakness")
        weak_layout.addWidget(weak_icon)
        weak_layout.addWidget(weak_label)

        strong_widget = QWidget()
        strong_widget.setObjectName("strongLegend")
        strong_layout = QHBoxLayout(strong_widget)
        strong_layout.setContentsMargins(8, 4, 8, 4)
        strong_widget.setStyleSheet("#strongLegend {border: 1px solid rgb(197, 7, 67); border-radius: 5px;}")
        strong_icon = QLabel()
        strong_icon.setPixmap(create_unicode_pixmap('chevrons-up', QSize(16, 16)))
        strong_label = QLabel("Strength")
        strong_layout.addWidget(strong_icon)
        strong_layout.addWidget(strong_label)

        legend_layout.addWidget(weak_widget)
        legend_layout.addSpacing(20)
        legend_layout.addWidget(strong_widget)

        main_layout.addLayout(legend_layout)

        # OK Button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        main_layout.addWidget(button_box, 0, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def _create_stats_widget(self, name, stats):
        """Creates a widget containing the stats for one boss/phase."""
        container_widget = QWidget()
        main_layout = QVBoxLayout(container_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Add a subtitle for multi-phase bosses
        if "phases" in self.boss_data.get("stats", {}):
            part_label = QLabel(name)
            part_label.setObjectName("dialogSubTitle")
            part_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(part_label)

        columns_container = QWidget()
        columns_layout = QHBoxLayout(columns_container)
        columns_layout.setSpacing(15)

        # Add HP and Runes at the top
        hp_runes_layout = QHBoxLayout()
        hp_runes_layout.setContentsMargins(170, 0, 170, 0)

        hp_icon = QLabel()
        hp_icon.setPixmap(QIcon(get_resource_path("assets/images/HP.png")).pixmap(QSize(24, 24)))
        hp_label = QLabel(f"<b>{stats.get('HP', '-')}</b>")
        hp_runes_layout.addWidget(hp_icon)
        hp_runes_layout.addWidget(hp_label)
        
        hp_runes_layout.addStretch()

        runes_icon = QLabel()
        runes_icon.setPixmap(QIcon(get_resource_path("assets/images/Runes.png")).pixmap(QSize(24, 24)))
        runes_label = QLabel(f"<b>{stats.get('Runes', '-')}</b>")
        hp_runes_layout.addWidget(runes_icon)
        hp_runes_layout.addWidget(runes_label)

        main_layout.addLayout(hp_runes_layout)

        negation_group = QGroupBox("Damage Negation")
        negation_layout = QVBoxLayout(negation_group)
        negation_layout.setSpacing(6)
        negation_keys = {
            "Standard": "Standard Negation", "Slash": "Slash Negation",
            "Strike": "Strike Negation", "Pierce": "Pierce Negation",
            "Magic": "Magic Negation", "Fire": "Fire Negation",
            "Lightning": "Lightning Negation", "Holy": "Holy Negation"
        }
        
        negation_stats = {k: stats.get(v) for k, v in negation_keys.items() if stats.get(v) is not None}
        weak_dmg, strong_dmg = self._get_weak_strong_damages(negation_stats)

        for display_name, json_key in negation_keys.items():
            value = stats.get(json_key, "-")
            row = self._create_icon_stat_row(get_resource_path(f"assets/images/{display_name} Damage.png"), display_name, value, json_key, weak_dmg, strong_dmg)
            negation_layout.addWidget(row)
        negation_layout.addStretch()
        columns_layout.addWidget(negation_group)

        resistances_group = QGroupBox("Resistances")
        resistances_layout = QVBoxLayout(resistances_group)
        resistances_layout.setSpacing(6)
        resistance_keys = {
            "Poison": "Poison", "Scarlet Rot": "Rot", "Hemorrhage": "Blood",
            "Frostbite": "Frost", "Sleep": "Sleep", "Madness": "Madness"
        }
        
        resistance_stats = {k: stats.get(v) for k, v in resistance_keys.items() if stats.get(v) is not None}
        weak_res, strong_res, immune_res = self._get_weak_strong_status(resistance_stats)

        for display_name, json_key in resistance_keys.items():
            value = stats.get(json_key, "-")
            icon_name = display_name.replace(" ", "_")
            if display_name == "Scarlet Rot":
                icon_name = "Scarlet Rot"
            row = self._create_icon_stat_row(get_resource_path(f"assets/images/{icon_name}.png"), display_name, value, json_key, weak_res, strong_res, immune_res, is_resistance=True)
            resistances_layout.addWidget(row)
        resistances_layout.addStretch()
        columns_layout.addWidget(resistances_group)
        
        main_layout.addWidget(columns_container)
        return container_widget

    def _get_weak_strong_damages(self, negations: dict):
        # Filter out non-numeric values before sorting
        numeric_negations = {k: v for k, v in negations.items() if isinstance(v, (int, float))}
        if not numeric_negations:
            return [], []
        
        sorted_types = sorted(numeric_negations.items(), key=lambda x: x[1])
        lowest_val = sorted_types[0][1]
        highest_val = sorted_types[-1][1]

        # Avoid marking everything as weak/strong if all values are the same
        if lowest_val == highest_val:
            return [], []

        lowest = [k for k, v in sorted_types if v == lowest_val]
        highest = [k for k, v in sorted_types if v == highest_val]
        return lowest, highest

    def _get_weak_strong_status(self, resistances: dict):
        numeric = {k: int(v) for k, v in resistances.items() if isinstance(v, str) and v.isdigit()}
        numeric.update({k: v for k, v in resistances.items() if isinstance(v, (int, float))})
        immune = [k for k, v in resistances.items() if v == "IMMUNE"]

        if not numeric:
            return [], [], immune

        sorted_status = sorted(numeric.items(), key=lambda x: x[1])
        
        if not sorted_status:
            return [], [], immune

        lowest_val = sorted_status[0][1]
        highest_val = sorted_status[-1][1]

        if lowest_val == highest_val:
            return list(numeric.keys()), [], immune

        # For resistances, a lower value is a weakness.
        weakest = [k for k, v in sorted_status if v == lowest_val]
        strongest = [k for k, v in sorted_status if v == highest_val]
        
        return weakest, strongest, immune

    def _create_icon_stat_row(self, icon_path, name, value, json_key, weak_list, strong_list, immune_list=None, is_resistance=False):
        """Creates a QHBoxLayout for a stat row with an icon and weakness/strength indicators."""
        row_widget = QWidget()
        row_layout = QHBoxLayout(row_widget)
        if is_resistance:
            row_layout.setContentsMargins(5, 2, 5, 2)
        else:
            row_layout.setContentsMargins(5, 2, 5, 2)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon_path).pixmap(QSize(24, 24)))
        
        name_label = QLabel(f"<b>{name}:</b>")
        name_label.setStyleSheet("background-color: transparent;")
        value_label = QLabel(str(value))
        value_label.setStyleSheet("background-color: transparent;")
        
        indicator_label = QLabel()
        indicator_label.setFixedSize(QSize(16, 16))
        indicator_label.setStyleSheet("background-color: transparent;")

        if name in weak_list:
            indicator_label.setPixmap(create_unicode_pixmap('chevrons-down', QSize(16, 16)))
            value_label.setStyleSheet("color: rgb(127, 204, 8); font-weight: bold; background-color: transparent;")
            row_widget.setStyleSheet("QWidget#rowWidget {background-color: rgba(127, 204, 8, 0.1); border-radius: 5px;}")
            row_widget.setObjectName("rowWidget")
        elif name in strong_list:
            indicator_label.setPixmap(create_unicode_pixmap('chevrons-up', QSize(16, 16)))
            value_label.setStyleSheet("color: rgb(197, 7, 67); font-weight: bold; background-color: transparent;")
            row_widget.setStyleSheet("QWidget#rowWidget {background-color: rgba(197, 7, 67, 0.1); border-radius: 5px;}")
            row_widget.setObjectName("rowWidget")

        row_layout.addWidget(icon_label)
        row_layout.addWidget(name_label)
        row_layout.addWidget(indicator_label)
        row_layout.addStretch()
        row_layout.addWidget(value_label)
        
        return row_widget
