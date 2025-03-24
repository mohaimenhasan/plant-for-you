@echo off
echo ===================================
echo MotivaPlant - Build with auto-py-to-exe
echo ===================================

echo Installing auto-py-to-exe...
pip install auto-py-to-exe

echo Creating version info file with publisher information...
echo VSVersionInfo( > version_info.txt
echo   ffi=FixedFileInfo( >> version_info.txt
echo     filevers=(1, 0, 0, 0), >> version_info.txt
echo     prodvers=(1, 0, 0, 0), >> version_info.txt
echo     mask=0x3f, >> version_info.txt
echo     flags=0x0, >> version_info.txt
echo     OS=0x40004, >> version_info.txt
echo     fileType=0x1, >> version_info.txt
echo     subtype=0x0, >> version_info.txt
echo     date=(0, 0) >> version_info.txt
echo     ), >> version_info.txt
echo   kids=[ >> version_info.txt
echo     StringFileInfo( >> version_info.txt
echo       [ >> version_info.txt
echo       StringTable( >> version_info.txt
echo         u'040904B0', >> version_info.txt
echo         [StringStruct(u'CompanyName', u'Mohaimen Khan'), >> version_info.txt
echo         StringStruct(u'FileDescription', u'MotivaPlant - A motivational plant game'), >> version_info.txt
echo         StringStruct(u'FileVersion', u'1.0.0'), >> version_info.txt
echo         StringStruct(u'InternalName', u'MotivaPlant'), >> version_info.txt
echo         StringStruct(u'LegalCopyright', u'© 2025 Mohaimen Khan. All rights reserved.'), >> version_info.txt
echo         StringStruct(u'OriginalFilename', u'MotivaPlant.exe'), >> version_info.txt
echo         StringStruct(u'ProductName', u'MotivaPlant'), >> version_info.txt
echo         StringStruct(u'ProductVersion', u'1.0.0')]) >> version_info.txt
echo       ]), >> version_info.txt
echo     VarFileInfo([VarStruct(u'Translation', [1033, 1200])]) >> version_info.txt
echo   ] >> version_info.txt
echo ) >> version_info.txt

echo.
echo Starting auto-py-to-exe...
echo.
echo INSTRUCTIONS:
echo 1. Select "One File" for output format
echo 2. Select "Window Based" for console
echo 3. Set Script Location to: main.py
echo 4. Add version file by clicking "Additional Files" and add:
echo    - Add File: version_info.txt [version_info.txt]
echo 5. Add publisher info by entering "--version-file=version_info.txt" in the Additional Arguments field
echo 6. Add Additional Files: Click "Add Folder" and select "assets" folder
echo 7. Click "Convert" to build the executable
echo.
echo Your executable will be created in the "output" directory.
echo.
echo.

python -m auto_py_to_exe

echo.
echo Done!
echo Your executable is in the output folder.
echo.