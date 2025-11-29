#!/bin/bash
# Start Splunk Enterprise in Docker
# Mac/Linux

set -e

SPLUNK_CONTAINER="splunk-course"
SPLUNK_IMAGE="splunk/splunk:latest"
SPLUNK_PASSWORD="password"
SPLUNK_WEB_PORT=8000
SPLUNK_MGMT_PORT=8089
SPLUNK_HEC_PORT=8088

echo "=========================================="
echo "Starting Splunk Enterprise (Docker)"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

# Check and install Python dependencies (optional - won't block Splunk startup)
echo "Checking Python dependencies..."
echo ""

# Determine Python command
PYTHON_AVAILABLE=0
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    PYTHON_AVAILABLE=1
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
    PYTHON_AVAILABLE=1
fi

if [ $PYTHON_AVAILABLE -eq 0 ]; then
    echo "WARNING: Python not found"
    echo ""
    echo "Python is required for data generation and loading scripts."
    echo "Splunk will start, but you'll need Python to load course data."
    echo ""
    echo "To install Python:"
    echo "  macOS: brew install python3"
    echo "  Linux: sudo apt-get install python3 python3-pip"
    echo "  Or visit: https://www.python.org/downloads/"
    echo ""
    echo "Continuing with Splunk startup..."
    echo ""
else
    echo "Using Python: $PYTHON_CMD ($($PYTHON_CMD --version 2>&1))"

    # Check if pip is available
    if ! command -v $PIP_CMD >/dev/null 2>&1; then
        echo "pip not found - attempting to install..."
        if $PYTHON_CMD -m ensurepip --upgrade >/dev/null 2>&1; then
            echo "✓ pip installed successfully"
            if ! command -v $PIP_CMD >/dev/null 2>&1; then
                PIP_CMD="$PYTHON_CMD -m pip"
            fi
        else
            echo "WARNING: Failed to install pip"
            echo "You may need to install packages manually later"
        fi
    fi

    # Check for requests package (non-blocking)
    if command -v $PIP_CMD >/dev/null 2>&1; then
        if ! $PYTHON_CMD -c "import requests" >/dev/null 2>&1; then
            echo "Installing required package: requests..."
            $PIP_CMD install requests>=2.31.0 --quiet >/dev/null 2>&1 || true
        fi

        # Check for urllib3 package (non-blocking)
        if ! $PYTHON_CMD -c "import urllib3" >/dev/null 2>&1; then
            echo "Installing required package: urllib3..."
            $PIP_CMD install urllib3>=2.0.0 --quiet >/dev/null 2>&1 || true
        fi

        # Final verification
        if $PYTHON_CMD -c "import requests, urllib3" >/dev/null 2>&1; then
            echo "✓ All Python dependencies installed"
        else
            echo "WARNING: Some Python dependencies missing"
            echo "Run: $PIP_CMD install -r requirements.txt"
        fi
    fi

    echo ""
fi

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${SPLUNK_CONTAINER}$"; then
    echo "Container ${SPLUNK_CONTAINER} already exists"

    # Check if it's running
    if docker ps --format '{{.Names}}' | grep -q "^${SPLUNK_CONTAINER}$"; then
        echo "Container is already running"
        echo ""
        echo "Splunk Web: http://localhost:${SPLUNK_WEB_PORT}"
        echo "Username: admin"
        echo "Password: ${SPLUNK_PASSWORD}"
        exit 0
    else
        echo "Starting existing container..."
        docker start ${SPLUNK_CONTAINER}
    fi
else
    echo "Creating new Splunk container..."
    docker run -d \
        --platform linux/amd64 \
        --name ${SPLUNK_CONTAINER} \
        -p ${SPLUNK_WEB_PORT}:8000 \
        -p ${SPLUNK_MGMT_PORT}:8089 \
        -p ${SPLUNK_HEC_PORT}:8088 \
        -e "SPLUNK_GENERAL_TERMS=--accept-sgt-current-at-splunk-com" \
        -e "SPLUNK_START_ARGS=--accept-license" \
        -e "SPLUNK_PASSWORD=${SPLUNK_PASSWORD}" \
        ${SPLUNK_IMAGE}
fi

echo ""
echo "Waiting for Splunk to start (this may take 1-2 minutes)..."
echo ""

# Wait for Splunk to be ready
MAX_WAIT=180
ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT ]; do
    if curl -k -s -u admin:${SPLUNK_PASSWORD} https://localhost:${SPLUNK_MGMT_PORT}/services/server/info >/dev/null 2>&1; then
        echo ""
        echo "✓ Splunk is ready!"
        break
    fi

    echo -n "."
    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo ""
    echo "✗ Timeout waiting for Splunk to start"
    echo "Check container logs: docker logs ${SPLUNK_CONTAINER}"
    exit 1
fi

echo ""
echo "=========================================="
echo "Splunk Enterprise Started Successfully"
echo "=========================================="
echo ""
echo "Access Splunk Web:"
echo "  URL: http://localhost:${SPLUNK_WEB_PORT}"
echo "  Username: admin"
echo "  Password: ${SPLUNK_PASSWORD}"
echo ""
echo "Management Port: ${SPLUNK_MGMT_PORT}"
echo "Container: ${SPLUNK_CONTAINER}"
echo ""
echo "View logs: docker logs -f ${SPLUNK_CONTAINER}"
echo "Stop Splunk: ./stop-splunk.sh"
echo "=========================================="
