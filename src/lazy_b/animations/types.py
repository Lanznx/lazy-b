"""Type definitions for ASCII Animation System."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Protocol, Union


@dataclass(frozen=True)
class AnimationMetadata:
    """Metadata for an animation sequence."""

    id: str
    name: str
    frame_count: int
    frame_rate: float
    directory: Path


@dataclass(frozen=True)
class AnimationFrame:
    """Represents a single frame in an animation sequence."""

    sequence: int
    content: str
    duration: Optional[float] = None


@dataclass(frozen=True)
class AnimationSequence:
    """Complete animation sequence with metadata and frames."""

    metadata: AnimationMetadata
    frames: List[AnimationFrame]


class AnimationLoader(Protocol):
    """Protocol for animation loading implementations."""

    def load_animation(self, directory: Path) -> AnimationSequence:
        """Load animation from directory."""
        ...

    def discover_animations(self, root_dir: Path) -> List[Path]:
        """Discover all valid animation directories."""
        ...


class AnimationRenderer(Protocol):
    """Protocol for animation rendering implementations."""

    def render_frame(self, frame: AnimationFrame) -> None:
        """Render a single frame to terminal."""
        ...

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        ...


@dataclass(frozen=True)
class AnimationConfig:
    """Configuration for animation playback."""

    default_frame_rate: float = 0.2
    animation_root_dir: Path = Path("animations")
    supported_extensions: Optional[List[str]] = None

    def __post_init__(self) -> None:
        if self.supported_extensions is None:
            object.__setattr__(self, "supported_extensions", [".txt"])


PlaybackResult = Union[bool, Exception]
