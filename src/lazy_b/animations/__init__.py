"""ASCII Animation System for Terminal Interface."""

from .types import AnimationMetadata, AnimationFrame, AnimationSequence
from .core import AnimationEngine
from .interactive_menu import InteractiveMenu

__all__ = [
    "AnimationMetadata",
    "AnimationFrame",
    "AnimationSequence",
    "AnimationEngine",
    "InteractiveMenu",
]
