# Scripts Directory

This directory contains utility scripts for managing Splunk environment and course data.

## Overview

The scripts in this directory are **cross-platform compatible** and work on:
- **Windows** (PowerShell, Command Prompt, or Git Bash)
- **macOS** (Terminal)
- **Linux** (Bash)

## Scripts

### 1. Data Generation Script

**File:** `generate_sample_data.py`

**Purpose:** Generates sample log data files (~450,000 events) for the course labs.

**Usage:**

```bash
# Mac/Linux
python3 generate_sample_data.py

# Windows
python generate_sample_data.py
```

**What it does:**
- Generates 6 log files (~53MB total)
  - `web_access.log` (16MB) - Apache Combined Log Format
  - `application.log` (9.3MB) - Key-value format
  - `auth.log` (4.4MB) - Linux secure log format
  - `sales.log` (6.5MB) - JSON format
  - `performance.log` (4.5MB) - JSON format
  - `api.log` (12MB) - JSON format
- Generates 1 lookup file
  - `users.csv` (35KB) - CSV format
- Saves files to `../data/` directory
- Can be run multiple times (overwrites existing files)

**Output Location:** `data/` directory (relative to project root)

**Time Required:** ~30-60 seconds depending on system performance

---

### 2. Data Loading Script

**File:** `load_data_to_splunk.py`

**Purpose:** Loads generated sample data into Splunk Enterprise.

**Usage:**

```bash
# Mac/Linux
python3 load_data_to_splunk.py

# Windows
python load_data_to_splunk.py
```

**Prerequisites:**
- Splunk Enterprise must be running
- Sample data must be generated (run `generate_sample_data.py` first)
- Docker must be installed and running (for lookup file upload)

**What it does:**
1. Connects to Splunk REST API (localhost:8089)
2. Creates 6 indexes if they don't exist:
   - `web` - Web access logs
   - `app` - Application logs
   - `auth` - Authentication logs
   - `sales` - Sales transaction data
   - `performance` - Performance metrics
   - `api` - API request logs
3. Creates HEC (HTTP Event Collector) token
4. Loads data files into respective indexes
5. Uploads lookup files to Splunk

**Configuration:**
- Default credentials: `admin` / `password`
- Default Splunk URL: `https://localhost:8089`
- Can be modified in script header

**Cross-Platform Features:**
- Uses Python `pathlib.Path` for file paths
- Automatically detects OS (Windows, Darwin, Linux)
- Docker commands work on all platforms
- Handles path separators correctly

---

### 3. Splunk Start/Stop Scripts

**Windows Scripts:**
- `start-splunk.bat` - Start Splunk in Docker
- `stop-splunk.bat` - Stop Splunk Docker container

**Mac/Linux Scripts:**
- `start-splunk.sh` - Start Splunk in Docker
- `stop-splunk.sh` - Stop Splunk Docker container

**Usage:**

**Windows:**
```cmd
# Start Splunk
start-splunk.bat

# Stop Splunk
stop-splunk.bat
```

**Mac/Linux:**
```bash
# Start Splunk
bash start-splunk.sh

# Stop Splunk
bash stop-splunk.sh
```

---

## Complete Workflow

### First Time Setup

**Step 1: Generate Sample Data**

```bash
# Mac/Linux
cd scripts
python3 generate_sample_data.py

# Windows
cd scripts
python generate_sample_data.py
```

This creates all sample data files in the `data/` directory.

**Step 2: Start Splunk**

```bash
# Mac/Linux
bash start-splunk.sh

# Windows
start-splunk.bat
```

Wait for Splunk to fully start (~60 seconds).

**Step 3: Load Data into Splunk**

```bash
# Mac/Linux
python3 load_data_to_splunk.py

# Windows
python load_data_to_splunk.py
```

This loads all data files into Splunk indexes.

**Step 4: Access Splunk**

Open browser to: http://localhost:8000
- Username: `admin`
- Password: `password`

---

## Separation of Concerns

The data generation and data loading scripts are **intentionally separate** for the following reasons:

### Why Separate Scripts?

