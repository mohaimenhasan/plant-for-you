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
        "--version-file",
        f"version_info.txt",
        "simple_run.py"
    ]
    
    # Create version info file with publisher name
    with open("version_info.txt", "w") as f:
        f.write("""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Mohaimen Khan'),
        StringStruct(u'FileDescription', u'MotivaPlant - A motivational plant game'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'MotivaPlant'),
        StringStruct(u'LegalCopyright', u'© 2025 Mohaimen Khan. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'MotivaPlant.exe'),
        StringStruct(u'ProductName', u'MotivaPlant'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
""")
    
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