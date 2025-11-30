# Scripts Directory

This directory contains utility scripts for managing the Splunk environment and course data.

## Overview

All scripts are **cross-platform compatible** and work on:
- **Windows** (PowerShell or Command Prompt)
- **macOS** (Terminal)
- **Linux** (Bash)

---

## For Students

Students use only these scripts to manage Splunk:

### Start Splunk

**Windows:**
```cmd
start-splunk.bat
```

**Mac/Linux:**
```bash
bash start-splunk.sh
```

**What it does:**
- Starts Splunk Enterprise in Docker container
- Maps ports 8000 (Web), 8088 (HEC), 8089 (Management)
- Sets admin password to "password"
- Wait ~60 seconds for Splunk to be ready

**Access Splunk:**
- URL: http://localhost:8000
- Username: `admin`
- Password: `password`

### Stop Splunk

**Windows:**
```cmd
stop-splunk.bat
```

**Mac/Linux:**
```bash
bash stop-splunk.sh
```

**What it does:**
- Gracefully stops the Splunk Docker container
- Preserves all data and configurations

### Cleanup Splunk

**Windows:**
```cmd
cleanup-splunk.bat
```

**Mac/Linux:**
```bash
bash cleanup-splunk.sh
```

**What it does:**
- Stops and removes the Splunk container
- **WARNING:** Deletes all data and configurations
- Use this to start fresh if needed

---

## For Instructors

### Data Generation Script

**File:** `generate_sample_data.py`

**Purpose:** Generates all sample log data files for the course.

**Usage:**
```bash
# Mac/Linux
python3 generate_sample_data.py

# Windows
python generate_sample_data.py
```

**What it generates:**
- 6 log files (~53MB total, ~350,000 events):
  - `web_access.log` (16MB) - Apache Combined Log Format with Cookie
  - `application.log` (9.3MB) - Key-value format
  - `auth.log` (4.4MB) - Key-value format
  - `sales.log` (6.5MB) - Key-value format
  - `performance.log` (4.5MB) - Key-value format
  - `api.log` (12MB) - JSON format
- 1 lookup file:
  - `users.csv` (35KB) - CSV format

**Output Location:** `../data/` directory

**Time Required:** ~30-60 seconds

**Note:** Data is already pre-generated and included in the repository. Only regenerate if you need to modify the data.

### Data Loading Script

**File:** `load_data_to_splunk.py`

**Purpose:** Automatically loads all sample data into Splunk (alternative to manual upload in Lab 1).

**Usage:**
```bash
# Mac/Linux
python3 load_data_to_splunk.py

# Windows
python load_data_to_splunk.py
```

**Prerequisites:**
- Splunk must be running (`start-splunk.sh` or `start-splunk.bat`)
- Sample data exists in `../data/` directory

**What it does:**
1. Connects to Splunk REST API (localhost:8089)
2. Creates 6 indexes: web, app, auth, sales, performance, api
3. Creates HEC token for data ingestion
4. Loads all data files into respective indexes using structured JSON
5. Uploads users.csv lookup file via Docker

**Configuration:**
- Default credentials: `admin` / `password`
- Default Splunk URL: `https://localhost:8089`
- Modify in script header if needed

**Note:** Students are instructed to manually upload data via Splunk UI (Lab 1). This script is useful for automated testing or instructor setup.

---

## Workflow

### For Students (Recommended)

1. **Start Splunk:**
   ```bash
   # Mac/Linux: bash start-splunk.sh
   # Windows: start-splunk.bat
   ```

2. **Complete Lab 1:**
   - Follow `labs/lab1-setup-data-environment/README.md`
   - Manually upload data files via Splunk Web UI
   - Configure field extractions

3. **Stop Splunk when done:**
   ```bash
   # Mac/Linux: bash stop-splunk.sh
   # Windows: stop-splunk.bat
   ```

### For Instructors/Automation

1. **Start Splunk:**
   ```bash
   bash start-splunk.sh  # or start-splunk.bat on Windows
   ```

2. **Load data automatically:**
   ```bash
   python3 load_data_to_splunk.py  # or python on Windows
   ```

3. **Access Splunk:**
   - http://localhost:8000
   - Username: `admin`
   - Password: `password`

---

## Requirements

### For Students
- **Docker:** Latest version
- **Disk Space:** 2GB free
- **Memory:** 8GB RAM minimum
- **Network:** Ports 8000, 8088, 8089 available

### For Instructors (Data Generation/Loading)
- All student requirements, plus:
- **Python:** 3.7 or higher
- **Python Packages:**
  ```bash
  # Mac/Linux
  pip3 install requests urllib3

  # Windows
  pip install requests urllib3
  ```

---

## Troubleshooting

### Splunk won't start
1. Check Docker is running: `docker ps`
2. Check port availability: `docker ps | grep 8000`
3. Kill any conflicting containers: `docker rm -f splunk-course`

### Data loading fails
1. Ensure Splunk is running and accessible
2. Wait 60 seconds after starting Splunk
3. Check Splunk logs: `docker logs splunk-course`

### Python command not found
- **Windows:** Use `python` (not `python3`)
- **Mac/Linux:** Use `python3` (not `python`)
- Install Python from python.org

---

## File Listing

**Splunk Management Scripts (Students use these):**
- `start-splunk.bat` / `start-splunk.sh` - Start Splunk
- `stop-splunk.bat` / `stop-splunk.sh` - Stop Splunk
- `cleanup-splunk.bat` / `cleanup-splunk.sh` - Remove Splunk completely

**Data Scripts (Instructors only):**
- `generate_sample_data.py` - Generate sample data files
- `load_data_to_splunk.py` - Automatically load data to Splunk

**Other:**
- `README.md` - This file
- `course_tests/` - Directory for course validation tests

---

**Last Updated:** November 2025
**Compatible Platforms:** Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
