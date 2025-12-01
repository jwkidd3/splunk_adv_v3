#!/bin/bash
################################################################################
# Splunk Advanced Course - Update Script
################################################################################
# This script pulls the latest changes from the GitHub repository
# Run from scripts directory or execute directly
################################################################################

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "================================================================================"
echo "          SPLUNK ADVANCED COURSE - UPDATE FROM GITHUB"
echo "================================================================================"
echo ""

# Change to the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Go up one level to the repository root
cd ..

# Display current location
echo -e "${GREEN}Repository Location:${NC} $(pwd)"
echo ""

# Check if this is a git repository
if [ ! -d ".git" ]; then
    echo -e "${RED}ERROR: This does not appear to be a git repository!${NC}"
    echo "Please run this script from the splunk_adv_v3 repository."
    echo ""
    exit 1
fi

echo "Pulling latest changes from GitHub..."
echo "================================================================================"
echo ""

# Pull changes
if git pull; then
    echo ""
    echo "================================================================================"
    echo -e "${GREEN}SUCCESS: Repository updated successfully!${NC}"
    echo "================================================================================"
    echo ""
    echo "Latest changes have been downloaded."
    echo "You can now use the updated course materials."
    echo ""
else
    echo ""
    echo "================================================================================"
    echo -e "${RED}ERROR: Failed to update repository!${NC}"
    echo "================================================================================"
    echo ""
    echo "Please check:"
    echo "  1. Your internet connection"
    echo "  2. Your GitHub credentials"
    echo "  3. Any local changes that may conflict"
    echo ""
    echo "You may need to:"
    echo "  - Commit or stash your local changes"
    echo "  - Resolve merge conflicts"
    echo "  - Check your git configuration"
    echo ""
    exit 1
fi
