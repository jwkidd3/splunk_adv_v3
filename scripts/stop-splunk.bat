@echo off
REM Stop Splunk Enterprise container
REM Windows

set SPLUNK_CONTAINER=splunk-course

echo ==========================================
echo Stopping Splunk Enterprise
echo ==========================================
echo.

REM Check if container exists and is running
docker ps --format "{{.Names}}" | findstr /x "%SPLUNK_CONTAINER%" >nul 2>&1
if not errorlevel 1 (
    echo Stopping container %SPLUNK_CONTAINER%...
    docker stop %SPLUNK_CONTAINER%
    echo * Splunk stopped successfully
) else (
    docker ps -a --format "{{.Names}}" | findstr /x "%SPLUNK_CONTAINER%" >nul 2>&1
    if not errorlevel 1 (
        echo Container %SPLUNK_CONTAINER% is already stopped
    ) else (
        echo Container %SPLUNK_CONTAINER% does not exist
    )
)

echo.
echo To start Splunk again: start-splunk.bat
echo To remove container completely: cleanup-splunk.bat
echo ==========================================

pause
