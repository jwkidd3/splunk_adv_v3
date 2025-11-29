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

# Check and install Python dependencies
echo "Checking Python dependencies..."
echo ""

# Determine Python command
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "Error: Python not found"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

echo "Using Python: $PYTHON_CMD ($($PYTHON_CMD --version 2>&1))"

# Check if pip is available
if ! command -v $PIP_CMD >/dev/null 2>&1; then
    echo "Error: pip not found"
    echo "Please install pip (Python package manager)"
    exit 1
fi

# Check for requests package
if ! $PYTHON_CMD -c "import requests" >/dev/null 2>&1; then
    echo "Installing required package: requests..."
    $PIP_CMD install requests>=2.31.0 --quiet || {
        echo "Warning: Failed to install requests automatically"
        echo "Please install manually: $PIP_CMD install requests"
    }
fi

# Check for urllib3 package
if ! $PYTHON_CMD -c "import urllib3" >/dev/null 2>&1; then
    echo "Installing required package: urllib3..."
    $PIP_CMD install urllib3>=2.0.0 --quiet || {
        echo "Warning: Failed to install urllib3 automatically"
        echo "Please install manually: $PIP_CMD install urllib3"
    }
fi

# Final verification
if $PYTHON_CMD -c "import requests, urllib3" >/dev/null 2>&1; then
    echo "✓ All Python dependencies installed"
else
    echo "Warning: Some dependencies may not be installed"
    echo "You can install them manually with:"
    echo "  $PIP_CMD install -r ../requirements.txt"
fi

echo ""

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
