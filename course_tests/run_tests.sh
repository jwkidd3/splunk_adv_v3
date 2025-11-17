#!/bin/bash
# Simple wrapper script to run course tests
# Mac/Linux

echo "=============================================="
echo "Splunk Advanced Course - Test Suite"
echo "=============================================="
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if in correct directory
if [ ! -f "run_all_tests.py" ]; then
    echo "Error: run_all_tests.py not found"
    echo "Please run this script from the course_tests directory"
    exit 1
fi

# Run tests with provided arguments
python3 run_all_tests.py "$@"

exit $?
