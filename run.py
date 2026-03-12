#!/usr/bin/env python3
"""Convenience script to run the bot from the root directory."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import main

if __name__ == "__main__":
    main()