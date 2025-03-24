"""
Build script to package the simplified tkinter version as a standalone executable.
This should work even without pygame installed.
"""

import os
import sys
import subprocess

def build_exe():
    """Build the executable using PyInstaller"""
    print("Building MotivaPlant Simple version executable...")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Run PyInstaller using Python module system
    cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller", 
        "--onefile", 
        "--windowed", 
        "--name", 
        "MotivaPlant", 
        "simple_run.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild complete!")
        print(f"Executable is located at: {os.path.abspath(os.path.join('dist', 'MotivaPlant.exe'))}")
        print("\nYou can share this single executable file.")
    except Exception as e:
        print(f"Error building executable: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()