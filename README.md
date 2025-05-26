# lazy-b

Keep Slack, Microsoft Teams, or other similar applications from showing you as "away" or "inactive" by simulating key presses at regular intervals.

![2025-05-2600 01 29-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/483c305b-411d-4bab-9f01-dd20c4329b49)


## Installation

Install directly from PyPI using pip or uv:

```bash
# Using pip
pip install lazy-b

# Using uv
uv pip install lazy-b
```

## Usage

### Command Line

Run `lazy-b` from the command line:

```bash
# Basic usage (will press Shift key every 1 second)
lazy-b

# Customize the interval (e.g., every 30 seconds)
lazy-b --interval 30
```

#### Platform-specific behavior

- **macOS**: By default, runs in background mode with no dock icon. You can close the terminal window after starting it, and it will continue to run.
- **Windows/Linux**: The application runs in the terminal window. You need to keep the window open for the program to continue running.

To stop lazy-b, you can:
- Press Ctrl+C in the terminal window
- On macOS, if running in background, find and kill the process:

```bash
# Find the process
ps aux | grep lazy-b

# Kill it using the PID
kill <PID>
```

### Python API

You can also use the Python API directly in your own scripts (works on all platforms):

```python
from lazy_b import LazyB
import time

# Create an instance with a custom interval (in seconds)
lazy = LazyB(interval=5)  # Press Shift every 5 seconds

# Define a callback function to handle status messages (optional)
def status_callback(message):
    print(f"Status: {message}")

# Start the simulation
lazy.start(callback=status_callback)

try:
    # Keep your script running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop on Ctrl+C
    lazy.stop()
```

## Features

- Prevents "away" or "inactive" status in messaging applications
- Customizable interval between key presses (default: 1 second)
- Simple command-line interface
- Cross-platform: Works on macOS, Windows, and Linux
- Background mode on macOS (no dock icon)
- Python API for integration into your own scripts
- Minimal resource usage

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Lanznx/lazy-b.git
cd lazy-b

# Setup development environment
make dev-setup

# Install in development mode
make install
```

### Releasing New Versions

To release a new version:

```bash
# Update version, create commit and tag
make release  # This will prompt for the new version

# Push changes and tag to GitHub
git push origin main
git push origin v<version>  # e.g., git push origin v0.2.0
```

Pushing a tag will automatically trigger the release workflow, which will:
1. Build the package
2. Create a GitHub release
3. Publish to PyPI

## Requirements

- Python 3.8 or higher
- PyAutoGUI
- PyObjC-Core (for macOS dock icon hiding, optional)

## License

MIT

## Disclaimer

This tool is meant for legitimate use cases like preventing timeouts during presentations or when you're actively reading but not typing. Please use responsibly and in accordance with your organization's policies.
