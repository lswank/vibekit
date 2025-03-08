#!/usr/bin/env python3
"""
Setup script for installing VibeKit using UV.

This script helps set up the VibeKit project environment with UV.
"""

import os
import subprocess
import sys

def main():
    """Set up the VibeKit development environment using UV."""
    
    print("Setting up VibeKit with UV...")
    
    # Check if UV is installed
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("UV not found. Installing UV...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
    
    # Create a virtual environment if it doesn't exist
    if not os.path.exists(".venv"):
        print("Creating a virtual environment...")
        subprocess.run(["uv", "venv"], check=True)
    
    # Install the package in development mode
    print("Installing VibeKit and dependencies...")
    subprocess.run(["uv", "pip", "install", "-e", "."], check=True)
    
    # Install development dependencies
    print("Installing development dependencies...")
    subprocess.run(["uv", "pip", "install", "-e", ".[dev]"], check=True)
    
    print("\nSetup complete! You can now use VibeKit.")
    print("\nTo activate the virtual environment, run:")
    print("  source .venv/bin/activate  # On Unix/macOS")
    print("  .venv\\Scripts\\activate    # On Windows")
    
    print("\nTo run an example:")
    print("  cd vibekit/examples")
    print("  python simple_example.py")

if __name__ == "__main__":
    main() 