#!/bin/bash
# Generate sample data for Splunk Advanced Course
# Mac/Linux

echo "======================================"
echo "Splunk Advanced Course Data Generator"
echo "======================================"
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Run the data generation script
python3 generate_sample_data.py

exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo ""
    echo "Success! Sample data has been generated."
    echo "Check the sample_data/ directory for output files."
else
    echo ""
    echo "Data generation failed with exit code: $exit_code"
    exit $exit_code
fi
