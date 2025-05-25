"""ASCII Animation System for Terminal Interface."""

from .core import AnimationEngine
from .interactive_menu import InteractiveMenu
from .types import AnimationFrame, AnimationMetadata, AnimationSequence

__all__ = [
    "AnimationMetadata",
    "AnimationFrame",
    "AnimationSequence",
    "AnimationEngine",
    "InteractiveMenu",
]
