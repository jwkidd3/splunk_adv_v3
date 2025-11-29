@echo off
REM Start Splunk Enterprise in Docker
REM Windows

setlocal enabledelayedexpansion

set SPLUNK_CONTAINER=splunk-course
set SPLUNK_IMAGE=splunk/splunk:latest
set SPLUNK_PASSWORD=password
set SPLUNK_WEB_PORT=8000
set SPLUNK_MGMT_PORT=8089
set SPLUNK_HEC_PORT=8088

echo ==========================================
echo Starting Splunk Enterprise (Docker)
echo ==========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

REM Check and install Python dependencies (optional - won't block Splunk startup)
echo Checking Python dependencies...
echo.

REM Determine Python command
set PYTHON_CMD=
set PIP_CMD=
set PYTHON_AVAILABLE=0

where python >nul 2>&1
if not errorlevel 1 (
    set PYTHON_CMD=python
    set PIP_CMD=pip
    set PYTHON_AVAILABLE=1
) else (
    where python3 >nul 2>&1
    if not errorlevel 1 (
        set PYTHON_CMD=python3
        set PIP_CMD=pip3
        set PYTHON_AVAILABLE=1
    )
)

if %PYTHON_AVAILABLE%==0 (
    echo Python not found - attempting automatic installation...
    echo.

    REM Check if winget is available (Windows 10/11)
    where winget >nul 2>&1
    if not errorlevel 1 (
        echo Installing Python 3.13 using Windows Package Manager...
        echo This will take 2-3 minutes...
        echo.

        REM Install Python silently
        winget install -e --id Python.Python.3.13 --silent --accept-package-agreements --accept-source-agreements

        if not errorlevel 1 (
            echo.
            echo ==========================================
            echo Python 3.13 installed successfully!
            echo ==========================================
            echo.
            echo Python has been installed, but Splunk will start now.
            echo After Splunk starts, you can run the data loading scripts.
            echo.

            REM Try to detect Python again after installation
            where python >nul 2>&1
            if not errorlevel 1 (
                set PYTHON_CMD=python
                set PIP_CMD=pip
                set PYTHON_AVAILABLE=1
            )
        ) else (
            echo.
            echo WARNING: Python installation failed
            echo You can install manually from https://www.python.org/downloads/
            echo.
        )
    ) else (
        echo.
        echo WARNING: Windows Package Manager not available
        echo.
        echo To install Python manually:
        echo   1. Download from https://www.python.org/downloads/
        echo   2. Run installer and check "Add Python to PATH"
        echo.
    )

    echo Continuing with Splunk startup...
    echo.

    if %PYTHON_AVAILABLE%==0 goto :skip_python
)

REM Get Python version
for /f "tokens=*" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Using Python: %PYTHON_CMD% (%PYTHON_VERSION%)

REM Check if pip is available
where %PIP_CMD% >nul 2>&1
if errorlevel 1 (
    echo pip not found - attempting to install...
    %PYTHON_CMD% -m ensurepip --upgrade >nul 2>&1
    if not errorlevel 1 (
        echo * pip installed successfully
        where %PIP_CMD% >nul 2>&1
        if errorlevel 1 (
            set PIP_CMD=%PYTHON_CMD% -m pip
        )
    ) else (
        echo WARNING: Failed to install pip
        echo You may need to install packages manually later
        goto :skip_python
    )
)

REM Check for requests package
%PYTHON_CMD% -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo Installing required package: requests...
    %PIP_CMD% install requests>=2.31.0 --quiet >nul 2>&1
)

REM Check for urllib3 package
%PYTHON_CMD% -c "import urllib3" >nul 2>&1
if errorlevel 1 (
    echo Installing required package: urllib3...
    %PIP_CMD% install urllib3>=2.0.0 --quiet >nul 2>&1
)

REM Final verification
%PYTHON_CMD% -c "import requests, urllib3" >nul 2>&1
if not errorlevel 1 (
    echo * All Python dependencies installed
) else (
    echo WARNING: Some Python dependencies missing
    echo Run: %PIP_CMD% install -r requirements.txt
)

echo.

:skip_python

REM Check if container already exists
docker ps -a --format "{{.Names}}" | findstr /x "%SPLUNK_CONTAINER%" >nul 2>&1
if not errorlevel 1 (
    echo Container %SPLUNK_CONTAINER% already exists

    REM Check if it's running
    docker ps --format "{{.Names}}" | findstr /x "%SPLUNK_CONTAINER%" >nul 2>&1
    if not errorlevel 1 (
        echo Container is already running
        echo.
        echo Splunk Web: http://localhost:%SPLUNK_WEB_PORT%
        echo Username: admin
        echo Password: %SPLUNK_PASSWORD%
        pause
        exit /b 0
    ) else (
        echo Starting existing container...
        docker start %SPLUNK_CONTAINER%
    )
) else (
    echo Creating new Splunk container...
    docker run -d ^
        --platform linux/amd64 ^
        --name %SPLUNK_CONTAINER% ^
        -p %SPLUNK_WEB_PORT%:8000 ^
        -p %SPLUNK_MGMT_PORT%:8089 ^
        -p %SPLUNK_HEC_PORT%:8088 ^
        -e "SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com" ^
        -e "SPLUNK_START_ARGS=--accept-license" ^
        -e "SPLUNK_PASSWORD=%SPLUNK_PASSWORD%" ^
        %SPLUNK_IMAGE%
)

echo.
echo Waiting for Splunk to start (this may take 1-2 minutes)...
echo.

REM Wait for Splunk to be ready
set MAX_WAIT=90
set ELAPSED=0

:wait_loop
if !ELAPSED! geq !MAX_WAIT! goto timeout

curl -k -s -u admin:%SPLUNK_PASSWORD% https://localhost:%SPLUNK_MGMT_PORT%/services/server/info >nul 2>&1
if not errorlevel 1 (
    echo.
    echo * Splunk is ready!
    goto ready
)

echo|set /p="."
timeout /t 2 /nobreak >nul
set /a ELAPSED+=1
goto wait_loop

:timeout
echo.
echo * Timeout waiting for Splunk to start
echo Check container logs: docker logs %SPLUNK_CONTAINER%
pause
exit /b 1

:ready
echo.
echo ==========================================
echo Splunk Enterprise Started Successfully
echo ==========================================
echo.
echo Access Splunk Web:
echo   URL: http://localhost:%SPLUNK_WEB_PORT%
echo   Username: admin
echo   Password: %SPLUNK_PASSWORD%
echo.
echo Management Port: %SPLUNK_MGMT_PORT%
echo Container: %SPLUNK_CONTAINER%
echo.
echo View logs: docker logs -f %SPLUNK_CONTAINER%
echo Stop Splunk: stop-splunk.bat
echo ==========================================

pause
