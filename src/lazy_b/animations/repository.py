"""Repository layer for animation file system operations."""

import logging
import re
from pathlib import Path
from typing import List, Optional, Tuple

from .types import (
    AnimationConfig,
    AnimationFrame,
    AnimationMetadata,
    AnimationSequence,
)

logger = logging.getLogger(__name__)


class FileSystemAnimationRepository:
    """Repository implementation for file system based animation storage."""

    def __init__(self, config: AnimationConfig) -> None:
        self._config = config
        # Support both formats: "001_description.txt" and "frame_1.txt"
        self._frame_pattern = re.compile(r"^(?:(\d+)_.*|.*_(\d+))\.txt$")

    def discover_animations(self, root_dir: Optional[Path] = None) -> List[Path]:
        """Discover all valid animation directories."""
        search_dir = root_dir or self._config.animation_root_dir

        if search_dir is None or not search_dir.exists():
            logger.warning(f"Animation directory {search_dir} does not exist")
            return []

        animation_dirs: List[Path] = []

        for item in search_dir.iterdir():
            if item.is_dir() and self._is_valid_animation_directory(item):
                animation_dirs.append(item)

        return sorted(animation_dirs, key=lambda p: p.name)

    def load_animation(self, directory: Path) -> AnimationSequence:
        """Load animation from directory and build domain tree."""
        if not directory.exists():
            raise FileNotFoundError(f"Animation directory {directory} not found")

        frame_files = self._discover_frame_files(directory)
        if not frame_files:
            raise ValueError(f"No valid frame files found in {directory}")

        frames = self._build_animation_frames(frame_files)
        metadata = self._build_metadata(directory, len(frames))

        return AnimationSequence(metadata=metadata, frames=frames)

    def _is_valid_animation_directory(self, directory: Path) -> bool:
        """Validate if directory contains valid animation files."""
        frame_files = list(directory.glob("*.txt"))
        return len(frame_files) > 0 and any(
            self._frame_pattern.match(f.name) for f in frame_files
        )

    def _discover_frame_files(self, directory: Path) -> List[Path]:
        """Discover and sort frame files by sequence number."""
        frame_files: List[Tuple[int, Path]] = []

        for file_path in directory.glob("*.txt"):
            match = self._frame_pattern.match(file_path.name)
            if match:
                # Extract sequence number from either group 1 or 2
                sequence_num = int(match.group(1) or match.group(2))
                frame_files.append((sequence_num, file_path))

        # Sort by sequence number
        frame_files.sort(key=lambda x: x[0])

        # Validate sequence continuity
        self._validate_sequence_continuity([seq for seq, _ in frame_files])

        return [path for _, path in frame_files]

    def _validate_sequence_continuity(self, sequences: List[int]) -> None:
        """Validate that frame sequences are continuous."""
        if not sequences:
            return

        expected_sequence = list(range(1, len(sequences) + 1))
        if sequences != expected_sequence:
            missing = set(expected_sequence) - set(sequences)
            if missing:
                raise ValueError(f"Missing frame sequences: {sorted(missing)}")

    def _build_animation_frames(self, frame_files: List[Path]) -> List[AnimationFrame]:
        """Build AnimationFrame objects from file paths."""
        frames: List[AnimationFrame] = []

        for i, file_path in enumerate(frame_files, 1):
            try:
                content = file_path.read_text(encoding="utf-8")
                frame = AnimationFrame(
                    sequence=i,
                    content=content,
                    duration=None,  # Use default from config
                )
                frames.append(frame)
            except UnicodeDecodeError as e:
                logger.error(f"Failed to read frame file {file_path}: {e}")
                raise ValueError(f"Invalid encoding in frame file {file_path}") from e

        return frames

    def _build_metadata(self, directory: Path, frame_count: int) -> AnimationMetadata:
        """Build AnimationMetadata from directory information."""
        return AnimationMetadata(
            id=directory.name,
            name=directory.name.replace("_", " ").title(),
            frame_count=frame_count,
            frame_rate=self._config.default_frame_rate,
            directory=directory,
        )
