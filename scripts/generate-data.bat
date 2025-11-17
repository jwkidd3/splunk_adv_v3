@echo off
REM Generate sample data for Splunk Advanced Course
REM Windows

echo ======================================
echo Splunk Advanced Course Data Generator
echo ======================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3 and try again
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Run the data generation script
python generate_sample_data.py

if %errorlevel% equ 0 (
    echo.
    echo Success! Sample data has been generated.
    echo Check the sample_data\ directory for output files.
) else (
    echo.
    echo Data generation failed with exit code: %errorlevel%
    pause
    exit /b %errorlevel%
)

pause