**1. Data Generation (`generate_sample_data.py`)**
- **Run Once:** Generate data files once, use many times
- **No Dependencies:** Doesn't require Splunk to be running
- **Fast Re-runs:** If Splunk crashes, don't regenerate data
- **Customization:** Students can modify data without affecting Splunk
- **Portability:** Data files can be shared or backed up

**2. Data Loading (`load_data_to_splunk.py`)**
- **Requires Splunk:** Only runs when Splunk is available
- **Repeatable:** Can reload data multiple times
- **Testing:** Can test different data loading strategies
- **Recovery:** If indexes are corrupted, reload from saved files
- **Flexibility:** Can load into different Splunk instances

### Benefits

✅ **Faster Development:** Generate data once, reload many times
✅ **Better Testing:** Test data loading without regenerating
✅ **Easier Debugging:** Isolate issues to generation vs loading
✅ **Data Persistence:** Keep generated data for reference
✅ **Resource Efficiency:** Don't waste time regenerating same data

---

## Troubleshooting

### Issue: "Splunk is not ready"

**Solution:**
1. Ensure Splunk is running: `docker ps`
2. Wait 60 seconds after starting Splunk
3. Check Splunk logs: `docker logs splunk-course`

### Issue: "File not found" errors

**Solution:**
1. Ensure you're in the `scripts/` directory
2. Run `generate_sample_data.py` first
3. Check `data/` directory exists: `ls ../data/`

### Issue: Docker command fails

**Solution:**
1. Ensure Docker is running
2. Check container is running: `docker ps | grep splunk`
3. On Windows, ensure Docker Desktop is started

### Issue: Python command not found

**Windows:**
- Use `python` instead of `python3`
- Install Python from python.org
- Add Python to PATH environment variable

**Mac:**
- Use `python3` instead of `python`
- Install Python 3: `brew install python3`

**Linux:**
- Use `python3` instead of `python`
- Install Python 3: `sudo apt-get install python3`

---

## Platform-Specific Notes

### Windows

**Command Prompt vs PowerShell:**
- Both work for Python scripts
- Use `.bat` files for Splunk management
- Path separators handled automatically by Python

**Python Installation:**
- Download from python.org
- Check "Add Python to PATH" during installation
- Use `python` command (not `python3`)

### macOS

**Python Version:**
- macOS includes Python 2.7 by default (use `python`)
- Install Python 3 via Homebrew: `brew install python3`
- Use `python3` command for scripts

**Permissions:**
- May need to make scripts executable: `chmod +x *.sh`
- Run with: `bash start-splunk.sh` or `./start-splunk.sh`

### Linux

**Python Installation:**
```bash
# Debian/Ubuntu
sudo apt-get install python3 python3-pip

# Red Hat/CentOS
sudo yum install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

**Docker Permissions:**
- Add user to docker group: `sudo usermod -aG docker $USER`
- Logout and login again

---

## Requirements

### Python Packages

Install required packages:

```bash
# Mac/Linux
pip3 install requests urllib3

# Windows
pip install requests urllib3
```

### System Requirements

- **Python:** 3.7 or higher
- **Docker:** Latest version
- **Disk Space:** 2GB free (for Splunk + data)
- **Memory:** 8GB RAM minimum
- **Network:** Ports 8000, 8088, 8089 available

---

## Advanced Usage

### Custom Splunk Credentials

Edit `load_data_to_splunk.py`:

```python
SPLUNK_USERNAME = "your_username"
SPLUNK_PASSWORD = "your_password"
```

### Custom Data Generation

Edit `generate_sample_data.py` to modify:
- Number of events per log file
- Date ranges
- Field values
- Log formats

### Remote Splunk Instance

Edit `load_data_to_splunk.py`:

```python
SPLUNK_HOST = "your-splunk-server.com"
SPLUNK_PORT = 8089
```

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review main course `README.md`
3. Check Splunk logs: `docker logs splunk-course`
4. Verify Docker is running: `docker ps`

---

**Last Updated:** November 2025
**Compatible Platforms:** Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
