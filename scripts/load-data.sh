#!/bin/bash
# Load sample data into Splunk
# Mac/Linux

echo "=========================================="
echo "Load Data into Splunk"
echo "=========================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if data has been generated
if [ ! -d "sample_data" ]; then
    echo "Error: Sample data not found"
    echo "Please generate data first:"
    echo "  ./generate-data.sh"
    exit 1
fi

# Check if Splunk is running
if ! curl -k -s -u admin:password https://localhost:8089/services/server/info >/dev/null 2>&1; then
    echo "Error: Splunk is not running or not accessible"
    echo "Please start Splunk first:"
    echo "  ./start-splunk.sh"
    exit 1
fi

# Run data loader
python3 load_data_to_splunk.py

exit $?
