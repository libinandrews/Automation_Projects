@echo off
REM Change to the directory where this script is located
cd /d "%~dp0"
set ROOT_DIR=%cd%
echo Root working directory set to: %ROOT_DIR%

REM Install Jupyter Lab if not already installed
pip install jupyterlab

REM Start Jupyter Lab with the root directory
jupyter lab --notebook-dir="%ROOT_DIR%"
pause