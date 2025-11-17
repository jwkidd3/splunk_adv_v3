@echo off
REM Load sample data into Splunk
REM Windows

echo ==========================================
echo Load Data into Splunk
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3 and try again
    pause
    exit /b 1
)

REM Check if data has been generated
if not exist "sample_data\" (
    echo Error: Sample data not found
    echo Please generate data first:
    echo   generate-data.bat
    pause
    exit /b 1
)

REM Check if Splunk is running
curl -k -s -u admin:password https://localhost:8089/services/server/info >nul 2>&1
if errorlevel 1 (
    echo Error: Splunk is not running or not accessible
    echo Please start Splunk first:
    echo   start-splunk.bat
    pause
    exit /b 1
)

REM Run data loader
python load_data_to_splunk.py

if %errorlevel% equ 0 (
    echo.
    echo Data loaded successfully!
) else (
    echo.
    echo Data loading completed with errors.
)

pause
