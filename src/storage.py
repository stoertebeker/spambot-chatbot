"""Storage handler for bot state persistence."""
import json
from pathlib import Path
from typing import Set, Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class BotStorage:
    """Handles persistent storage of bot state."""
    
    def __init__(self, filepath: str = "data/bot_state.json"):
        """Initialize storage.
        
        Args:
            filepath: Path to the JSON storage file
        """
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Storage initialized at: {self.filepath}")
    
    def save_state(
        self, 
        active_targets: Set[int], 
        style_examples: Dict[int, List[str]],
        conversation_history: Dict[int, List[Dict[str, str]]] = None
    ) -> None:
        """Save bot state to JSON file.
        
        Args:
            active_targets: Set of active chat IDs
            style_examples: Dictionary mapping chat IDs to style examples
            conversation_history: Optional conversation history to save
        """
        try:
            state = {
                "active_targets": list(active_targets),
                "style_examples": {str(k): v for k, v in style_examples.items()},
                "version": "2.0"
            }
            
            # Optionally save conversation history (can be large)
            if conversation_history:
                state["conversation_history"] = {
                    str(k): v for k, v in conversation_history.items()
                }
            
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, ensure_ascii=False)
            
            logger.info(
                f"State saved: {len(active_targets)} targets, "
                f"{len(style_examples)} style examples"
            )
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
            raise
    
    def load_state(self) -> Tuple[Set[int], Dict[int, List[str]]]:
        """Load bot state from JSON file.
        
        Returns:
            Tuple of (active_targets, style_examples)
        """
        if not self.filepath.exists():
            logger.info("No existing state file found, starting fresh")
            return set(), {}
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            active_targets = set(state.get("active_targets", []))
            
            # Convert string keys back to integers
            style_examples = {
                int(k): v 
                for k, v in state.get("style_examples", {}).items()
            }
            
            logger.info(
                f"State loaded: {len(active_targets)} targets, "
                f"{len(style_examples)} style examples"
            )
            
            return active_targets, style_examples
            
        except Exception as e:
            logger.error(f"Failed to load state: {e}")
            # Return empty state on error
            return set(), {}
    
    def clear_state(self) -> None:
        """Clear all saved state."""
        if self.filepath.exists():
            self.filepath.unlink()
            logger.info("State cleared")
    
    def save_session(self, session_string: str) -> None:
        """Save Telethon session string.
        
        Args:
            session_string: Telethon session string for persistent login
        """
        session_file = self.filepath.parent / "session.json"
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump({"session": session_string}, f)
            logger.info("Session string saved")
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    def load_session(self) -> str:
        """Load Telethon session string.
        
        Returns:
            Session string or empty string if not found
        """
        session_file = self.filepath.parent / "session.json"
        if not session_file.exists():
            return ""
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info("Session string loaded")
            return data.get("session", "")
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return ""