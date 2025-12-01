@echo off
REM =============================================================================
REM Splunk Advanced Course - Update Script
REM =============================================================================
REM This script pulls the latest changes from the GitHub repository
REM Run this script from any location - it will automatically find the repo
REM =============================================================================

echo.
echo ================================================================================
echo            SPLUNK ADVANCED COURSE - UPDATE FROM GITHUB
echo ================================================================================
echo.

REM Save current directory
set ORIGINAL_DIR=%CD%

REM Change to the script's directory
cd /d "%~dp0"

REM Go up one level to the repository root
cd ..

REM Display current location
echo Repository Location: %CD%
echo.

REM Check if this is a git repository
if not exist ".git" (
    echo ERROR: This does not appear to be a git repository!
    echo Please run this script from within the splunk_adv_v3 repository.
    echo.
    pause
    cd /d "%ORIGINAL_DIR%"
    exit /b 1
)

REM Check git status first
echo Checking repository status...
echo.
git status
echo.

REM Ask for confirmation
echo ================================================================================
set /p CONFIRM="Do you want to pull the latest changes from GitHub? (Y/N): "

if /i not "%CONFIRM%"=="Y" (
    echo.
    echo Update cancelled.
    echo.
    pause
    cd /d "%ORIGINAL_DIR%"
    exit /b 0
)

echo.
echo ================================================================================
echo Pulling latest changes from GitHub...
echo ================================================================================
echo.

REM Pull changes
git pull

REM Check if pull was successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ================================================================================
    echo SUCCESS: Repository updated successfully!
    echo ================================================================================
    echo.
    echo Latest changes have been downloaded.
    echo You can now use the updated course materials.
    echo.
) else (
    echo.
    echo ================================================================================
    echo ERROR: Failed to update repository!
    echo ================================================================================
    echo.
    echo Please check:
    echo   1. Your internet connection
    echo   2. Your GitHub credentials
    echo   3. Any local changes that may conflict
    echo.
    echo You may need to:
    echo   - Commit or stash your local changes
    echo   - Resolve merge conflicts
    echo   - Check your git configuration
    echo.
)

REM Return to original directory
cd /d "%ORIGINAL_DIR%"

pause
