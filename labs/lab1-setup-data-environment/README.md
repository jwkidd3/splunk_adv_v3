# Lab 1: Setup Data Environment

**Duration:** 30 minutes
**Difficulty:** Beginner
**Prerequisites:** Splunk Enterprise running (via start-splunk script)

## Lab Objectives

By the end of this lab, you will be able to:
- Create custom indexes in Splunk
- Upload data files via the Splunk Web UI
- Configure lookup files for data enrichment
- Create custom field extractions
- Verify data ingestion and field extraction

## Overview

This lab sets up the complete data environment needed for all subsequent labs in this course. You will load ~350,000 events across 6 different data sources and configure one custom field extraction.

**Data Summary:**
- **web_access.log** - 100,000 Apache web server logs (16MB) - Apache Combined Log Format with Cookie
- **application.log** - 75,000 application events (9.3MB) - Key-Value format
- **auth.log** - 37,500 authentication events (4.4MB) - Key-Value format
- **sales.log** - 50,000 sales transactions (6.5MB) - Key-Value format
- **performance.log** - 30,000 system metrics (4.5MB) - Key-Value format
- **api.log** - 60,000 API requests (12MB) - JSON format
- **users.csv** - 500 user profiles (35KB) - CSV lookup file

**Total:** ~53MB, ~350,000 events

### Data Formats and Field Extraction

| File | Format | Sourcetype | Auto-Extraction | Custom Extraction Needed |
|------|--------|------------|-----------------|--------------------------|
| `web_access.log` | Apache Combined + Cookie + response_time | `access_combined_wcookie` | Most fields | **YES** - `response_time` field |
| `application.log` | Key-Value | Auto-detected | All fields | NO |
| `auth.log` | Key-Value | Auto-detected | All fields | NO |
| `sales.log` | Key-Value | Auto-detected | All fields | NO |
| `performance.log` | Key-Value | Auto-detected | All fields | NO |
| `api.log` | JSON | `_json` | All fields | NO |
| `users.csv` | CSV | N/A (lookup) | N/A | NO |

**Important:** Only `web_access.log` requires custom field extraction. All other files use formats that Splunk automatically extracts.

---

## Exercise 1: Create Indexes (5 minutes)

Indexes organize your data into separate collections for better search performance and access control.

**Tasks:**

1. **Navigate to Indexes:**
   - Log into Splunk Web: http://localhost:8000
   - Username: `admin`, Password: `password`
   - Go to **Settings** → **Indexes**

2. **Create the following indexes:**

   Click **New Index** for each and use these settings:

   | Index Name | Purpose |
   |------------|---------|
   | `web` | Web access logs |
   | `app` | Application logs |
   | `auth` | Authentication logs |
   | `sales` | Sales transaction data |
   | `performance` | Performance metrics |
   | `api` | API request logs |

   **For each index:**
   - **Index Name:** Enter the name from the table above
   - **Home Path:** Leave as default
   - **Max Size:** Leave as default (500MB)
   - Click **Save**

3. **Verify:**
   - You should now see 6 new indexes in the list
   - All should show "Enabled" status

---

## Exercise 2: Upload Data Files (15 minutes)

You will upload each data file and assign it to the correct index.

**Data File Locations:**
All files are in the `data/` directory of the course repository.

### Upload Process (repeat for each file):

1. **Go to Add Data:**
   - **Settings** → **Add Data**
   - Click **Upload**

2. **Select File:**
   - Click **Select File**
   - Navigate to the `data/` directory
   - Choose the file (see table below)
   - Click **Next**

3. **Set Source Type:**
   - **For web_access.log**:
     - In the "Select Source Type" dropdown, choose `access_combined_wcookie`
     - Click **Next**

   - **For application.log** (first key-value file):
     - Splunk will default to "default" sourcetype
     - Click **Next**
     - Splunk will prompt you with a dialog to create a new sourcetype
     - **In the dialog:**
       - Enter a name like `application_kv` or accept the suggested name
       - Click **Save**
     - This sourcetype will be reused for the other key-value files

   - **For auth.log, sales.log, performance.log** (subsequent key-value files):
     - In the "Select Source Type" dropdown, choose the sourcetype you created for application.log (e.g., `application_kv`)
     - Click **Next**
     - OR: If you let it default to "default" and click Next, create a new sourcetype for each file (both approaches work)

   - **For api.log**:
     - In the "Select Source Type" dropdown, choose `_json`
     - Click **Next**

4. **Input Settings (CRITICAL - do this for EVERY file):**
   - **Host:** Type `course-data` (use this exact value for ALL 6 files)
   - **Index:** Select the appropriate index from the table below
   - Click **Review**

   **IMPORTANT:** You must enter `course-data` as the host value for each file you upload. This is required for all 6 data files.

5. **Submit:**
   - Review the settings
   - Click **Submit**
   - Wait for "File has been uploaded successfully" message

### Data File Configuration:

