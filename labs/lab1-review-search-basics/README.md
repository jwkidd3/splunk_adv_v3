# Lab 1: Review of Search Basics

**Duration:** 30 minutes
**Difficulty:** Beginner
**Prerequisites:** Splunk Fundamentals - Level 1

## Lab Objectives

By the end of this lab, you will be able to:
- Use basic search operators and wildcards effectively
- Extract and filter fields in Splunk searches
- Apply the fields, where, and stats commands
- Understand search syntax and best practices
- Navigate the Splunk Search & Reporting interface

## Lab Setup

### Prerequisites
- Splunk Enterprise running and accessible at http://localhost:8000
- Sample data loaded into Splunk
- Access to Search & Reporting app

### Verify Environment
1. Open Splunk Web Interface: http://localhost:8000
2. Navigate to Search & Reporting app
3. Verify you can access the search bar

## Exercises

### Exercise 1: Basic Search Operations (10 minutes)

**Objective:** Practice fundamental search syntax

**Tasks:**

1. **Simple keyword search:**
   ```spl
   error
   ```
   - Observe the results and timeline
   - Note how many events match

2. **Search with wildcards:**
   ```spl
   error*
   ```
   - Compare results with previous search
   - How are they different?

3. **Boolean operators:**
   ```spl
   error OR failed
   ```
   ```spl
   error AND failed
   ```
   ```spl
   error NOT warning
   ```
   - Understand how AND, OR, NOT affect results

4. **Case-sensitive search:**
   ```spl
   ERROR
   ```
   - Note: Splunk searches are case-insensitive by default for keywords

**Expected Outcome:** Understanding of basic search operators and wildcards

---

### Exercise 2: Field Extraction and Filtering (10 minutes)

**Objective:** Work with fields to refine searches

**Tasks:**

1. **Display specific fields:**
   ```spl
   index=main | fields host, source, sourcetype
   ```
   - View only the specified fields

2. **Filter by field values:**
   ```spl
   index=main status=404
   ```
   ```spl
   index=main status>=400 status<500
   ```
   - Understand field-value filtering

3. **Using the where command:**
   ```spl
   index=main | where status=404
   ```
   ```spl
   index=main | where status > 400 AND status < 500
   ```
   - Compare with field=value syntax

4. **Field existence check:**
   ```spl
   index=main | where isnotnull(user_id)
   ```
   - Find events with specific fields present

**Expected Outcome:** Ability to filter and extract fields effectively

---

### Exercise 3: Statistical Commands (10 minutes)

**Objective:** Use stats command for basic aggregations

**Tasks:**

1. **Count events:**
   ```spl
   index=main | stats count
   ```
   - Get total event count

2. **Count by field:**
   ```spl
   index=main | stats count by status
   ```
   - Group events by HTTP status code

3. **Multiple statistics:**
   ```spl
   index=main | stats count, avg(response_time), max(response_time) by host
   ```
   - Calculate multiple metrics

4. **Top values:**
   ```spl
   index=main | top limit=10 user
   ```
   - Find most common users

5. **Rare values:**
   ```spl
   index=main | rare limit=10 source
   ```
   - Find least common sources

**Expected Outcome:** Proficiency with basic statistical commands

---

## Lab Challenges

### Challenge 1: Search Efficiency
Write a search that finds all authentication failures in the last hour, displaying only the username, time, and source IP address.

<details>
<summary>Solution</summary>

```spl
index=main earliest=-1h "authentication failed" OR "login failed"
| fields _time, username, src_ip
| sort -_time
```
</details>

### Challenge 2: Error Analysis
Find all ERROR level events, count them by sourcetype, and display results in descending order.

<details>
<summary>Solution</summary>

```spl
index=main log_level=ERROR OR level=ERROR
| stats count by sourcetype
| sort -count
```
</details>

### Challenge 3: Performance Metrics
Calculate the average, minimum, and maximum response time for web requests, grouped by status code.

<details>
<summary>Solution</summary>

```spl
index=web
| stats avg(response_time) as avg_time, min(response_time) as min_time, max(response_time) as max_time by status
| sort -avg_time
```
</details>

---

## Key Concepts

### Search Processing Language (SPL)
- Splunk uses SPL for all searches
- Commands are connected with pipes (|)
- Search terms filter data, commands process it

### Search Best Practices
1. Be specific with time ranges
2. Use index names when possible
3. Filter early in the search pipeline
4. Avoid leading wildcards (e.g., *error)
5. Use field filtering instead of keyword searches when possible

### Common Commands Review
| Command | Purpose | Example |
|---------|---------|---------|
| fields | Select specific fields | `fields host, source` |
| where | Filter results with boolean logic | `where status=200` |
| stats | Calculate statistics | `stats count by user` |
| top | Find most common values | `top 10 sourcetype` |
| rare | Find least common values | `rare 10 host` |
| sort | Order results | `sort -count` |

---

## Verification

Check your understanding:
- [ ] I can write basic searches with keywords and wildcards
- [ ] I understand boolean operators (AND, OR, NOT)
- [ ] I can use fields command to display specific fields
- [ ] I can filter events using where command
- [ ] I can calculate basic statistics with stats command
- [ ] I understand the difference between search-time and index-time fields

---

## Additional Resources

- [Splunk Search Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference)
- [Search Manual](https://docs.splunk.com/Documentation/Splunk/latest/Search)
- [SPL Quick Reference](https://www.splunk.com/pdfs/solution-guides/splunk-quick-reference-guide.pdf)

---

## Next Steps

Proceed to **Lab 2: Subsearches and Macros** to learn advanced search techniques for building complex search pipelines.
