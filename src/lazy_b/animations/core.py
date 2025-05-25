"""Core animation engine - Domain Layer."""

import logging
import os
import platform
import time
from typing import List, Optional

from .repository import FileSystemAnimationRepository
from .types import (
    AnimationConfig,
    AnimationFrame,
    AnimationRenderer,
    AnimationSequence,
    PlaybackResult,
)

logger = logging.getLogger(__name__)


class TerminalRenderer:
    """Terminal-specific animation renderer."""

    def __init__(self) -> None:
        self._clear_command = "cls" if platform.system() == "Windows" else "clear"

    def render_frame(self, frame: AnimationFrame) -> None:
        """Render a single frame to terminal."""
        print(frame.content)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system(self._clear_command)


class AnimationEngine:
    """Core animation playback engine."""

    def __init__(
        self,
        config: Optional[AnimationConfig] = None,
        renderer: Optional[AnimationRenderer] = None,
    ) -> None:
        self._config = config or AnimationConfig()
        self._renderer = renderer or TerminalRenderer()
        self._repository = FileSystemAnimationRepository(self._config)
        self._is_playing = False

    def discover_animations(self) -> List[str]:
        """Discover all available animation names."""
        animation_dirs = self._repository.discover_animations()
        return [directory.name for directory in animation_dirs]

    def load_animation(self, animation_id: str) -> Optional[AnimationSequence]:
        """Load a specific animation by ID."""
        animation_dirs = self._repository.discover_animations()

        for directory in animation_dirs:
            if directory.name == animation_id:
                try:
                    return self._repository.load_animation(directory)
                except Exception as e:
                    logger.error(f"Failed to load animation {animation_id}: {e}")
                    return None

        logger.warning(f"Animation {animation_id} not found")
        return None

    def play_animation(
        self, animation: AnimationSequence, loop: bool = True
    ) -> PlaybackResult:
        """Play an animation sequence."""
        if not animation.frames:
            return ValueError("Animation has no frames")

        self._is_playing = True

        try:
            while self._is_playing:
                for frame in animation.frames:
                    if not self._is_playing:
                        break

                    self._renderer.clear_screen()
                    self._renderer.render_frame(frame)

                    # Use frame-specific duration or default
                    duration = frame.duration or animation.metadata.frame_rate
                    time.sleep(duration)

                if not loop:
                    break

        except KeyboardInterrupt:
            self.stop_animation()
        except Exception as e:
            logger.error(f"Error during animation playback: {e}")
            return e

        return True

    def stop_animation(self) -> None:
        """Stop current animation playback."""
        self._is_playing = False

    def preview_animation(
        self, animation: AnimationSequence, frames_to_show: int = 3
    ) -> PlaybackResult:
        """Preview first few frames of an animation."""
        if not animation.frames:
            return ValueError("Animation has no frames")

        preview_frames = animation.frames[:frames_to_show]

        try:
            for frame in preview_frames:
                self._renderer.clear_screen()
                self._renderer.render_frame(frame)
                time.sleep(animation.metadata.frame_rate)

        except Exception as e:
            logger.error(f"Error during animation preview: {e}")
            return e

        return True
