"""Personality loader and manager."""
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class PersonalityManager:
    """Manages bot personality configuration."""
    
    def __init__(self, config_path: str = "config/personality.json"):
        self.config_path = Path(config_path)
        self.personality: Dict[str, Any] = {}
        self.load_personality()
    
    def load_personality(self) -> None:
        """Load personality configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.personality = json.load(f)
            logger.info(f"Personality loaded: {self.personality.get('name', 'Unknown')}")
        except FileNotFoundError:
            logger.warning(f"Personality file not found: {self.config_path}")
            self._create_default_personality()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing personality file: {e}")
            self._create_default_personality()
    
    def _create_default_personality(self) -> None:
        """Create a default personality if none exists."""
        self.personality = {
            "name": "Anna",
            "system_prompt": "Du bist eine freundliche Person, die gerne chattet."
        }
        logger.info("Using default personality")
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the LLM."""
        return self.personality.get("system_prompt", "Du bist ein hilfreicher Chatbot.")
    
    def get_name(self) -> str:
        """Get the bot's persona name."""
        return self.personality.get("name", "Bot")
    
    def get_full_context(self) -> str:
        """Get full personality context for the LLM."""
        context_parts = []
        
        if "name" in self.personality:
            context_parts.append(f"Name: {self.personality['name']}")
        
        if "age" in self.personality:
            context_parts.append(f"Alter: {self.personality['age']}")
        
        if "occupation" in self.personality:
            context_parts.append(f"Beruf: {self.personality['occupation']}")
        
        if "background" in self.personality:
            context_parts.append(f"Hintergrund: {self.personality['background']}")
        
        if "interests" in self.personality:
            interests = ", ".join(self.personality['interests'])
            context_parts.append(f"Interessen: {interests}")
        
        return "\n".join(context_parts)