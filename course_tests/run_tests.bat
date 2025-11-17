@echo off
REM Simple wrapper script to run course tests
REM Windows

echo ==============================================
echo Splunk Advanced Course - Test Suite
echo ==============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3 and try again
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist run_all_tests.py (
    echo Error: run_all_tests.py not found
    echo Please run this script from the course_tests directory
    pause
    exit /b 1
)

REM Run tests with provided arguments
python run_all_tests.py %*

if %errorlevel% equ 0 (
    echo.
    echo Tests completed successfully!
) else (
    echo.
    echo Tests completed with failures. Check the report for details.
)

pause
