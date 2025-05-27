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

## 🎬 Adding Custom Animations

LazyB supports ASCII animations that play while keeping your status active. You can add your own custom animations to the system.

### Animation File Structure

Animations are stored in the `animations` directory, with each animation in its own subdirectory. Each frame should be saved as a separate `.txt` file with a numbered sequence.

**Supported naming formats:**
- `frame_1.txt`, `frame_2.txt`, `frame_3.txt`, ... (frame_NUMBER.txt)
- `001_description.txt`, `002_description.txt`, `003_description.txt`, ... (NUMBER_description.txt)

**Example structure:**
```
animations/
├── my_cool_animation/
│   ├── frame_1.txt
│   ├── frame_2.txt
│   └── frame_3.txt
└── another_animation/
    ├── 001_start.txt
    ├── 002_middle.txt
    └── 003_end.txt
```

### Creating Animations from Videos

If you want to convert a video into ASCII animation, follow these steps:

#### Step 1: Convert Video to ASCII Frames

1. **Clone the ASCII Animator tool:**
   ```bash
   git clone https://github.com/bradysheridan/ascii-animator.git
   cd ascii-animator
   ```

2. **Upload your video file** to the ASCII Animator and process it through their system.

3. **Export the output** - you should get a `frames.js` file containing an array of ASCII frames.

#### Step 2: Convert Frames to TXT Files

1. **Place the `frames.js` file** in your LazyB `animations` directory.

2. **Run the conversion script** (requires Node.js):
   ```bash
   # Install Node.js if not already installed
   # Visit https://nodejs.org/ or use package manager
   
   cd animations
   node convertFramesToTxt.js
   ```

3. **Follow the prompts** to name your animation directory (avoid spaces and special characters).

4. **The script will create** a new directory with all frames converted to individual `.txt` files.

#### Step 3: Test Your Animation

1. **Run LazyB** and your new animation should appear in the selection menu:
   ```bash
   lazy-b
   ```

2. **Use arrow keys** to navigate and select your animation.

### Animation Guidelines

- **File naming**: Frames must be numbered sequentially starting from 1
- **File format**: Plain text (`.txt`) files with UTF-8 encoding
- **Frame size**: Recommended maximum 80 characters wide for terminal compatibility
- **Frame rate**: Default is 0.2 seconds per frame (5 FPS), configurable
- **Directory naming**: Use underscores instead of spaces, avoid special characters

### Troubleshooting

- **Animation not showing up?** Check that frame files follow the naming convention
- **Frames out of order?** Ensure sequential numbering without gaps
- **Display issues?** Verify files are UTF-8 encoded and frames aren't too wide

## Features

- Prevents "away" or "inactive" status in messaging applications
- **🎬 ASCII Animation Support**: Display entertaining animations while keeping your status active
- Interactive animation selection menu with live preview
- Customizable interval between key presses (default: 3 minutes)
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

### Runtime Requirements
- Python 3.8 or higher
- PyAutoGUI
- PyObjC-Core (for macOS dock icon hiding, optional)

### Animation Development Requirements (Optional)
- Node.js (for running the frame conversion script)
- Access to [ASCII Animator](https://github.com/bradysheridan/ascii-animator) for video-to-ASCII conversion

## License

MIT

## Disclaimer

This tool is meant for legitimate use cases like preventing timeouts during presentations or when you're actively reading but not typing. Please use responsibly and in accordance with your organization's policies.
