# Data Loading Guide

## Overview

This guide shows how to manually load course data into Splunk. All data files are pre-generated and included in the repository.

## Prerequisites

- Splunk Enterprise running (via `start-splunk.bat` or `start-splunk.sh`)
- Access to Splunk Web at http://localhost:8000
- Login credentials: **admin** / **password**

## Data Files

All sample data files are located in the `data/` directory:

| File | Size | Events | Format |
|------|------|--------|--------|
| `web_access.log` | 16MB | ~150,000 | Apache Combined Log |
| `application.log` | 9.3MB | ~100,000 | Key-Value Pairs |
| `auth.log` | 4.4MB | ~50,000 | Linux Auth Log |
| `sales.log` | 6.5MB | ~50,000 | JSON |
| `performance.log` | 4.5MB | ~50,000 | JSON |
| `api.log` | 12MB | ~100,000 | JSON |
| `users.csv` | 35KB | 1,000 | CSV (Lookup File) |

**Total:** ~53MB, ~450,000 events

---

## Step-by-Step Data Loading

### Step 1: Create Indexes

1. Navigate to **Settings** → **Indexes**
2. Click **New Index** and create the following:

| Index Name | Notes |
|------------|-------|
| `web` | For web access logs |
| `app` | For application logs |
| `auth` | For authentication logs |
| `sales` | For sales transaction data |
| `performance` | For performance metrics |
| `api` | For API request logs |

**Settings for each index:**
- Home Path: Use defaults
- Max Size: Use defaults (500MB)
- Searchable Retention: Use defaults

### Step 2: Upload Data Files

For each data file, follow these steps:

1. Go to **Settings** → **Add Data**
2. Click **Upload**
3. Click **Select File** and choose the data file
4. Click **Next**

**Configure Source Type:**
- For `.log` files: Choose appropriate sourcetype or let Splunk auto-detect
- For `.json` files: Select `_json` or let Splunk auto-detect
- Click **Next**

**Input Settings:**
- **Host:** `course-data`
- **Index:** Select the appropriate index (see table below)
- Click **Review**
- Click **Submit**

### Data File to Index Mapping

| Data File | Index | Source Type |
|-----------|-------|-------------|
| `web_access.log` | `web` | `access_combined` |
| `application.log` | `app` | Auto-detect (key-value) |
| `auth.log` | `auth` | Auto-detect (key-value) |
| `sales.log` | `sales` | Auto-detect (key-value) |
| `performance.log` | `performance` | Auto-detect (key-value) |
| `api.log` | `api` | `_json` |

### Step 3: Upload Lookup File

1. Go to **Settings** → **Lookups**
2. Click **Lookup table files** → **New Lookup Table File**
3. **Destination app:** Search & Reporting
4. **Upload file:** Select `data/users.csv`
5. **Destination filename:** `users.csv`
6. Click **Save**

---

## Verification

### Check Data Ingestion

Run these searches in Splunk to verify data was loaded:

```spl
index=web | stats count
index=app | stats count
index=auth | stats count
index=sales | stats count
index=performance | stats count
index=api | stats count
```

### Expected Event Counts

| Index | Expected Events |
|-------|----------------|
| `web` | ~150,000 |
| `app` | ~100,000 |
| `auth` | ~50,000 |
| `sales` | ~50,000 |
| `performance` | ~50,000 |
| `api` | ~100,000 |
| **TOTAL** | **~450,000** |

### Verify Lookup File

```spl
| inputlookup users.csv | stats count
```

**Expected:** 1,000 users

---

## Troubleshooting

### Data Not Appearing

1. **Check index permissions:** Ensure user role has access to custom indexes
2. **Check time range:** Data is timestamped from recent dates - use "All time" search
3. **Check data input status:** Settings → Data Inputs → Files & Directories
4. **Check internal logs:** `index=_internal source=*metrics.log`

### File Upload Errors

- **File too large:** Increase `max_content_length` in `limits.conf` (default: 2GB should be sufficient)
- **Permission denied:** Ensure Docker container has access to files
- **Upload timeout:** For large files, use Method 2 (monitoring) instead

### Lookup File Not Found

1. Verify file uploaded: Settings → Lookups → Lookup table files
2. Check filename matches: Should be exactly `users.csv`
3. Verify permissions: Ensure "Read" permissions are set for all roles

---

## Quick Start (Recommended Flow)

1. **Start Splunk**
   - Windows: `start-splunk.bat`
   - Mac/Linux: `./start-splunk.sh`

2. **Create Indexes** (one-time setup)
   - Create 6 indexes: web, app, auth, sales, performance, api

3. **Upload Data Files** (one-time setup)
   - Upload 6 data files via Settings → Add Data → Upload

4. **Upload Lookup File** (one-time setup)
   - Upload users.csv via Settings → Lookups

5. **Configure Field Extractions** (one-time setup)
   - See FIELD_EXTRACTION_GUIDE.md for detailed instructions
   - Configure `response_time` field extraction for web logs

6. **Verify Data**
   - Run verification searches to confirm ~450,000 events total
   - Verify field extractions are working

**Total Time:** ~20-25 minutes (one-time setup)

---

## Notes

- Data files are **pre-generated** and included in the repository
- Data has timestamps from recent dates for realistic searching
- All data is **synthetic** - safe for training purposes
- Data persists in Splunk container until you run `cleanup-splunk.bat/sh`
- You can reload data anytime by re-uploading the files
- **IMPORTANT:** After loading data, configure field extractions per FIELD_EXTRACTION_GUIDE.md

---

## For Instructors

If you need to regenerate data (not required for students):

```bash
cd scripts
python3 generate_sample_data.py
```

This will regenerate all files in the `data/` directory.
