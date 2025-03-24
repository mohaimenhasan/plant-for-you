#!/usr/bin/env python
"""
MotivaPlant Game Launcher
------------------------
This script checks if the required dependencies are installed and then launches the game.
"""

import sys
import subprocess
import os

def check_requirements():
    """Check if required packages are installed."""
    missing_deps = []
    try:
        import pygame
    except ImportError:
        missing_deps.append("pygame")
    
    try:
        import pyglet
    except ImportError:
        missing_deps.append("pyglet")
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("pillow")
    
    try:
        import numpy
    except ImportError:
        missing_deps.append("numpy")
    
    if missing_deps:
        print("Missing required dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        return False
    return True

def install_requirements():
    """Install the required packages using pip."""
    try:
        print("Attempting to install required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except Exception as e:
        print(f"\nError during package installation: {e}")
        print("\nInstallation Instructions:")
        print("1. Make sure you have pip installed for your Python version")
        print("   - For Windows: python -m ensurepip")
        print("   - For Linux: sudo apt-get install python3-pip")
        print("   - For macOS: brew install python (includes pip)")
        print("\n2. Install the required packages:")
        print("   pip install -r requirements.txt")
        print("   or")
        print("   pip3 install -r requirements.txt")
        print("\n3. Run the game again after installing dependencies")
        return False

def check_assets():
    """Check if required asset directories exist."""
    asset_dirs = [
        "assets/fonts",
        "assets/sounds",
        "assets/images"
    ]
    
    for directory in asset_dirs:
        if not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)
    
    # Check for specific assets
    missing_assets = False
    
    # Check for font
    if not os.path.exists("assets/fonts/minecraft.ttf"):
        print("\nWARNING: Minecraft font not found.")
        print("Creating a placeholder file, but the game will use system fonts.")
        print("Please check ASSETS.md for instructions on downloading the proper font.")
        # Create an empty placeholder file
        try:
            with open("assets/fonts/minecraft.ttf", 'wb') as f:
                f.write(b'PLACEHOLDER')
        except Exception as e:
            print(f"Error creating placeholder font: {e}")
        missing_assets = True
    
    # Check for sound files
    sound_files = ["water.wav", "grow.wav", "click.wav"]
    missing_sounds = [f for f in sound_files if not os.path.exists(f"assets/sounds/{f}")]
    
    if missing_sounds:
        print("\nWARNING: Some sound files are missing:")
        for sound in missing_sounds:
            print(f"  - assets/sounds/{sound}")
            # Create an empty placeholder file
            # This will create invalid WAV files which will be caught by the error handlers
            try:
                with open(f"assets/sounds/{sound}", 'wb') as f:
                    # Write an empty WAV header (this is not a valid WAV file but creates the file)
                    f.write(b'RIFF\x00\x00\x00\x00WAVEfmt \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            except Exception as e:
                print(f"Error creating placeholder sound: {e}")
        print("Creating placeholder files, but the game will not have sound effects.")
        print("Please check ASSETS.md for instructions on downloading the proper sound files.")
        missing_assets = True
    
    if missing_assets:
        print("\nThe game will run with placeholders, but for the full experience,")
        print("download the required assets as described in ASSETS.md")
        print("The game will continue in 3 seconds...")
        try:
            import time
            time.sleep(3)
        except KeyboardInterrupt:
            print("Setup interrupted by user.")
            sys.exit(0)

def launch_game():
    """Launch the MotivaPlant game."""
    import main
    main.main()

if __name__ == "__main__":
    print("\nMotivaPlant - A motivational plant game")
    print("----------------------------------------")
    
    # Make sure requirements are installed
    if not check_requirements():
        print("\nMissing dependencies. Attempting to install...\n")
        if not install_requirements():
            print("\nCould not automatically install dependencies.")
            sys.exit(1)
        
        # Check again after installation attempt
        if not check_requirements():
            print("\nDependencies are still missing after installation attempt.")
            print("Please install them manually and run the game again.")
            sys.exit(1)
    
    # Check assets
    check_assets()
    
    print("\nStarting MotivaPlant...\n")
    try:
        launch_game()
    except Exception as e:
        print(f"Error launching game: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)