import argparse
import platform
import signal
import sys
import time
from typing import Any, List, Optional


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="LazyB: Keep Slack/Teams active with optional ASCII animations."
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=180,
        help="Interval between key presses in seconds (default: 180 = 3 minutes)",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Run in quiet mode (no output)"
    )

    parser.add_argument(
        "--animation",
        type=str,
        help="Specify animation to use (skips interactive selection)",
    )

    if platform.system() == "Darwin":
        parser.add_argument(
            "-f",
            "--foreground",
            action="store_true",
            help=(
                "Run in foreground mode "
                "(by default, runs in background with no dock icon)"
            ),
        )

    return parser.parse_args(args)


def hide_dock_icon() -> None:
    """Hide the dock icon on macOS."""
    if platform.system() != "Darwin":
        return

    try:
        from AppKit import NSApplication  # type: ignore

        app = NSApplication.sharedApplication()
        # NSApplicationActivationPolicyAccessory = 1
        # This prevents the app from showing in the dock
        app.setActivationPolicy_(1)
    except ImportError:
        pass


def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the CLI."""
    parsed_args = parse_args(args)

    from .integrated_runner import IntegratedLazyB

    # Setup integrated runner
    integrated_runner = IntegratedLazyB(
        interval=parsed_args.interval, quiet=parsed_args.quiet
    )

    # Handle dock icon on macOS
    os_name = platform.system()
    is_macos = os_name == "Darwin"
    if is_macos and hasattr(parsed_args, "foreground") and not parsed_args.foreground:
        hide_dock_icon()

    def signal_handler(sig: Any, frame: Any) -> None:
        """Handle Ctrl+C to gracefully shut down."""
        if not parsed_args.quiet:
            print("\nShutting down LazyB...")
        integrated_runner.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Handle different modes
        if parsed_args.animation:
            # Use specified animation
            integrated_runner.start_with_animation(parsed_args.animation)
        else:
            # Default: start with interactive animation selection menu
            integrated_runner.start_with_animation_menu()

        # Show platform-specific information
        if (
            is_macos
            and hasattr(parsed_args, "foreground")
            and not parsed_args.foreground
        ):
            print("Running in background mode. You can close this terminal window.")
        else:
            print(
                f"Running on {os_name}. "
                "Keep this window open for the program to continue running."
            )

        # Keep running until interrupted
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        if not parsed_args.quiet:
            print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