| File | Index | Host | Source Type | Notes |
|------|-------|------|-------------|-------|
| `web_access.log` | `web` | `course-data` | `access_combined_wcookie` | Apache web logs |
| `application.log` | `app` | `course-data` | Auto-detected | Key-value format - accept auto-detected sourcetype |
| `auth.log` | `auth` | `course-data` | Auto-detected | Key-value format - accept auto-detected sourcetype |
| `sales.log` | `sales` | `course-data` | Auto-detected | Key-value format - accept auto-detected sourcetype |
| `performance.log` | `performance` | `course-data` | Auto-detected | Key-value format - accept auto-detected sourcetype |
| `api.log` | `api` | `course-data` | `_json` | JSON format |

**IMPORTANT:**
- Use `course-data` as the **Host** value for ALL files above
- For key-value files (application, auth, sales, performance), accept whatever sourcetype name Splunk auto-detects

**Expected time:** ~2-3 minutes per file

---

## Exercise 3: Upload Lookup File (3 minutes)

Lookup files provide additional data that can be joined with your event data.

**Tasks:**

1. **Navigate to Lookups:**
   - **Settings** → **Lookups**
   - Click **Lookup table files**
   - Click **New Lookup Table File**

2. **Upload the lookup:**
   - **Destination app:** Search & Reporting (or search)
   - Click **Choose File**
   - Select `data/users.csv`
   - **Destination filename:** `users.csv`
   - Click **Save**

3. **Verify:**
   - You should see `users.csv` in the lookup table files list
   - File size should be ~35KB

---

## Exercise 4: Verify Data Ingestion (3 minutes)

Confirm all data has been loaded correctly.

**Tasks:**

1. **Go to Search & Reporting app**

2. **Check each index:**

   Run these searches (set time range to "All time"):

   ```spl
   index=web | stats count
   ```
   **Expected:** ~100,000 events

   ```spl
   index=app | stats count
   ```
   **Expected:** ~75,000 events

   ```spl
   index=auth | stats count
   ```
   **Expected:** ~37,500 events

   ```spl
   index=sales | stats count
   ```
   **Expected:** ~50,000 events

   ```spl
   index=performance | stats count
   ```
   **Expected:** ~30,000 events

   ```spl
   index=api | stats count
   ```
   **Expected:** ~60,000 events

3. **Verify lookup file:**

   ```spl
   | inputlookup users.csv | stats count
   ```
   **Expected:** 500 users

4. **Check total events:**

   ```spl
   index=* | stats count
   ```
   **Expected:** ~350,000 events (excluding internal Splunk indexes)

---

## Exercise 5: Configure Field Extraction (4 minutes)

The web access logs include a custom `response_time` field that needs manual extraction.

**Why needed:** Labs 2, 4, 8, and 9 use the `response_time` field for performance analysis. This field is appended to the standard Apache log format and requires custom extraction.

**Sample log line:**
```
192.168.1.100 - user1 [29/Nov/2025:10:30:45 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 150ms
```

### Configure the extraction:

1. **Navigate to Field Extractions:**
   - **Settings** → **Fields** → **Field extractions**
   - Click **New Field Extraction**

2. **Name the Extraction:**
   - **Name:** `response_time_extraction` (or any descriptive name)
   - **Destination app:** Search & Reporting (or search)

3. **Specify Source:**
   - **Sourcetype:** `access_combined_wcookie`
   - Click to select the sourcetype

4. **Define Extraction Type:**
   - **Type:** Select **Inline**
   - This allows you to enter the regex directly

5. **Enter the Extraction:**
   - **Extraction/Transform:** Paste the following regular expression in the field:
     ```
     \s(?<response_time>\d+)ms$
     ```
   - This regex extracts the numeric value before "ms" at the end of each log line

6. **Save:**
   - Click **Save** to create the field extraction

7. **Verify the extraction:**

   Run this search:
   ```spl
   index=web | head 10 | table clientip method status response_time
   ```

   **Expected:** You should see the `response_time` field populated with numeric values (10-2000)

7. **Test performance queries:**

   ```spl
   index=web | stats avg(response_time) as avg_time max(response_time) as max_time by status
   ```

   **Expected:** Average and max response times grouped by HTTP status code

### Understanding Auto-Extracted Fields

Splunk automatically extracts fields based on the data format. Here's what fields are available in each data source:

**web_access.log (access_combined_wcookie sourcetype):**
- `clientip` - Client IP address
- `method` - HTTP method (GET, POST, etc.)
- `uri` - Requested URL
- `status` - HTTP status code
- `bytes` - Response size in bytes
- `useragent` - User agent string
- `cookie` - HTTP cookie (if present)
- `response_time` - **Custom field (requires field extraction above)**

**application.log, auth.log, sales.log, performance.log (key-value format):**
- All `key=value` pairs are automatically extracted as fields
- Common fields: `host`, `level`, `transaction_id`, `user_id`, `action`, `status`, etc.
- No custom configuration needed - Splunk extracts these automatically

