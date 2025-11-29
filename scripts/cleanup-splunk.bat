@echo off
REM Cleanup Splunk Enterprise container and data
REM Windows

set SPLUNK_CONTAINER=splunk-course

echo ==========================================
echo Cleanup Splunk Enterprise
echo ==========================================
echo.
echo WARNING: This will remove the Splunk container
echo and all indexed data. This action cannot be undone.
echo.

set /p CONFIRM="Continue? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo Cleanup cancelled
    pause
    exit /b 0
)

echo.
echo Stopping and removing Splunk container...

REM Force stop and remove container (works even if container doesn't exist)
docker rm -f %SPLUNK_CONTAINER% >nul 2>&1
if not errorlevel 1 (
    echo * Container removed successfully
) else (
    echo * Container does not exist or already removed
)

REM Remove associated volumes
echo.
echo Removing associated volumes...
for /f "tokens=*" %%v in ('docker volume ls -q ^| findstr splunk') do (
    docker volume rm %%v 2>nul
)

echo.
echo ==========================================
echo Cleanup Complete
echo ==========================================
echo.
echo To start fresh:
echo   1. start-splunk.bat
echo   2. generate-data.bat
echo   3. load-data.bat
echo ==========================================

pause
