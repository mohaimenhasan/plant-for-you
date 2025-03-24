"""
Build script to package MotivaPlant as a standalone executable.
This creates a single .exe file that can run without Python installed.
"""

import os
import sys
import shutil
import subprocess

def build_exe():
    """Build the executable using PyInstaller"""
    print("Building MotivaPlant executable...")
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create spec file content with custom settings
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=['pygame', 'pygame.mixer', 'pygame.font', 'pygame.image', 'pygame.display', 'pygame.time', 'pygame.mixer_music', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MotivaPlant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icon.ico' if os.path.exists('assets/images/icon.ico') else None,
)
"""
    
    # Write spec file
    with open("MotivaPlant.spec", "w") as f:
        f.write(spec_content)
    
    # Create icon directory if it doesn't exist
    os.makedirs("assets/images", exist_ok=True)
    
    # Run PyInstaller using Python module system
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "MotivaPlant.spec"]
    subprocess.check_call(cmd)
    
    print("\nBuild complete!")
    print(f"Executable is located at: {os.path.abspath(os.path.join('dist', 'MotivaPlant.exe'))}")
    print("\nIf you want to distribute the app, copy the entire 'dist' folder.")
    print("Make sure the assets folder contains all required files (fonts, sounds)!")

if __name__ == "__main__":
    build_exe()