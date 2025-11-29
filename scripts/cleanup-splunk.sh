#!/bin/bash
# Cleanup Splunk Enterprise container and data
# Mac/Linux

SPLUNK_CONTAINER="splunk-course"

echo "=========================================="
echo "Cleanup Splunk Enterprise"
echo "=========================================="
echo ""
echo "WARNING: This will remove the Splunk container"
echo "and all indexed data. This action cannot be undone."
echo ""
read -p "Continue? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled"
    exit 0
fi

echo ""
echo "Stopping and removing Splunk container..."

# Force stop and remove container (works even if container doesn't exist)
if docker rm -f ${SPLUNK_CONTAINER} >/dev/null 2>&1; then
    echo "✓ Container removed successfully"
else
    echo "✓ Container does not exist or already removed"
fi

# Remove associated volumes
echo ""
echo "Removing associated volumes..."
docker volume ls -q | grep splunk | xargs -r docker volume rm 2>/dev/null || true

echo ""
echo "=========================================="
echo "Cleanup Complete"
echo "=========================================="
echo ""
echo "To start fresh:"
echo "  1. ./start-splunk.sh"
echo "  2. ./generate-data.sh"
echo "  3. ./load-data.sh"
echo "=========================================="
