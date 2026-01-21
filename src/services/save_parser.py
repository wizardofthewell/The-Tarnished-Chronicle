# src/services/save_parser.py
"""
Pure Python parser for Elden Ring save files (.sl2/.co2)
Replaces the Rust CLI tool functionality.

Based on research from ER-Save-Lib and save file format documentation.
"""

import struct
import io
import os
import urllib.request
from typing import Optional, Tuple, List, Dict, Any


# Constants for event flag parsing
FLAG_DIVISOR = 1000
BLOCK_SIZE = 125

# Event flag block map - loaded from ER-Save-Lib BST file
# This maps block IDs to offsets in the event flags array
_EVENT_FLAG_BLOCK_MAP: Optional[Dict[int, int]] = None
_BST_URL = "https://raw.githubusercontent.com/ClayAmore/ER-Save-Lib/master/src/res/eventflag_bst.txt"


def _get_cache_dir() -> str:
    """Get the cache directory for storing the BST file."""
    # Use a temp directory relative to this script
    cache_dir = os.path.join(os.path.dirname(__file__), '.cache')
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def _load_bst_from_file(file_path: str) -> Dict[int, int]:
    """Load BST mapping from a local file."""
    bst_map = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if ',' in line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        bst_map[int(parts[0])] = int(parts[1])
    except Exception as e:
        print(f"Error loading BST from {file_path}: {e}")
    return bst_map


def _download_bst() -> Dict[int, int]:
    """Download the BST file from ER-Save-Lib GitHub."""
    bst_map = {}
    try:
        print("Downloading event flag BST from ER-Save-Lib...")
        with urllib.request.urlopen(_BST_URL, timeout=15) as response:
            bst_content = response.read().decode('utf-8')
            
            # Parse the content
            for line in bst_content.strip().split('\n'):
                if ',' in line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        bst_map[int(parts[0])] = int(parts[1])
            
            # Cache the file for future use
            cache_file = os.path.join(_get_cache_dir(), 'eventflag_bst.txt')
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(bst_content)
            print(f"BST downloaded and cached ({len(bst_map)} entries)")
            
    except Exception as e:
        print(f"Failed to download BST: {e}")
    
    return bst_map


def get_event_flag_block_map() -> Dict[int, int]:
    """Get the event flag block map, downloading if necessary."""
    global _EVENT_FLAG_BLOCK_MAP
    
    if _EVENT_FLAG_BLOCK_MAP is not None:
        return _EVENT_FLAG_BLOCK_MAP
    
    # Try to load from cache first
    cache_file = os.path.join(_get_cache_dir(), 'eventflag_bst.txt')
    if os.path.exists(cache_file):
        _EVENT_FLAG_BLOCK_MAP = _load_bst_from_file(cache_file)
        if _EVENT_FLAG_BLOCK_MAP:
            print(f"Loaded BST from cache ({len(_EVENT_FLAG_BLOCK_MAP)} entries)")
            return _EVENT_FLAG_BLOCK_MAP
    
    # Download from GitHub
    _EVENT_FLAG_BLOCK_MAP = _download_bst()
    
    if not _EVENT_FLAG_BLOCK_MAP:
        print("WARNING: Could not load event flag BST - boss tracking will not work!")
        _EVENT_FLAG_BLOCK_MAP = {}
    
    return _EVENT_FLAG_BLOCK_MAP

# Save file structure offsets (for PC version)
SAVE_HEADER_SIZE = 0x30C  # Header with checksum and magic
SLOT_SIZE = 0x280010  # Size of each character slot

# Profile summary is at a FIXED location in the file (not per-slot)
PROFILE_SUMMARY_BASE = 0x1901D00  # Base offset for profile summary section
PROFILE_ENTRY_SIZE = 0x24C  # 588 bytes per profile entry

# Profile entry structure offsets (relative to entry start)
PROFILE_NAME_OFFSET = 0x0E  # Character name (UTF-16LE, 32 bytes max)
PROFILE_LEVEL_OFFSET = 0x30  # Character level (4 bytes, little-endian)
PROFILE_PLAYTIME_OFFSET = 0x34  # Play time in seconds (4 bytes, little-endian)

# Event flags configuration  
EVENT_FLAGS_SIZE = 0x1BF99F  # Event flags section size (~1.83MB per slot)
EVENT_FLAGS_SLOT_OFFSET = 0x389F8  # Offset of event flags within each character slot


