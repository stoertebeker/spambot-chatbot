"""Timing configuration manager."""
import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class TimingManager:
    """Manages timing configuration for natural behavior."""
    
    def __init__(self, config_path: str = "config/timing.json"):
        """Initialize timing manager.
        
        Args:
            config_path: Path to timing configuration JSON file
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load timing configuration from JSON file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            logger.info(f"Timing configuration loaded from {self.config_path}")
        except FileNotFoundError:
            logger.warning(f"Timing config not found: {self.config_path}, using defaults")
            self._create_default_config()
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing timing config: {e}, using defaults")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create default timing configuration."""
        self.config = {
            "min_delay": 2.0,
            "max_delay": 8.0,
            "chars_per_second_min": 3.5,
            "chars_per_second_max": 6.0,
            "long_pause_chance": 0.15,
            "long_pause_min": 30,
            "long_pause_max": 180,
            "reading_delay_min": 1.0,
            "reading_delay_max": 3.0
        }
        
        # Save default config
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Default timing config saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save default config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get timing configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all timing configuration."""
        return self.config.copy()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Update timing configuration.
        
        Args:
            updates: Dictionary of configuration updates
        """
        self.config.update(updates)
        
        # Save updated config
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
            logger.info(f"Timing configuration updated: {updates}")
        except Exception as e:
            logger.error(f"Failed to save updated config: {e}")
            raise