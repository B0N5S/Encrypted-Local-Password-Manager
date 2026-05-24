@echo off
setlocal EnableDelayedExpansion
title PassSafe - Setup Wizard
cls
echo.
echo  =============================================================
echo   ___              ___        __
echo  ^|   ^|__  ^| ^|__^|  ^|   ^| __  ^|__^|  ___
echo  ^|___^|  ^| ^| ^|  ^|  ^|___^|^|__^| ^|    ^|_^|
echo.
echo                  PassSafe Setup Wizard
echo  =============================================================
echo.
echo  This script will:
echo    [1] Check Python is installed
echo    [2] Upgrade pip
echo    [3] Install required libraries
echo    [4] Launch PassSafe
echo.
echo  =============================================================
echo.
pause
echo.
echo  [STEP 1/4]  Checking for Python...
echo  -----------------------------------------------------------
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
    echo.
    echo    [OK]  Found: !PY_VER!
    goto :check_version
)
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    for /f "tokens=*" %%v in ('python3 --version 2^>^&1') do set PY_VER=%%v
    echo.
    echo    [OK]  Found: !PY_VER!
    goto :check_version
)
py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    for /f "tokens=*" %%v in ('py --version 2^>^&1') do set PY_VER=%%v
    echo.
    echo    [OK]  Found: !PY_VER!
    goto :check_version
)
echo.
echo    [FAIL]  Python was not found on this system.
echo.
echo    Please install Python 3.10 or higher from:
echo    https://www.python.org/downloads/
echo.
echo    IMPORTANT: During installation, tick the box that says
echo    "Add Python to PATH" before clicking Install Now.
echo.
echo    After installing, close this window and run setup.bat again.
echo.
pause
exit /b 1
:check_version
for /f "tokens=2 delims= " %%v in ('!PYTHON_CMD! --version 2^>^&1') do set VER_FULL=%%v
for /f "tokens=1 delims=." %%m in ("!VER_FULL!") do set VER_MAJOR=%%m
for /f "tokens=2 delims=." %%m in ("!VER_FULL!") do set VER_MINOR=%%m
if !VER_MAJOR! LSS 3 (
    echo.
    echo    [FAIL]  Python !VER_FULL! is too old. PassSafe needs Python 3.10+.
    echo    Please download a newer version from python.org
    echo.
    pause
    exit /b 1
)
if !VER_MAJOR! == 3 (
    if !VER_MINOR! LSS 10 (
        echo.
        echo    [WARN]  Python !VER_FULL! detected. Python 3.10+ is recommended.
        echo    PassSafe may still work, but upgrading is advised.
        echo.
    )
)
echo    Version check passed.
echo.
echo  [STEP 2/4]  Upgrading pip...
echo  -----------------------------------------------------------
echo.
!PYTHON_CMD! -m pip install --upgrade pip --quiet 2>&1
if %errorlevel% == 0 (
    echo    [OK]  pip is up to date.
) else (
    echo    [WARN]  Could not upgrade pip. Continuing anyway...
)
echo.
echo  [STEP 3/4]  Installing required libraries...
echo  -----------------------------------------------------------
echo.
echo    Installing PyQt6 ^(this may take a minute^)...
echo.
!PYTHON_CMD! -m pip install PyQt6 --quiet
if %errorlevel% NEQ 0 (
    echo.
    echo    [FAIL]  Could not install PyQt6.
    echo.
    echo    Try running this command manually:
    echo    !PYTHON_CMD! -m pip install PyQt6
    echo.
    pause
    exit /b 1
)
echo    [OK]  PyQt6 installed.
echo.
echo    Installing cryptography...
echo.
!PYTHON_CMD! -m pip install cryptography --quiet
if %errorlevel% NEQ 0 (
    echo.
    echo    [FAIL]  Could not install cryptography.
    echo.
    echo    Try running this command manually:
    echo    !PYTHON_CMD! -m pip install cryptography
    echo.
    pause
    exit /b 1
)
echo    [OK]  cryptography installed.
echo.
echo    Verifying installations...
!PYTHON_CMD! -c "import PyQt6; import cryptography; print('    [OK]  All libraries verified.')"
if %errorlevel% NEQ 0 (
    echo.
    echo    [FAIL]  Library verification failed.
    echo    Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)
echo.
echo  [STEP 4/4]  Launching PassSafe...
echo  -----------------------------------------------------------
echo.
if not exist "%~dp0main.py" (
    echo    [FAIL]  main.py was not found in this folder:
    echo    %~dp0
    echo.
    echo    Make sure setup.bat is inside the PassSafe folder
    echo    alongside main.py and all other .py files.
    echo.
    pause
    exit /b 1
)
echo    [OK]  All files found.
echo.
echo  =============================================================
echo.
echo    Setup complete! Starting PassSafe now...
echo.
echo    You can close this window once the app opens, or keep
echo    it open to see any error messages.
echo.
echo  =============================================================
echo.
cd /d "%~dp0"
!PYTHON_CMD! main.py
if %errorlevel% NEQ 0 (
    echo.
    echo  =============================================================
    echo    PassSafe closed with an error (code: %errorlevel%)
    echo    Read the message above to see what went wrong.
    echo  =============================================================
    echo.
    pause
)
endlocal
