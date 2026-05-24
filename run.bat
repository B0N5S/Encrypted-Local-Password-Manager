@echo off
title PassSafe
cd /d "%~dp0"
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% == 0 ( set PYTHON_CMD=python & goto :launch )
python3 --version >nul 2>&1
if %errorlevel% == 0 ( set PYTHON_CMD=python3 & goto :launch )
py --version >nul 2>&1
if %errorlevel% == 0 ( set PYTHON_CMD=py & goto :launch )
echo.
echo  [ERROR]  Python not found. Please run setup.bat first.
echo.
pause
exit /b 1
:launch
%PYTHON_CMD% main.py
if %errorlevel% NEQ 0 (
    echo.
    echo  PassSafe exited with an error. See above for details.
    echo  If this keeps happening, run setup.bat again.
    echo.
    pause
)
