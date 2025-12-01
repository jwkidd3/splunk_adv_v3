@echo off
REM =============================================================================
REM Splunk Advanced Course - Update Script
REM =============================================================================
REM This script pulls the latest changes from the GitHub repository
REM IMPORTANT: Update the path below to match your local installation
REM =============================================================================

echo.
echo ================================================================================
echo            SPLUNK ADVANCED COURSE - UPDATE FROM GITHUB
echo ================================================================================
echo.

REM Change to the repository directory
cd /d "C:\Users\Administrator\Desktop\splunk_adv_v3"

REM Display current location
echo Repository Location: %CD%
echo.

REM Check if this is a git repository
if not exist ".git" (
    echo ERROR: This does not appear to be a git repository!
    echo Please run this script from the splunk_adv_v3 repository.
    echo.
    pause
    exit /b 1
)

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

pause
