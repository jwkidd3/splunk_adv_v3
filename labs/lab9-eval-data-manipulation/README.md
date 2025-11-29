# Lab 8: Eval Command and Data Manipulation

**Duration:** 40 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 1-7 completed

## Lab Objectives

By the end of this lab, you will be able to:
- Use the eval command for field calculations
- Perform data type conversions
- Implement conditional logic with if, case, and coalesce
- Create calculated fields for analysis
- Manipulate strings and numbers effectively

## Lab Setup

### Prerequisites
- Splunk Enterprise running and accessible
- Completed Labs 1-7
- Sample web and application data loaded

## Exercises

### Exercise 1: Basic Eval Operations (10 minutes)

**Objective:** Understand eval syntax and basic calculations

**Concept:** The `eval` command creates or redefines fields using expressions.

**Tasks:**

1. **Simple calculations:**
   ```spl
   index=web
   | eval response_time_sec = response_time / 1000
   | table _time, response_time, response_time_sec
   ```
   - Convert milliseconds to seconds

2. **String concatenation:**
   ```spl
   index=main
   | eval full_name = first_name + " " + last_name
   | table first_name, last_name, full_name
   ```
   - Combine multiple fields

3. **Mathematical operations:**
   ```spl
   index=sales
   | eval profit = revenue - cost
   | eval profit_margin = round((profit / revenue) * 100, 2)
   | table product, revenue, cost, profit, profit_margin
   ```
   - Calculate profit and margin

4. **Field comparison:**
   ```spl
   index=web
   | eval is_slow = if(response_time > 1000, "Yes", "No")
   | stats count by is_slow
   ```
   - Categorize events based on conditions

**Expected Outcome:** Proficiency with basic eval expressions

---

### Exercise 2: Conditional Logic (15 minutes)

**Objective:** Implement if, case, and coalesce functions

**Tasks:**

1. **Simple if statement:**
   ```spl
   index=web
   | eval status_category = if(status < 400, "Success", "Error")
   | stats count by status_category
   ```
   - Binary categorization

2. **Nested if statements:**
   ```spl
   index=web
   | eval status_type = if(status < 300, "Success",
                          if(status < 400, "Redirect",
                          if(status < 500, "Client Error", "Server Error")))
   | stats count by status_type
   ```
   - Multi-level categorization

3. **Case statement (cleaner alternative):**
   ```spl
   index=web
   | eval status_category = case(
       status >= 200 AND status < 300, "Success",
       status >= 300 AND status < 400, "Redirect",
       status >= 400 AND status < 500, "Client Error",
       status >= 500, "Server Error",
       1=1, "Unknown"
   )
   | stats count by status_category
   ```
   - Case provides cleaner multi-condition logic

4. **Coalesce for null handling:**
   ```spl
   index=users
   | eval display_name = coalesce(nickname, first_name, user_id)
   | table user_id, nickname, first_name, display_name
   ```
   - Returns first non-null value

5. **Complex business logic:**
   ```spl
   index=sales
   | eval discount = case(
       amount > 10000, 0.15,
       amount > 5000, 0.10,
       amount > 1000, 0.05,
       1=1, 0
   )
   | eval final_amount = amount * (1 - discount)
   | table customer, amount, discount, final_amount
   ```
   - Tiered discount calculation

**Expected Outcome:** Mastery of conditional logic in eval

---

### Exercise 3: Data Type Conversion and String Functions (15 minutes)

**Objective:** Work with different data types and string manipulation

**Tasks:**

1. **Type conversion:**
   ```spl
   index=main
   | eval count_num = tonumber(count_str)
   | eval timestamp = tostring(_time, "%Y-%m-%d %H:%M:%S")
   | table count_str, count_num, _time, timestamp
   ```
   - Convert between types

2. **String functions:**
   ```spl
   index=web
   | eval url_upper = upper(url)
   | eval url_lower = lower(url)
   | eval url_length = len(url)
   | table url, url_upper, url_lower, url_length
   ```
   - Case conversion and length

3. **Substring extraction:**
   ```spl
   index=web
   | eval domain = substr(url, 1, 50)
   | eval first_char = substr(method, 1, 1)
   | table url, domain, method, first_char
   ```
   - Extract portions of strings

4. **Replace and trim:**
   ```spl
   index=main
   | eval cleaned_email = lower(trim(email))
   | eval masked_email = replace(cleaned_email, "(\w+)@", "***@")
   | table email, cleaned_email, masked_email
   ```
   - Clean and mask sensitive data

5. **Split and mvindex:**
   ```spl
   index=web
   | eval url_parts = split(url, "/")
   | eval first_part = mvindex(url_parts, 0)
   | eval second_part = mvindex(url_parts, 1)
   | table url, first_part, second_part
   ```
   - Work with multi-value fields

6. **Date and time functions:**
   ```spl
   index=main
   | eval hour = strftime(_time, "%H")
   | eval day_of_week = strftime(_time, "%A")
   | eval is_weekend = if(day_of_week="Saturday" OR day_of_week="Sunday", 1, 0)
   | stats count by is_weekend
   ```
   - Extract time components

**Expected Outcome:** Proficiency with data transformation functions

---

## Lab Challenges