class EldenRingSaveParser:
    """Parser for Elden Ring save files (.sl2/.co2)"""
    
    def __init__(self):
        self._data: Optional[bytes] = None
        self._file_path: Optional[str] = None
        
    def load_file(self, file_path: str) -> Tuple[bool, Optional[str]]:
        """Load a save file into memory."""
        try:
            with open(file_path, 'rb') as f:
                self._data = f.read()
            self._file_path = file_path
            
            # Basic validation
            if len(self._data) < SAVE_HEADER_SIZE:
                return False, "File too small to be a valid save file"
            
            # Check magic bytes (BND4 or save file magic)
            magic = self._data[:4]
            if magic not in [b'BND4', b'\x00\x00\x00\x00']:
                # More flexible check - look for valid save structure
                pass
                
            return True, None
        except FileNotFoundError:
            return False, f"File not found: {file_path}"
        except PermissionError:
            return False, f"Permission denied: {file_path}"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
    
    def _find_event_flags_base(self, slot_index: int) -> Optional[int]:
        """
        Get the event flags base offset for a character slot.
        
        The event flags are stored at a fixed offset (0x389F8) within each 
        character slot. This offset was discovered through calibration with
        known boss event flags using the BST (block->offset) mapping algorithm.
        """
        if self._data is None:
            return None
        
        # Calculate the event flags base: slot start + fixed offset
        slot_start = self._get_slot_offset(slot_index)
        event_flags_base = slot_start + EVENT_FLAGS_SLOT_OFFSET
        
        # Validate the offset is within bounds
        if event_flags_base >= len(self._data):
            return None
        
        return event_flags_base
    
    def _get_slot_offset(self, slot_index: int) -> int:
        """Calculate the byte offset for a character slot."""
        # PC save structure: Header at 0x310, then character slots
        # Each slot is SLOT_SIZE (0x280010) bytes
        # Slots are numbered 0-9 for up to 10 characters
        base_offset = 0x310  # After checksum and header
        return base_offset + (slot_index * SLOT_SIZE)
    
    def _read_utf16_string(self, offset: int, max_length: int = 32) -> str:
        """Read a null-terminated UTF-16LE string from the save data."""
        if self._data is None:
            return ""
        
        try:
            # Read max_length characters (2 bytes each for UTF-16)
            raw = self._data[offset:offset + max_length * 2]
            # Find null terminator
            null_pos = raw.find(b'\x00\x00')
            if null_pos != -1:
                # Make sure we're at an even boundary
                if null_pos % 2 == 1:
                    null_pos += 1
                raw = raw[:null_pos]
            return raw.decode('utf-16-le', errors='ignore').rstrip('\x00')
        except Exception:
            return ""
    
    def _read_uint32(self, offset: int) -> int:
        """Read a 4-byte unsigned integer (little-endian)."""
        if self._data is None or offset + 4 > len(self._data):
            return 0
        return struct.unpack('<I', self._data[offset:offset + 4])[0]
    
    def _read_uint8(self, offset: int) -> int:
        """Read a single byte."""
        if self._data is None or offset >= len(self._data):
            return 0
        return self._data[offset]
    
    def list_characters(self) -> Tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        List all characters in the save file.
        Returns a list of character info dicts or an error message.
        
        Character data is read from the profile summary section which is at a 
        fixed location (0x1901D00) with each entry being 0x24C (588) bytes.
        """
        if self._data is None:
            return None, "No save file loaded"
        
        characters = []
        
        # Elden Ring supports up to 10 character slots
        for slot_idx in range(10):
            try:
                # Profile summary entries are at a fixed base, sequential
                entry_offset = PROFILE_SUMMARY_BASE + (slot_idx * PROFILE_ENTRY_SIZE)
                
                # Check if entry is within file bounds
                if entry_offset + PROFILE_ENTRY_SIZE > len(self._data):
                    break
                
                # Read character name at entry + 0x0E (UTF-16LE, 32 bytes max = 16 chars)
                name_offset = entry_offset + PROFILE_NAME_OFFSET
                char_name = self._read_utf16_string(name_offset, 16)
                
                if not char_name:
                    # Empty slot - skip
                    continue
                
                # Read character level at entry + 0x30
                level_offset = entry_offset + PROFILE_LEVEL_OFFSET
                level = self._read_uint32(level_offset)
                
                # Read play time at entry + 0x34 (in seconds)
                time_offset = entry_offset + PROFILE_PLAYTIME_OFFSET
                play_time = self._read_uint32(time_offset)
                
                # Deaths are not in profile summary - would need to read from slot data
                deaths = 0
                
                if char_name:  # Only add if we found a valid character
                    characters.append({
                        'slot_index': slot_idx,
                        'character_name': char_name,
                        'character_level': level,
                        'deaths': deaths,
                        'seconds_played': play_time
                    })
            except Exception as e:
                print(f"Error reading slot {slot_idx}: {e}")
                continue
        
        if not characters:
            return None, "No characters found in save file. The file may be corrupted or in an unsupported format."
        
        return characters, None
    
    def get_event_flag(self, slot_index: int, event_id: int) -> Tuple[Optional[bool], Optional[str]]:
        """
        Check if an event flag is set for a character.
        
        Args:
            slot_index: Character slot index (0-9)
            event_id: The event ID to check (e.g., boss defeat flags)
            
        Returns:
            Tuple of (flag_value, error_message)
        """
        if self._data is None:
            return None, "No save file loaded"
        
        try:
            # Get the BST map (downloads if needed)
            bst_map = get_event_flag_block_map()
            
            # Calculate block and bit position
            block = event_id // FLAG_DIVISOR
            index = event_id - block * FLAG_DIVISOR
            
            # Look up block in the map
            if block not in bst_map:
                return None, f"Event ID {event_id} not found in flag map (block {block})"
            
            block_offset = bst_map[block]
            offset = block_offset * BLOCK_SIZE
            
            byte_index = index // 8
            bit_index = 7 - (index - byte_index * 8)
            
            # Find the event flags base for this slot (searches dynamically)
            event_flags_start = self._find_event_flags_base(slot_index)
            if event_flags_start is None:
                return None, f"Could not find event flags for slot {slot_index}"
            
            flag_byte_offset = event_flags_start + offset + byte_index
            
            if flag_byte_offset >= len(self._data):
                return None, f"Offset {flag_byte_offset} out of bounds"
            
            flag_byte = self._data[flag_byte_offset]
            flag_value = ((flag_byte >> bit_index) & 1) == 1
            
            return flag_value, None
            
        except Exception as e:
            return None, f"Error reading event flag: {str(e)}"
    
    def get_boss_statuses(self, slot_index: int, event_ids: List[int]) -> Tuple[Optional[Dict[str, bool]], Optional[str]]:
        """
        Get the defeat status of multiple bosses.
        
        Args:
            slot_index: Character slot index (0-9)
            event_ids: List of boss event IDs to check
            
        Returns:
            Tuple of (dict mapping event_id_str -> defeated_bool, error_message)
        """
        if self._data is None:
            return None, "No save file loaded"
        
        statuses = {}
        errors = []
        
        for event_id in event_ids:
            result, err = self.get_event_flag(slot_index, event_id)
            if err:
                errors.append(f"Event {event_id}: {err}")
                statuses[str(event_id)] = False
            else:
                statuses[str(event_id)] = result if result is not None else False
        
        if errors and len(errors) == len(event_ids):
            return None, "; ".join(errors[:3])  # Return first 3 errors
        
        return statuses, None
    
    def get_character_stats(self, slot_index: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Get stats for a specific character.
        
        Args:
            slot_index: Character slot index (0-9)
            
        Returns:
            Tuple of (stats_dict, error_message)
        """
        if self._data is None:
            return None, "No save file loaded"
        
        try:
            # Read from profile summary (same location as list_characters)
            entry_offset = PROFILE_SUMMARY_BASE + (slot_index * PROFILE_ENTRY_SIZE)
            
            # Read character name
            name_offset = entry_offset + PROFILE_NAME_OFFSET
            char_name = self._read_utf16_string(name_offset, 16)
            
            # Read level at entry + 0x30
            level_offset = entry_offset + PROFILE_LEVEL_OFFSET
            level = self._read_uint32(level_offset)
            
            # Read play time at entry + 0x34 (in seconds)
            time_offset = entry_offset + PROFILE_PLAYTIME_OFFSET
            play_time = self._read_uint32(time_offset)
            
            # Deaths - not stored in profile summary, would need slot-specific location
            # For now return 0, can be enhanced later if offset is found
            deaths = 0
            
            stats = {
                'character_name': char_name,
                'deaths': deaths,
                'seconds_played': play_time,
                'level': level
            }
            
            return stats, None
            
        except Exception as e:
            return None, f"Error reading character stats: {str(e)}"
    
    def get_full_status(self, slot_index: int, event_ids: List[int]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Get complete status for a character including stats and boss flags.
        This mirrors the Rust CLI get-full-status command.
        
        Args:
            slot_index: Character slot index (0-9)
            event_ids: List of boss event IDs to check
            
        Returns:
            Tuple of (full_status_dict, error_message)
        """
        if self._data is None:
            return None, "No save file loaded"
        
        # Get character stats
        stats, stats_err = self.get_character_stats(slot_index)
        if stats_err:
            stats = {'deaths': 0, 'seconds_played': 0, 'level': 1}
        
        # Get boss statuses
        boss_statuses, boss_err = self.get_boss_statuses(slot_index, event_ids)
        if boss_err:
            return None, boss_err
        
        return {
            'stats': stats,
            'boss_statuses': boss_statuses
        }, None


class SaveParserHandler:
    """
    Drop-in replacement for RustCliHandler that uses pure Python parsing.
    """
    
    def __init__(self, cli_path_placeholder=None):
        # cli_path_placeholder is ignored - we don't need external tools
        self._parser = EldenRingSaveParser()
        self._current_file: Optional[str] = None
        print("Using Python save parser (no Rust CLI required)")
    
    def is_cli_available(self) -> bool:
        """Always returns True since we use pure Python."""
        return True
    
    def list_characters(self, save_file_path: str) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all characters in the save file.
        Compatible with RustCliHandler interface.
        """
        # Load file if needed
        if self._current_file != save_file_path:
            success, err = self._parser.load_file(save_file_path)
            if not success:
                return None, err
            self._current_file = save_file_path
        
        return self._parser.list_characters()
    
    def get_full_status(self, save_file_path: str, slot_index: int, event_ids: List[int]) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get full character status including stats and boss flags.
        Compatible with RustCliHandler interface.
        """
        # Load file if needed  
        if self._current_file != save_file_path:
            success, err = self._parser.load_file(save_file_path)
            if not success:
                return None, err
            self._current_file = save_file_path
        
        return self._parser.get_full_status(slot_index, event_ids)


# For backwards compatibility, alias the class
PythonSaveHandler = SaveParserHandler
