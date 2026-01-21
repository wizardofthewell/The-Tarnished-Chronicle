# src/services/hybrid_save_handler.py
"""
Hybrid save file handler that tries Python parser first, 
then falls back to Rust CLI if needed.
"""

from typing import Optional, Tuple, List, Dict, Any
from .save_parser import SaveParserHandler
from .rust_cli_handler import RustCliHandler


class HybridSaveHandler:
    """
    Hybrid handler that tries the Python parser first for speed and reliability,
    then falls back to the Rust CLI if the Python parser fails.
    """
    
    def __init__(self, cli_path_placeholder="RUST_CLI_TOOL_PATH_PLACEHOLDER"):
        # Initialize both handlers
        self._python_handler = SaveParserHandler()
        self._rust_handler = RustCliHandler(cli_path_placeholder)
        self._use_rust_fallback = True  # Enable fallback by default
        self._last_used = "none"
        
        print("Initialized HybridSaveHandler (Python-first, Rust fallback)")
    
    def is_cli_available(self) -> bool:
        """Check if at least one handler is available."""
        # Python handler is always available
        return True
    
    def list_characters(self, save_file_path: str) -> Tuple[Optional[List[Dict]], Optional[str]]:
        """
        List all characters in the save file.
        Tries Python parser first, falls back to Rust CLI on failure.
        """
        # Try Python parser first
        try:
            result, err = self._python_handler.list_characters(save_file_path)
            if result is not None and len(result) > 0:
                self._last_used = "python"
                print(f"[HybridHandler] Successfully listed characters using Python parser")
                return result, None
            
            # Python parser returned empty or error
            if err:
                print(f"[HybridHandler] Python parser error: {err}")
        except Exception as e:
            print(f"[HybridHandler] Python parser exception: {e}")
        
        # Fall back to Rust CLI if available and enabled
        if self._use_rust_fallback and self._rust_handler.is_cli_available():
            print("[HybridHandler] Falling back to Rust CLI")
            try:
                result, err = self._rust_handler.list_characters(save_file_path)
                if result is not None:
                    self._last_used = "rust"
                    return result, err
            except Exception as e:
                print(f"[HybridHandler] Rust CLI exception: {e}")
                return None, f"Both parsers failed. Rust error: {e}"
        
        # If Rust is not available, return the Python error
        self._last_used = "none"
        return None, "Python parser could not read characters. Rust CLI not available as fallback."
    
    def get_full_status(self, save_file_path: str, slot_index: int, event_ids: List[int]) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get full character status including stats and boss flags.
        Tries Python parser first, falls back to Rust CLI on failure.
        """
        # Try Python parser first
        try:
            result, err = self._python_handler.get_full_status(save_file_path, slot_index, event_ids)
            if result is not None:
                self._last_used = "python"
                return result, None
            
            if err:
                print(f"[HybridHandler] Python parser error for get_full_status: {err}")
        except Exception as e:
            print(f"[HybridHandler] Python parser exception for get_full_status: {e}")
        
        # Fall back to Rust CLI if available and enabled
        if self._use_rust_fallback and self._rust_handler.is_cli_available():
            print("[HybridHandler] Falling back to Rust CLI for get_full_status")
            try:
                result, err = self._rust_handler.get_full_status(save_file_path, slot_index, event_ids)
                if result is not None:
                    self._last_used = "rust"
                    return result, err
            except Exception as e:
                print(f"[HybridHandler] Rust CLI exception: {e}")
                return None, f"Both parsers failed. Rust error: {e}"
        
        self._last_used = "none"
        return None, "Python parser failed. Rust CLI not available as fallback."
    
    def get_last_used_parser(self) -> str:
        """Returns which parser was last used: 'python', 'rust', or 'none'"""
        return self._last_used
    
    def disable_rust_fallback(self):
        """Disable Rust CLI fallback (Python only mode)"""
        self._use_rust_fallback = False
        print("[HybridHandler] Rust fallback disabled")
    
    def enable_rust_fallback(self):
        """Enable Rust CLI fallback"""
        self._use_rust_fallback = True
        print("[HybridHandler] Rust fallback enabled")
