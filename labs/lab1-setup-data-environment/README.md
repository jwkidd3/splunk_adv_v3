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

This lab sets up the complete data environment needed for all subsequent labs in this course. You will load ~450,000 events across 6 different data sources and configure one custom field extraction.

**Data Summary:**
- **web_access.log** - 150,000 Apache web server logs (16MB)
- **application.log** - 100,000 application events (9.3MB)
- **auth.log** - 50,000 authentication events (4.4MB)
- **sales.log** - 50,000 sales transactions (6.5MB)
- **performance.log** - 50,000 system metrics (4.5MB)
- **api.log** - 100,000 API requests (12MB)
- **users.csv** - 1,000 user profiles (35KB)

**Total:** ~53MB, ~450,000 events

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
   - Configure as shown in the table below
   - Click **Next**

4. **Input Settings:**
   - **Host:** `course-data`
   - **Index:** Select the appropriate index (see table below)
   - Click **Review**

5. **Submit:**
   - Review the settings
   - Click **Submit**
   - Wait for "File has been uploaded successfully" message

### Data File Configuration:

| File | Index | Source Type | Notes |
|------|-------|-------------|-------|
| `web_access.log` | `web` | `access_combined` | Apache web logs |
| `application.log` | `app` | Auto-detect | Key-value format |
| `auth.log` | `auth` | Auto-detect | Key-value format |
| `sales.log` | `sales` | Auto-detect | Key-value format |
| `performance.log` | `performance` | Auto-detect | Key-value format |
| `api.log` | `api` | `_json` | JSON format |

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
   **Expected:** ~150,000 events

   ```spl
   index=app | stats count
   ```
   **Expected:** ~100,000 events

   ```spl
   index=auth | stats count
   ```
   **Expected:** ~50,000 events

   ```spl
   index=sales | stats count
   ```
   **Expected:** ~50,000 events

   ```spl
   index=performance | stats count
   ```
   **Expected:** ~50,000 events

   ```spl
   index=api | stats count
   ```
   **Expected:** ~100,000 events

3. **Verify lookup file:**

   ```spl
   | inputlookup users.csv | stats count
   ```
   **Expected:** 1,000 users

4. **Check total events:**

   ```spl
   index=* | stats count
   ```
   **Expected:** ~450,000 events (excluding internal Splunk indexes)

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

2. **Select Source:**
   - **Destination app:** Search & Reporting
   - **Step 1:** Select **Sourcetype**
   - **Sourcetype:** `access_combined`
   - Click **Next**

3. **Provide Sample Event:**
   - Paste this sample event:
     ```
     192.168.1.100 - user1 [29/Nov/2025:10:30:45 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 150ms
     ```
   - Click **Next**

4. **Extract Fields:**
   - **Method:** Regular Expression
   - **Regular Expression:**
     ```
     \s(?<response_time>\d+)ms$
     ```
   - Click **Preview**
   - You should see `response_time` highlighted with value `150`
   - Click **Next**

5. **Validate:**
   - **Field Name:** Verify it shows `response_time`
   - **Sample Values:** Should show numeric values
   - Click **Finish**

6. **Verify the extraction:**

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
- [ ] Verified ~450,000 total events ingested
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
   - Should show `access_combined`
2. **Check field extraction:** Settings → Fields → Field extractions
   - Should show extraction for `access_combined` sourcetype
3. **Refresh:** Try logging out and back in to Splunk

### Lookup file not found

1. **Verify upload:** Settings → Lookups → Lookup table files
   - Should show `users.csv`
2. **Check permissions:** Ensure file has Read permissions for all users
3. **Try re-uploading:** Delete and re-upload if necessary

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
- 6 indexes containing ~450,000 events
- 1 lookup file with 1,000 user profiles
- Custom field extraction for response_time

Proceed to **Lab 2: Review of Search Basics** to start working with this data.

---

## Additional Resources

- [Splunk Indexes Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Indexer/Aboutindexesandindexers)
- [Add Data Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Data/Getstartedwithgettingdatain)
- [Field Extractions](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutfields)
- [Lookups](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Aboutlookupsandfieldactions)
