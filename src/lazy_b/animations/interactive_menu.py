"""Interactive menu system for animation selection."""

import sys
import os
import time
import threading
import platform
from typing import List, Optional

from .types import AnimationSequence, AnimationConfig
from .repository import FileSystemAnimationRepository
from pathlib import Path


class InteractiveMenu:
    """Interactive menu with arrow key navigation and animation preview."""

    def __init__(self, config: AnimationConfig) -> None:
        self.config = config
        self.repository = FileSystemAnimationRepository(config)
        self.animations: List[AnimationSequence] = []
        self.current_index = 0
        self.preview_thread: Optional[threading.Thread] = None
        self.stop_preview = False

    def _get_char(self) -> str:
        """Get a single character from stdin."""
        try:
            if platform.system() == "Windows":
                import msvcrt

                char = msvcrt.getch().decode("utf-8")
                if char == "\xe0":  # Special key prefix on Windows
                    char += msvcrt.getch().decode("utf-8")
                return char
            else:
                import termios
                import tty

                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    char = sys.stdin.read(1)
                    if char == "\x1b":  # ESC sequence
                        char += sys.stdin.read(2)
                    return char
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except Exception:
            # Fallback to regular input
            return input()

    def _clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system("clear" if os.name != "nt" else "cls")

    def _load_animations(self) -> bool:
        """Load all available animations."""
        animation_dirs = self.repository.discover_animations()

        if not animation_dirs:
            return False

        self.animations = []
        for directory in animation_dirs:
            try:
                animation = self.repository.load_animation(directory)
                self.animations.append(animation)
            except Exception:
                continue  # Skip invalid animations

        return len(self.animations) > 0

    def _stop_current_preview(self) -> None:
        """Stop the current preview animation."""
        self.stop_preview = True
        if self.preview_thread and self.preview_thread.is_alive():
            self.preview_thread.join(timeout=0.5)

    def _start_preview(self, animation: AnimationSequence) -> None:
        """Start preview animation in a separate thread."""
        self._stop_current_preview()
        self.stop_preview = False

        def preview_loop():
            frame_index = 0
            while not self.stop_preview:
                if frame_index >= len(animation.frames):
                    frame_index = 0

                frame = animation.frames[frame_index]

                # Calculate preview area position
                preview_start_line = 6 + len(self.animations)

                # Clear preview area more thoroughly - clear 15 lines
                for i in range(15):
                    print(
                        f"\033[{preview_start_line + i};1H\033[2K", end=""
                    )  # Clear entire line

                # Position cursor and show title
                print(f"\033[{preview_start_line};1H", end="")
                print("Preview:")

                # Clean and display frame content
                # Remove trailing whitespace and newlines
                clean_content = frame.content.rstrip()
                frame_lines = clean_content.split("\n") if clean_content else []

                # Display each line, ensuring we clear any potential overlap
                for i, line in enumerate(frame_lines):
                    line_num = preview_start_line + 1 + i
                    # Move to line and clear it completely, then write content
                    print(f"\033[{line_num};1H\033[2K{line.rstrip()}", end="")

                sys.stdout.flush()

                frame_index += 1
                time.sleep(animation.metadata.frame_rate)

        self.preview_thread = threading.Thread(target=preview_loop, daemon=True)
        self.preview_thread.start()

    def _render_menu(self) -> None:
        """Render the interactive menu."""
        self._clear_screen()

        print("🎭 \033[1mWelcome to LazyB!\033[0m")
        print("Use ↑↓ arrows to select animation, Enter to start, or 'q' to quit")
        print("LazyB will press Shift every 3 minutes to keep your apps active.\n")

        for i, animation in enumerate(self.animations):
            if i == self.current_index:
                # Highlighted option
                print(f"🎬 \033[1;36m► {animation.metadata.name}\033[0m")
            else:
                # Normal option
                print(f"   {animation.metadata.name}")

        print()

        # Start preview for current selection
        if self.animations:
            current_animation = self.animations[self.current_index]
            self._start_preview(current_animation)

    def _handle_input(self) -> Optional[AnimationSequence]:
        """Handle user input and return selected animation or None if quit."""
        while True:
            char = self._get_char()

            if char == "q":
                return None
            elif char == "\r" or char == "\n":  # Enter
                return self.animations[self.current_index]
            elif char == "\x1b[A" or char == "\xe0H":  # Up arrow (Unix/Windows)
                self.current_index = (self.current_index - 1) % len(self.animations)
                self._render_menu()
            elif char == "\x1b[B" or char == "\xe0P":  # Down arrow (Unix/Windows)
                self.current_index = (self.current_index + 1) % len(self.animations)
                self._render_menu()

    def show_menu(self) -> Optional[AnimationSequence]:
        """Show interactive menu and return selected animation."""
        if not self._load_animations():
            print("❌ No animations found!")
            return None

        try:
            self._render_menu()
            selected = self._handle_input()
            self._stop_current_preview()
            return selected
        except KeyboardInterrupt:
            self._stop_current_preview()
            print("\n👋 Goodbye!")
            return None
        finally:
            self._clear_screen()


def create_interactive_menu(
    config: Optional[AnimationConfig] = None,
) -> InteractiveMenu:
    """Create and return an interactive menu instance."""
    if config is None:
        config = AnimationConfig(animation_root_dir=Path("animations"))
    return InteractiveMenu(config)
