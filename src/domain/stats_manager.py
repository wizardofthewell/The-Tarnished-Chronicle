# src/stats_manager.py
import json
from PySide6.QtCore import QFile, QIODevice

# Hardcoded list of all stats files to be loaded from Qt Resources.
# This is necessary because we cannot list directories in a .qrc file.
STATS_FILES = [
    ":/data/Bosses_stats/academy_of_raya_lucaria_boss_stats.json",
    ":/data/Bosses_stats/ainsel_river_boss_stats.json",
    ":/data/Bosses_stats/altus_plateau_boss_stats.json",
    ":/data/Bosses_stats/caelid_boss_stats.json",
    ":/data/Bosses_stats/capital_outskirts_boss_stats.json",
    ":/data/Bosses_stats/consecrated_snowfield_boss_stats.json",
    ":/data/Bosses_stats/crumbling_farum_azula_boss_stats.json",
    ":/data/Bosses_stats/deeproot_depths_boss_stats.json",
    ":/data/Bosses_stats/dragonbarrow_boss_stats.json",
    ":/data/Bosses_stats/elden_throne_boss_stats.json",
    ":/data/Bosses_stats/forbidden_lands_boss_stats.json",
    ":/data/Bosses_stats/lake_of_rot_boss_stats.json",
    ":/data/Bosses_stats/leyndell_ashen_capital_boss_stats.json",
    ":/data/Bosses_stats/leyndell_royal_capital_boss_stats.json",
    ":/data/Bosses_stats/limgrave_boss_stats.json",
    ":/data/Bosses_stats/liurnia_of_the_lakes_boss_stats.json",
    ":/data/Bosses_stats/miquellas_haligtree_boss_stats.json",
    ":/data/Bosses_stats/mohgwyn_dynasty_mausoleum_boss_stats.json",
    ":/data/Bosses_stats/moonlight_altar_boss_stats.json",
    ":/data/Bosses_stats/mountaintops_of_the_giants_boss_stats.json",
    ":/data/Bosses_stats/mt_gelmir_boss_stats.json",
    ":/data/Bosses_stats/nokron_eternal_city_boss_stats.json",
    ":/data/Bosses_stats/siofra_river_boss_stats.json",
    ":/data/Bosses_stats/stormveil_castle_boss_stats.json",
    ":/data/Bosses_stats/weeping_peninsula_boss_stats.json",
    ":/data/Bosses_stats_DLC/abyssal_woods_boss_stats.json",
    ":/data/Bosses_stats_DLC/ancient_ruins_of_rauh_boss_stats.json",
    ":/data/Bosses_stats_DLC/cerulean_coast_boss_stats.json",
    ":/data/Bosses_stats_DLC/charos_hidden_grave_boss_stats.json",
    ":/data/Bosses_stats_DLC/enir_ilim_boss_stats.json",
    ":/data/Bosses_stats_DLC/gravesite_plain_boss_stats.json",
    ":/data/Bosses_stats_DLC/jagged_peak_boss_stats.json",
    ":/data/Bosses_stats_DLC/rauh_base_boss_stats.json",
    ":/data/Bosses_stats_DLC/scadu_altus_boss_stats.json",
    ":/data/Bosses_stats_DLC/scaduview_boss_stats.json"
]

class StatsManager:
    def __init__(self):
        self.stats_data = self._load_all_stats()

    def _normalize_key(self, text: str) -> str:
        """Creates a simplified, consistent key from a string by keeping only alphanumeric characters."""
        return "".join(filter(str.isalnum, text)).lower()

    def _filename_to_location_name(self, filename: str) -> str:
        """Extracts the base name from the stats file to be used as a location identifier."""
        base_name = filename.split('/')[-1] # Get the actual filename from the resource path
        return base_name.replace("_boss_stats.json", "")

    def _load_all_stats(self):
        """
        Loads all boss stats from the hardcoded list of Qt resource files.
        """
        all_stats = {}
        for filepath in STATS_FILES:
            location_name = self._filename_to_location_name(filepath)
            location_key = self._normalize_key(location_name)
            
            if location_key not in all_stats:
                all_stats[location_key] = {}
            
            qfile = QFile(filepath)
            if not qfile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
                print(f"Error: Cannot open resource file '{filepath}'")
                continue
            
            try:
                content = qfile.readAll().data().decode('utf-8')
                data = json.loads(content)
                for item in data:
                    boss_name = item.get("Encounter Name")
                    if boss_name:
                        boss_key = self._normalize_key(boss_name)
                        all_stats[location_key][boss_key] = item
            except (json.JSONDecodeError) as e:
                print(f"Error loading stats file '{filepath}': {e}")
            finally:
                qfile.close()
        
        return all_stats

    def get_stats_for_boss(self, boss_name: str) -> dict:
        """
        Gets stats for a specific boss by name.
        """
        boss_key = self._normalize_key(boss_name)
        for location_stats in self.stats_data.values():
            if boss_key in location_stats:
                return location_stats[boss_key]
        return {}

    def get_all_stats(self) -> dict:
        """Returns the entire dictionary of stats data, keyed by location."""
        return self.stats_data