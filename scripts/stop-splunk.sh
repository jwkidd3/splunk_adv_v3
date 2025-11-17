#!/bin/bash
# Stop Splunk Enterprise container
# Mac/Linux

SPLUNK_CONTAINER="splunk-course"

echo "=========================================="
echo "Stopping Splunk Enterprise"
echo "=========================================="
echo ""

# Check if container exists and is running
if docker ps --format '{{.Names}}' | grep -q "^${SPLUNK_CONTAINER}$"; then
    echo "Stopping container ${SPLUNK_CONTAINER}..."
    docker stop ${SPLUNK_CONTAINER}
    echo "✓ Splunk stopped successfully"
else
    if docker ps -a --format '{{.Names}}' | grep -q "^${SPLUNK_CONTAINER}$"; then
        echo "Container ${SPLUNK_CONTAINER} is already stopped"
    else
        echo "Container ${SPLUNK_CONTAINER} does not exist"
    fi
fi

echo ""
echo "To start Splunk again: ./start-splunk.sh"
echo "To remove container completely: ./cleanup-splunk.sh"
echo "=========================================="
