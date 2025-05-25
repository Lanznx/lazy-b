"""Utility functions for animation system."""

import sys
from pathlib import Path
from typing import Optional


def find_animations_directory() -> Optional[Path]:
    """Find the animations directory, checking multiple possible locations."""
    # Possible locations to check
    possible_paths = [
        # Current working directory (for development)
        Path.cwd() / "animations",
        # Relative to the module (for development)
        Path(__file__).parent.parent.parent.parent / "animations",
        # Package data location (after installation)
        Path(sys.prefix) / "animations",
        # Site-packages data location (pip install)
        Path(__file__).parent.parent.parent / "animations",
        # Alternative site-packages location
        Path(sys.prefix) / "share" / "lazy-b" / "animations",
    ]

    # Check each possible path
    for path in possible_paths:
        if path.exists() and path.is_dir():
            # Verify it contains animation directories
            if any(item.is_dir() for item in path.iterdir()):
                return path

    return None


def get_default_animations_path() -> Path:
    """Get the default path for animations, with fallback."""
    found_path = find_animations_directory()
    if found_path:
        return found_path

    # Fallback to current directory if nothing found
    return Path("animations")
