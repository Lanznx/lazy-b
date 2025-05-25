"""Integrated runner for LazyB with animation support."""

import threading
import time
from typing import Optional
from pathlib import Path

from .main import LazyB
from .animations.core import AnimationEngine
from .animations.types import AnimationConfig


class IntegratedLazyB:
    """Integrated LazyB runner with animation support."""

    def __init__(self, interval: int = 1, quiet: bool = False) -> None:
        self.interval = interval
        self.quiet = quiet
        self.lazy_b = LazyB(interval=interval)

        # Setup animation system
        config = AnimationConfig(animation_root_dir=Path("animations"))
        self.animation_engine = AnimationEngine(config)

        self._animation_thread: Optional[threading.Thread] = None
        self._is_running = False

    def print_status(self, message: str) -> None:
        """Print status messages if not in quiet mode."""
        if not self.quiet:
            print(message)

    def start_with_animation_menu(self) -> None:
        """Start with interactive animation selection, then keep active."""
        from .animations.interactive_menu import create_interactive_menu

        # Create and show interactive menu
        menu = create_interactive_menu(self.animation_engine._config)
        selected_animation = menu.show_menu()

        if selected_animation is None:
            # User quit or no animations available
            self.print_status("👋 Goodbye!")
            import sys

            sys.exit(0)

        # Start LazyB with selected animation
        self.print_status(
            f"✅ Starting LazyB with animation: {selected_animation.metadata.name}"
        )
        self._start_with_animation_sequence(selected_animation)

    def _start_with_animation_sequence(self, animation) -> None:
        """Start keeping active with provided animation sequence."""
        self._is_running = True

        # Start animation in separate thread
        def run_animation():
            while self._is_running:
                try:
                    result = self.animation_engine.play_animation(animation, loop=False)
                    if isinstance(result, Exception) or not self._is_running:
                        break
                except Exception:
                    break

        self._animation_thread = threading.Thread(target=run_animation, daemon=True)
        self._animation_thread.start()

        # Start keeping active
        self.print_status(f"\n🎬 Animation: {animation.metadata.name}")
        self.print_status(
            f"⌨️  LazyB will press Shift every {self.interval//60} minutes"
        )
        self.print_status("🛑 Press Ctrl+C to stop")

        self.lazy_b.start(callback=self.print_status)
        self.print_status(
            f"\n✅ LazyB is now active! Animation and key presses started."
        )
        self.print_status(f"📅 Next Shift press in {self.interval//60} minutes...")

    def start_with_animation(self, animation_name: str) -> None:
        """Start keeping active with specified animation."""
        animation = self.animation_engine.load_animation(animation_name)

        if not animation:
            self.print_status(
                f"Animation '{animation_name}' not found. Starting without animation..."
            )
            self.start_active_only()
            return

        self._is_running = True

        # Start animation in separate thread
        def run_animation():
            while self._is_running:
                try:
                    result = self.animation_engine.play_animation(animation, loop=False)
                    if isinstance(result, Exception) or not self._is_running:
                        break
                except Exception:
                    break

        self._animation_thread = threading.Thread(target=run_animation, daemon=True)
        self._animation_thread.start()

        # Start keeping active
        self.print_status(f"\n🎬 Animation: {animation.metadata.name}")
        self.print_status(
            f"⌨️  LazyB will press Shift every {self.interval//60} minutes"
        )
        self.print_status("🛑 Press Ctrl+C to stop")

        self.lazy_b.start(callback=self.print_status)
        self.print_status(
            f"\n✅ LazyB is now active! Animation and key presses started."
        )
        self.print_status(f"📅 Next Shift press in {self.interval//60} minutes...")

    def start_active_only(self) -> None:
        """Start keeping active without animation."""
        self.print_status(
            f"\n⌨️  LazyB will press Shift every {self.interval//60} minutes"
        )
        self.print_status("🛑 Press Ctrl+C to stop")

        self.lazy_b.start(callback=self.print_status)
        self.print_status(f"\n✅ LazyB is now active! (no animation)")
        self.print_status(f"📅 Next Shift press in {self.interval//60} minutes...")

    def stop(self) -> None:
        """Stop all running processes."""
        self._is_running = False
        self.lazy_b.stop()

        if self._animation_thread and self._animation_thread.is_alive():
            self._animation_thread.join(timeout=1)

    def list_animations(self) -> None:
        """List available animations."""
        from .animations.repository import FileSystemAnimationRepository

        repo = FileSystemAnimationRepository(self.animation_engine._config)
        animation_dirs = repo.discover_animations()

        if not animation_dirs:
            self.print_status("No animations found!")
            return

        self.print_status("Available animations:")
        for i, directory in enumerate(animation_dirs, 1):
            animation_name = directory.split("/")[-1]
            self.print_status(f"  {i}. {animation_name}")
