#!/usr/bin/env python3
"""
Update version script for lazy-b package.
Usage: python scripts/update_version.py <new_version>
Example: python scripts/update_version.py 0.2.0
"""
import sys
import re
import subprocess
from pathlib import Path


def update_version(new_version: str) -> None:
    """Update version in all necessary files."""
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        print(f"Error: Version must follow semver format (e.g., 1.2.3), got {new_version}")
        sys.exit(1)
    
    # Get the project root directory
    root_dir = Path(__file__).parent.parent
    
    # Update pyproject.toml
    pyproject_path = root_dir / "pyproject.toml"
    with open(pyproject_path, 'r') as f:
        content = f.read()
    
    content = re.sub(
        r'version = "[0-9]+\.[0-9]+\.[0-9]+"',
        f'version = "{new_version}"',
        content
    )
    
    with open(pyproject_path, 'w') as f:
        f.write(content)
    
    # Update __init__.py
    init_path = root_dir / "src" / "lazy_b" / "__init__.py"
    with open(init_path, 'r') as f:
        content = f.read()
    
    content = re.sub(
        r'__version__ = "[0-9]+\.[0-9]+\.[0-9]+"',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(init_path, 'w') as f:
        f.write(content)
    
    print(f"Version updated to {new_version} in all files")
    
    # Create git commit and tag
    subprocess.run(["git", "add", str(pyproject_path), str(init_path)], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version to {new_version}"], check=True)
    subprocess.run(["git", "tag", f"v{new_version}"], check=True)
    
    print(f"Created commit and tag for v{new_version}")
    print("\nNext steps:")
    print(f"  1. Push the changes: git push origin main")
    print(f"  2. Push the tag: git push origin v{new_version}")
    print("  3. GitHub Actions will automatically build and publish the package")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <new_version>")
        sys.exit(1)
    
    update_version(sys.argv[1]) 