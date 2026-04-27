@echo off
:: Quick start script for OmniVoice AMD GPU Edition

:: Set environment variables
set "HF_ENDPOINT=https://hf-mirror.com"
set "HF_HOME=%~dp0models"
set "MIOPEN_LOG_LEVEL=6"

echo ============================================================
echo     OmniVoice AMD GPU Edition - Quick Start
echo ============================================================
echo.

:: Check if model is downloaded
if not exist "%HF_HOME%\models--k2-fsa--OmniVoice" (
    echo First run: downloading model...
    echo This may take a few minutes.
    echo.
)

:: Run the Python script
py -3.12 verify_install.py

echo.
pause
