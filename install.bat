@echo off
echo.
echo ============================================================
echo     OmniVoice AMD GPU Edition - Installer
echo ============================================================
echo.

:: Set installation directory
set "INSTALL_DIR=%~dp0"
set "MODEL_DIR=%INSTALL_DIR%models"

:: Create models directory
if not exist "%MODEL_DIR%" mkdir "%MODEL_DIR%"

:: Step 1: Check Python 3.12
echo [Step 1/5] Checking Python environment...
echo.

py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python 3.12 detected
    set PYTHON_CMD=py -3.12
    goto :step2
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    python --version | findstr "3.12" >nul
    if %errorlevel% equ 0 (
        echo [OK] Python 3.12 detected
        set PYTHON_CMD=python
        goto :step2
    )
)

echo.
echo ============================================================
echo [Notice] Python 3.12 is required
echo ============================================================
echo.
echo ROCm 7.2.1 only supports Python 3.12
echo.
echo Options:
echo   1. Auto install Python 3.12 (recommended)
echo   2. Open download page (manual install)
echo   3. Exit
echo.

set /p choice="Enter option (1/2/3): "

if "%choice%"=="1" goto :install_python
if "%choice%"=="2" goto :manual_install
if "%choice%"=="3" exit /b 0
goto :end

:install_python
echo.
echo Downloading Python 3.12.9...
echo.

set PYTHON_URL=https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe
set PYTHON_INSTALLER=%TEMP%\python-3.12.9-amd64.exe

curl -L -o "%PYTHON_INSTALLER%" "%PYTHON_URL%"
if %errorlevel% neq 0 (
    echo [Error] Download failed!
    echo Please download manually: %PYTHON_URL%
    pause
    exit /b 1
)

echo.
echo Installing Python 3.12.9...
echo Please click "Install Now" in the popup window.
echo.

"%PYTHON_INSTALLER%" InstallAllUsers=1 PrependPath=1 Include_pip=1

echo.
echo Press any key after installation completes...
pause >nul

py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python 3.12 installed successfully!
    set PYTHON_CMD=py -3.12
    del "%PYTHON_INSTALLER%" 2>nul
    goto :step2
) else (
    echo [Error] Python installation may not be complete.
    echo Please run this script again.
    pause
    exit /b 1
)

:manual_install
echo.
echo Opening Python download page...
start https://www.python.org/downloads/release/python-3129/
echo.
echo After installation, please run this script again.
pause
exit /b 0

:step2
echo.
echo ============================================================
echo [Step 2/5] Upgrading pip...
echo ============================================================
echo.

%PYTHON_CMD% -m pip install --upgrade pip -q
echo [OK] pip upgraded
echo.

echo ============================================================
echo [Step 3/5] Installing AMD ROCm PyTorch...
echo ============================================================
echo.
echo Downloading ROCm PyTorch (about 2GB, please wait)...
echo.

setlocal enabledelayedexpansion

:: ROCm SDK packages
%PYTHON_CMD% -m pip install --upgrade ^
    "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_core-7.2.1-py3-none-win_amd64.whl" ^
    "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl" ^
    "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm-7.2.1.tar.gz"

if !errorlevel! neq 0 (
    echo [Error] ROCm SDK installation failed!
    pause
    exit /b 1
)

:: PyTorch packages with + in filename (need quotes)
%PYTHON_CMD% -m pip install --upgrade ^
    "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl" ^
    "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchaudio-2.9.1+rocm7.2.1-cp312-cp312-win_amd64.whl" ^
    "https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchvision-0.24.1+rocm7.2.1-cp312-cp312-win_amd64.whl"

if !errorlevel! neq 0 (
    echo [Error] PyTorch installation failed!
    pause
    exit /b 1
)

endlocal

echo.
echo [OK] ROCm PyTorch installed
echo.

echo ============================================================
echo [Step 4/5] Installing OmniVoice AMD Edition...
echo ============================================================
echo.

if exist omnivoice_amd-0.1.4-py3-none-any.whl (
    %PYTHON_CMD% -m pip install omnivoice_amd-0.1.4-py3-none-any.whl
) else (
    echo [Warning] Wheel file not found, trying PyPI...
    %PYTHON_CMD% -m pip install omnivoice-amd
)

if %errorlevel% neq 0 (
    echo.
    echo [Error] OmniVoice installation failed!
    pause
    exit /b 1
)

echo.
echo [OK] OmniVoice installed
echo.

echo ============================================================
echo [Step 5/5] Installing FFmpeg...
echo ============================================================
echo.

:: Check if ffmpeg already exists
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] FFmpeg already installed
    goto :env_setup
)

:: Try winget first
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing FFmpeg via winget...
    winget install ffmpeg --accept-source-agreements --accept-package-agreements -q
    if %errorlevel% equ 0 (
        echo [OK] FFmpeg installed via winget
        goto :env_setup
    )
)

:: Fallback: download ffmpeg
echo Downloading FFmpeg...
set FFMPEG_URL=https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
set FFMPEG_ZIP=%TEMP%\ffmpeg.zip
set FFMPEG_DIR=%LOCALAPPDATA%\ffmpeg

curl -L -o "%FFMPEG_ZIP%" "%FFMPEG_URL%"
if %errorlevel% neq 0 (
    echo [Warning] FFmpeg download failed
    echo You can install it manually later
    goto :env_setup
)

echo Extracting FFmpeg...
powershell -Command "Expand-Archive -Path '%FFMPEG_ZIP%' -DestinationPath '%FFMPEG_DIR%' -Force"

:: Add to PATH for current session
set "PATH=%PATH%;%FFMPEG_DIR%\ffmpeg-master-latest-win64-gpl\bin"

del "%FFMPEG_ZIP%" 2>nul
echo [OK] FFmpeg installed

:env_setup
echo.
echo ============================================================
echo              Setting Environment Variables
echo ============================================================
echo.

:: Set environment variables permanently
echo Setting HF_ENDPOINT (HuggingFace mirror)...
setx HF_ENDPOINT "https://hf-mirror.com" >nul 2>&1

echo Setting HF_HOME (model cache directory)...
setx HF_HOME "%MODEL_DIR%" >nul 2>&1

echo Setting MIOPEN_LOG_LEVEL (suppress warnings)...
setx MIOPEN_LOG_LEVEL "6" >nul 2>&1

:: Set for current session
set "HF_ENDPOINT=https://hf-mirror.com"
set "HF_HOME=%MODEL_DIR%"
set "MIOPEN_LOG_LEVEL=6"

echo [OK] Environment variables configured
echo.

echo ============================================================
echo                    Verifying Installation
echo ============================================================
echo.

echo Checking GPU status...
%PYTHON_CMD% -c "import torch; print(''); print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'Not detected'); print('')"

echo.
echo ============================================================
echo                 Installation Complete!
echo ============================================================
echo.
echo Installation directory: %INSTALL_DIR%
echo Model cache directory: %MODEL_DIR%
echo.
echo You can now run:
echo   - verify_install.py  (verify installation)
echo   - run.bat            (quick start)
echo.
echo Or start Web UI:
echo   %PYTHON_CMD% -m omnivoice.cli.demo --ip 0.0.0.0 --port 8001
echo.
echo ============================================================
echo.

:end
pause