### Challenge 1: Customer Segmentation
Create a search that segments customers based on their total purchase amount:
- VIP: > $10,000
- Premium: $5,000 - $10,000
- Standard: $1,000 - $5,000
- Basic: < $1,000

Calculate the average order value for each segment.

<details>
<summary>Solution</summary>

```spl
index=sales
| stats sum(amount) as total_spent, avg(amount) as avg_order by customer_id
| eval segment = case(
    total_spent > 10000, "VIP",
    total_spent > 5000, "Premium",
    total_spent > 1000, "Standard",
    1=1, "Basic"
)
| stats avg(avg_order) as average_order_value, count as customer_count by segment
| eval average_order_value = round(average_order_value, 2)
```
</details>

### Challenge 2: Performance SLA Tracker
Create a search that calculates SLA compliance:
- Response time < 200ms: Excellent
- Response time < 500ms: Good
- Response time < 1000ms: Acceptable
- Response time >= 1000ms: Poor

Show the percentage of requests in each category.

<details>
<summary>Solution</summary>

```spl
index=web
| eval sla_category = case(
    response_time < 200, "Excellent",
    response_time < 500, "Good",
    response_time < 1000, "Acceptable",
    1=1, "Poor"
)
| stats count by sla_category
| eventstats sum(count) as total
| eval percentage = round((count / total) * 100, 2)
| fields sla_category, count, percentage
| sort -percentage
```
</details>

### Challenge 3: Email Domain Extraction
Extract the domain from email addresses and find the top 10 domains. Clean the data by converting to lowercase and trimming whitespace.

<details>
<summary>Solution</summary>

```spl
index=users
| eval clean_email = lower(trim(email))
| rex field=clean_email "@(?<domain>[^@]+)$"
| stats count by domain
| sort -count
| head 10
```
</details>

---

## Key Concepts

### Eval Command Syntax
```spl
| eval new_field = expression
| eval field1 = expr1, field2 = expr2  # Multiple evals in one command
```

### Common Eval Functions

#### Mathematical
- `+, -, *, /` - Basic arithmetic
- `%` - Modulo
- `round(value, decimals)` - Round numbers
- `ceil(value)`, `floor(value)` - Rounding functions
- `abs(value)` - Absolute value
- `sqrt(value)`, `pow(base, exp)` - Power functions

#### String Functions
- `upper(str)`, `lower(str)` - Case conversion
- `len(str)` - String length
- `substr(str, start, length)` - Substring extraction
- `trim(str)`, `ltrim(str)`, `rtrim(str)` - Remove whitespace
- `replace(str, pattern, replacement)` - String replacement
- `split(str, delimiter)` - Split into multi-value field
- `urldecode(url)` - Decode URL encoding

#### Conversion Functions
- `tonumber(str)` - Convert to number
- `tostring(value)` - Convert to string
- `tostring(time, format)` - Format time

#### Conditional Functions
- `if(condition, true_value, false_value)` - Simple conditional
- `case(condition1, value1, condition2, value2, ..., default)` - Multiple conditions
- `coalesce(field1, field2, ...)` - First non-null value
- `null()` - Return null value
- `isnull(field)`, `isnotnull(field)` - Null checks

#### Date/Time Functions
- `now()` - Current time
- `time()` - Event time
- `strftime(time, format)` - Format time
- `strptime(str, format)` - Parse time string
- `relative_time(time, offset)` - Time arithmetic

---

## Verification

Check your understanding:
- [ ] I can perform calculations with eval
- [ ] I understand if, case, and coalesce functions
- [ ] I can convert between data types
- [ ] I can manipulate strings effectively
- [ ] I can extract and format date/time components
- [ ] I know when to use eval vs other commands

---

## Best Practices

### Performance Optimization
```spl
# Bad: Eval after stats (inefficient)
index=web | stats count by status | eval is_error = if(status >= 400, 1, 0)

# Good: Filter before aggregation
index=web | eval is_error = if(status >= 400, 1, 0) | stats sum(is_error) as errors, count as total
```

### Code Readability
```spl
# Bad: Hard to read nested ifs
| eval x = if(a > 10, if(b < 5, "Y", "N"), if(c = "X", "Y", "N"))

# Good: Use case for multiple conditions
| eval x = case(
    a > 10 AND b < 5, "Y",
    a <= 10 AND c = "X", "Y",
    1=1, "N"
)
```

---

## Common Pitfalls

### String vs Number Comparison
```spl
# Wrong: Comparing string "10" > "9" returns false
| eval result = if("10" > "9", "yes", "no")

# Correct: Convert to numbers first
| eval result = if(tonumber("10") > tonumber("9"), "yes", "no")
```

### Null Handling
```spl
# Wrong: Null comparisons can cause unexpected results
| eval result = if(field = null(), "empty", "not empty")

# Correct: Use isnull()
| eval result = if(isnull(field), "empty", "not empty")
```

---

## Additional Resources

- [Eval Command Reference](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/Eval)
- [Evaluation Functions](https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/CommonEvalFunctions)
- [Data Type Conversion](https://docs.splunk.com/Documentation/Splunk/latest/Search/Useevalexpressionswithcommonstatisticalfunctions)

---

## Next Steps

Proceed to **Lab 9: Regular Expressions with Rex** to learn advanced field extraction using regex patterns.