**api.log (_json sourcetype):**
- `timestamp` - ISO 8601 timestamp
- `method` - HTTP method
- `endpoint` - API endpoint path
- `status` - HTTP status code
- `response_time_ms` - Response time in milliseconds
- `user_id` - User identifier
- `ip_address` - Client IP
- `request_id` - Unique request ID

**users.csv (lookup file):**
- Used for data enrichment in future labs
- Fields: `user_id`, `username`, `email`, `department`, `role`, etc.

---

## Lab Challenges

### Challenge 1: Data Distribution
Write a search that shows the event count for each index, sorted by count in descending order.

<details>
<summary>Solution</summary>

```spl
index=* | stats count by index | sort -count
```
</details>

### Challenge 2: Field Extraction Verification
Find the slowest web requests (top 10 by response_time) and display the URL, status code, and response time.

<details>
<summary>Solution</summary>

```spl
index=web | sort -response_time | head 10 | table uri status response_time
```
</details>

### Challenge 3: Lookup Usage
Use the users.csv lookup to enrich web log data and show the top 5 users by request count.

<details>
<summary>Solution</summary>

```spl
index=web | stats count by user | sort -count | head 5
```

Note: The lookup file contains user profile data that can be joined using the `user` field in future labs.
</details>

---

## Verification Checklist

Check that you have completed all setup tasks:

- [ ] Created 6 indexes: web, app, auth, sales, performance, api
- [ ] Uploaded 6 data files with correct sourcetypes
- [ ] Uploaded users.csv lookup file
- [ ] Verified ~350,000 total events ingested
- [ ] Configured response_time field extraction
- [ ] Verified response_time field appears in web index searches
- [ ] All searches complete in reasonable time (<10 seconds)

---

## Troubleshooting

### Data not appearing in searches

1. **Check time range:** Set to "All time" - data has recent timestamps
2. **Check index permissions:** Ensure your role has access to custom indexes
3. **Verify file upload:** Settings → Data Inputs → Uploaded files should show 6 files

### Field extraction not working

1. **Check sourcetype:** Run `index=web | stats count by sourcetype`
   - Should show `access_combined_wcookie`
2. **Check field extraction:** Settings → Fields → Field extractions
   - Should show extraction for `access_combined_wcookie` sourcetype
3. **Refresh:** Try logging out and back in to Splunk

### Lookup file not found

1. **Verify upload:** Settings → Lookups → Lookup table files
   - Should show `users.csv`
2. **Check permissions:** Ensure file has Read permissions for all users
3. **Try re-uploading:** Delete and re-upload if necessary

### File upload errors

- **File too large:** Files should upload fine (largest is 16MB). If you see errors, check Splunk logs: `index=_internal source=*metrics.log`
- **Upload timeout:** Try uploading again - large files may take 1-2 minutes
- **Permission denied:** Ensure data files are accessible and not locked by another program

### Data input status check

- **Settings** → **Data Inputs** → **Files & Directories** should show your 6 uploaded files
- If files don't appear, the upload may have failed - try again

---

## Optional: Field Alias for src_ip

Some labs may reference `src_ip`, but the Apache Combined Log format extracts the IP address as `clientip`.

**Option 1: Use clientip directly (Recommended)**
- Simply use `clientip` in searches instead of `src_ip`
- Example: `index=web | stats count by clientip`

**Option 2: Create a field alias**

If you prefer to use `src_ip`:

1. Go to **Settings** → **Fields** → **Field aliases**
2. Click **New Field Alias**
3. **Destination app:** Search & Reporting
4. **Source type:** `access_combined_wcookie`
5. **Name:** `src_ip_alias`
6. **Field alias:** `src_ip` AS `clientip`
7. Click **Save**

After creating the alias, both `clientip` and `src_ip` will work in searches.

---

## Key Concepts

### Indexes
- Logical data stores in Splunk
- Provide data segregation and access control
- Improve search performance by searching specific indexes
- Default retention: 500MB per index

### Source Types
- Define how Splunk parses and indexes data
- Auto-detection works for common formats (JSON, key-value)
- Custom sourcetypes can be defined for special formats

### Field Extraction
- Extracts fields from raw event data
- Automatic for structured data (JSON, CSV, key-value)
- Custom regex for non-standard fields
- Configured via Web UI or configuration files

### Lookups
- Enrich event data with external reference data
- CSV files uploaded to Splunk
- Joined with events using common fields
- Updated independently of indexed data

---

## Next Steps

Your Splunk environment is now fully configured with:
- 6 indexes containing ~350,000 events
- 1 lookup file with 500 user profiles
- Custom field extraction for response_time

Proceed to **Lab 2: Review of Search Basics** to start working with this data.

---

## Additional Resources

- [Splunk Indexes Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Aboutindexesandindexers)
- [Add Data Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Data/Getstartedwithgettingdatain)
- [Field Extractions](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutfields)
- [Lookups](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutlookupsandfieldactions)
