@echo off
ECHO ===================================
ECHO MotivaPlant - Build Windows Executable
ECHO ===================================

ECHO Installing required packages...
pip install -r requirements.txt
pip install pyinstaller pillow

ECHO Creating application icon...
python create_icon.py

ECHO Building executable...
python build_exe.py

ECHO Done!
ECHO The executable is in the 'dist' folder.
ECHO Copy the entire 'dist' folder to share the application.
ECHO ===================================

pause