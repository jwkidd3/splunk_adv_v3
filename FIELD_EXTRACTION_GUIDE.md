# Field Extraction Guide

## Overview

This guide explains which data files require custom field extractions and provides step-by-step configuration instructions.

## Data Format Summary

| File | Format | Auto-Extraction | Custom Extraction Needed |
|------|--------|----------------|--------------------------|
| `web_access.log` | Apache Combined + custom | Most fields | **YES** - `response_time` |
| `application.log` | Key-Value | All fields | NO |
| `auth.log` | Key-Value | All fields | NO |
| `sales.log` | Key-Value | All fields | NO |
| `performance.log` | Key-Value | All fields | NO |
| `api.log` | JSON | All fields | NO |
| `users.csv` | CSV Lookup | N/A (lookup file) | NO |

---

## Required Field Extraction

### 1. Extract `response_time` from web_access.log

**Why needed:** The web_access.log file uses Apache Combined Log format with a custom `response_time` field appended at the end (e.g., "150ms"). The standard `access_combined` sourcetype does not extract this custom field.

**Used in labs:**
- Lab 1: Challenge 3 - Performance Metrics (lab1-review-search-basics/README.md:188)
- Lab 3: Statistical Commands
- Lab 7: Search Optimization
- Lab 8: Eval and Data Manipulation

**Sample log line:**
```
192.168.1.100 - user1 [29/Nov/2025:10:30:45 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 150ms
```

#### How to Configure

1. **Navigate to Field Extractions:**
   - Go to **Settings** → **Fields** → **Field extractions**
   - Click **New Field Extraction**

2. **Select Source:**
   - **Destination app:** Search & Reporting
   - **Select source:** Choose existing source type
   - **Source type:** `access_combined`
   - Click **Next**

3. **Sample Event:**
   - Paste a sample event:
     ```
     192.168.1.100 - user1 [29/Nov/2025:10:30:45 +0000] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0" 150ms
     ```
   - Click **Next**

4. **Extract Fields:**
   - **Extraction/Transform:** Regular expression
   - **Regular expression:**
     ```
     \s(?<response_time>\d+)ms$
     ```
   - Click **Preview** to verify extraction
   - You should see `response_time` field with value `150`
   - Click **Next**

5. **Validate:**
   - **Field name:** `response_time`
   - Review and click **Finish**

6. **Verify:**
   - Search: `index=web | stats avg(response_time) by status`
   - You should see numeric response_time values

---

## Optional: Field Alias for src_ip

Some labs reference `src_ip` but Apache Combined Log format extracts the IP address as `clientip`.

**To create a field alias:**

1. Go to **Settings** → **Fields** → **Field aliases**
2. Click **New Field Alias**
3. **Destination app:** Search & Reporting
4. **Source type:** `access_combined`
5. **Name:** `src_ip_alias`
6. **Field alias:** `src_ip` AS `clientip`
7. Click **Save**

**Alternative:** Simply use `clientip` in searches instead of `src_ip`

---

## Auto-Extracted Fields

### web_access.log (access_combined sourcetype)
**Auto-extracted fields:**
- `clientip` - Client IP address
- `method` - HTTP method (GET, POST, etc.)
- `uri` - Requested URL
- `status` - HTTP status code
- `bytes` - Response size in bytes
- `useragent` - User agent string

### application.log, auth.log, sales.log, performance.log (Key-Value format)
**Auto-extracted via Splunk's auto-KV:**
- All key=value pairs automatically extracted
- Examples: host, level, transaction_id, user_id, action, status, etc.

### api.log (JSON format with _json sourcetype)
**Auto-extracted fields:**
- `timestamp` - ISO 8601 timestamp
- `method` - HTTP method
- `endpoint` - API endpoint path
- `status` - HTTP status code
- `response_time_ms` - Response time in milliseconds
- `user_id` - User identifier
- `ip_address` - Client IP
- `request_id` - Unique request ID

---

## Verification Queries

After configuring field extractions, verify with these searches:

### Check response_time extraction:
```spl
index=web
| stats count avg(response_time) as avg_time max(response_time) as max_time min(response_time) as min_time
```

**Expected:** Numeric values for avg_time, max_time, min_time

### Check all web fields:
```spl
index=web
| head 1
| table clientip method uri status bytes useragent response_time
```

**Expected:** All fields populated with values

### Check key-value extractions:
```spl
index=app
| head 1
| table host level transaction_id user_id message
```

**Expected:** All fields populated from application.log

### Check JSON extractions:
```spl
index=api
| head 1
| table method endpoint status response_time_ms user_id ip_address request_id
```

**Expected:** All fields populated from api.log JSON structure

---

## Summary

**Action Required:**
- Configure `response_time` field extraction for `access_combined` sourcetype (web_access.log)

**Optional:**
- Create `src_ip` field alias pointing to `clientip` (or update lab instructions)

**No Action Required:**
- All other data files use formats that Splunk auto-extracts (key-value pairs and JSON)

---

## Additional Resources

- [Splunk Field Extraction Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Extractfieldsfromfileheadersatindextime)
- [Regular Expression Reference](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/AboutSplunkregularexpressions)
- [props.conf Configuration](https://docs.splunk.com/Documentation/Splunk/latest/Admin/Propsconf)
