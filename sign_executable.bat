@echo off
echo ===================================
echo MotivaPlant - Code Signing Script
echo ===================================

echo Creating a self-signed certificate for code signing...

REM Check if OpenSSL is installed
where openssl >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo OpenSSL is not installed or not in PATH.
    echo Please install OpenSSL or add it to your PATH.
    echo You can download OpenSSL from: https://slproweb.com/products/Win32OpenSSL.html
    pause
    exit /b 1
)

REM Create a self-signed certificate
echo Creating a self-signed certificate...
openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout MohaimenKhan.key -out MohaimenKhan.crt -subj "/CN=Mohaimen Khan/O=Mohaimen Khan/C=US"

REM Convert to PFX format
echo Converting to PFX format...
openssl pkcs12 -export -out MohaimenKhan.pfx -inkey MohaimenKhan.key -in MohaimenKhan.crt -password pass:changeit

echo Certificate created successfully!

REM Check if signtool is available (part of Windows SDK)
where signtool >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Signtool is not installed or not in PATH.
    echo Please install Windows SDK which includes signtool.
    echo You can download it from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
    echo.
    echo After installing, you will need to run:
    echo signtool sign /f MohaimenKhan.pfx /p changeit /d "MotivaPlant" /du "https://github.com/mohaimenkhan/motivatorapp" /t http://timestamp.sectigo.com dist\MotivaPlant.exe
    pause
    exit /b 1
)

REM Sign the executable
echo Signing the executable...
signtool sign /f MohaimenKhan.pfx /p changeit /d "MotivaPlant" /du "https://github.com/mohaimenkhan/motivatorapp" /t http://timestamp.sectigo.com dist\MotivaPlant.exe

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================
    echo Executable signed successfully!
    echo Publisher name: Mohaimen Khan
    echo ===================================
) else (
    echo.
    echo Failed to sign the executable.
    echo Please check if the executable exists and the certificate is valid.
)

pause