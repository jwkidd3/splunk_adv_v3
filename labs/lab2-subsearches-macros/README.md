# Lab 2: Subsearches and Macros

**Duration:** 45 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lab 1 completed

## Lab Objectives

By the end of this lab, you will be able to:
- Understand and implement subsearches in SPL
- Create and use search macros
- Build complex search pipelines
- Optimize searches using subsearch techniques
- Save and manage reusable search logic

## Lab Setup

### Prerequisites
- Splunk Enterprise running and accessible
- Completed Lab 1
- Access to Settings > Advanced search > Search macros

## Exercises

### Exercise 1: Introduction to Subsearches (15 minutes)

**Objective:** Understand subsearch syntax and use cases

**Concept:** A subsearch is a search within a search that runs first and passes results to the outer search.

**Tasks:**

1. **Basic subsearch:**
   ```spl
   index=web status=200
   [search index=web status=404 | fields src_ip | dedup src_ip]
   ```
   - Finds successful requests from IPs that also had 404 errors
   - Subsearch is enclosed in square brackets []

2. **Subsearch with return command:**
   ```spl
   index=web
   [search index=users premium=true | fields user_id | return 1000 $user_id]
   ```
   - Returns only premium users from web logs
   - return command specifies max results

3. **Format command in subsearch:**
   ```spl
   index=web
   [search index=alerts severity=critical | fields host | format]
   ```
   - format command creates proper field=value pairs

**Expected Outcome:** Understanding of subsearch mechanics and syntax

---

### Exercise 2: Advanced Subsearch Patterns (15 minutes)

**Objective:** Implement complex subsearch scenarios

**Tasks:**

1. **Find related events:**
   ```spl
   index=main
   [search index=main error | head 10 | fields transaction_id]
   | stats count by user, action
   ```
   - Finds all events related to transactions that had errors

2. **Time-based subsearch:**
   ```spl
   index=web
   [search index=web earliest=-1h status>=500 | stats max(_time) as latest_error]
   | where _time > latest_error
   ```
   - Finds events after the last server error

3. **NOT with subsearch:**
   ```spl
   index=web NOT
   [search index=web status=200 | fields session_id]
   ```
   - Finds sessions that never had a successful request

4. **Multiple subsearches:**
   ```spl
   index=main
   [search index=alerts priority=high | fields alert_id]
   OR
   [search index=incidents status=open | fields incident_id]
   ```
   - Combines results from multiple subsearches

**Expected Outcome:** Ability to build complex multi-level searches

---

### Exercise 3: Creating and Using Macros (15 minutes)

**Objective:** Create reusable search macros

**Tasks:**

1. **Create a simple macro:**
   - Go to Settings > Advanced search > Search macros
   - Click "Add new"
   - Name: `get_errors`
   - Definition: `status>=400 status<600`
   - Click Save

2. **Use the macro:**
   ```spl
   index=web `get_errors`
   | stats count by status
   ```
   - Notice backticks (`) around macro name

3. **Create macro with arguments:**
   - Go to Settings > Advanced search > Search macros
   - Click "Add new"
   - Name: `time_range(1)`
   - Definition: `earliest=-$arg1$`
   - Arguments: `hours`
   - Click Save

4. **Use macro with arguments:**
   ```spl
   index=main `time_range(24)`
   | stats count
   ```
   - Passes 24 as argument to macro

5. **Create complex macro:**
   - Name: `top_users(2)`
   - Definition: `| stats count by $arg1$ | sort -count | head $arg2$`
   - Arguments: `field,limit`
   - Save

6. **Use complex macro:**
   ```spl
   index=web `top_users(user_id, 10)`
   ```
   - Finds top 10 users by activity

**Expected Outcome:** Ability to create and use search macros for code reuse

---

## Lab Challenges

### Challenge 1: Anomaly Detection
Create a search using subsearches to find users who logged in from a new location (IP address they haven't used in the past 30 days).

<details>
<summary>Solution</summary>

```spl
index=auth action=login earliest=-1d
NOT [search index=auth action=login earliest=-30d latest=-1d | fields user, src_ip]
| stats count by user, src_ip
| sort -count
```
</details>

### Challenge 2: Macro for Error Tracking
Create a macro called `error_summary(2)` that takes an index name and time range, then returns count of errors by host.

<details>
<summary>Solution</summary>

**Macro Definition:**
- Name: `error_summary(2)`
- Definition: `index=$arg1$ earliest=-$arg2$ (level=ERROR OR status>=500) | stats count by host | sort -count`
- Arguments: `index,timerange`

**Usage:**
```spl
`error_summary(web, 1h)`
```
</details>

### Challenge 3: Complex Pipeline
Build a search that finds the top 10 most active users, then use that result in a subsearch to analyze their error rates.

<details>
<summary>Solution</summary>

```spl
index=web user_id IN
[search index=web earliest=-24h | stats count by user_id | sort -count | head 10 | fields user_id]
| eval is_error=if(status>=400, 1, 0)
| stats count as total, sum(is_error) as errors by user_id
| eval error_rate=round((errors/total)*100, 2)
| sort -error_rate
```
</details>

---

## Key Concepts

### Subsearch Fundamentals
- Subsearches run **first** before the outer search
- Enclosed in square brackets `[ ]`
- Results passed to outer search as field-value pairs
- Default limit: 10,000 results
- Default time limit: 60 seconds

### Subsearch Best Practices
1. Keep subsearches focused and filtered
2. Use `fields` command to limit returned fields
3. Use `dedup` to reduce duplicate results
4. Consider using `return` to specify format
5. Avoid nested subsearches (max 2 levels)
6. For large result sets, consider using join or lookup instead

### Macro Advantages
- **Reusability:** Write once, use many times
- **Maintainability:** Update in one place
- **Consistency:** Same logic across searches
- **Simplification:** Hide complex logic behind simple names
- **Parameterization:** Pass dynamic values as arguments

### When to Use What

| Scenario | Recommended Approach |
|----------|---------------------|
| Filter by dynamic list | Subsearch |
| Reusable search logic | Macro |
| Combining different indexes | Subsearch or join |
| Standard time ranges | Macro |
| Complex field calculations | Macro |
| Large result sets (>10K) | Join or lookup instead |

---

## Verification

Check your understanding:
- [ ] I can write and execute subsearches
- [ ] I understand subsearch execution order
- [ ] I can create search macros via Settings
- [ ] I can create macros with arguments
- [ ] I know when to use subsearches vs joins vs lookups
- [ ] I can combine subsearches with macros

---

## Common Pitfalls

### Subsearch Limitations
```spl
# Bad: Too broad, returns too many results
index=web [search index=main]

# Good: Specific and filtered
index=web [search index=main error | fields user | dedup user | head 100]
```

### Macro Syntax Errors
```spl
# Wrong: Using single quotes
index=web 'get_errors'

# Correct: Using backticks
index=web `get_errors`
```

---

## Additional Resources

- [Subsearch Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Search/Aboutsubsearches)
- [Search Macro Documentation](https://docs.splunk.com/Documentation/Splunk/latest/Knowledge/Definesearchmacros)
- [Subsearch Best Practices](https://docs.splunk.com/Documentation/Splunk/latest/Search/Writesubsearches)

---

## Next Steps

Proceed to **Lab 3: Statistical Commands** to master data aggregation and analysis.
