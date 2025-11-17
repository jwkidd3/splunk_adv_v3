# Lab 9: Regular Expressions with Rex

**Duration:** 45 minutes
**Difficulty:** Advanced
**Prerequisites:** Lab 8 completed

## Lab Objectives

- Master rex command for field extraction
- Write effective regular expressions
- Use sed command for field transformation
- Extract complex patterns from unstructured data
- Test and debug regex patterns

## Exercises

### Exercise 1: Basic Rex
```spl
index=web | rex field=url "\/api\/(?<endpoint>[^\/]+)"
```

### Exercise 2: Multiple Field Extraction
```spl
index=main | rex "(?<ip>\d+\.\d+\.\d+\.\d+).*user=(?<user>\w+)"
```

### Exercise 3: Named Capture Groups
Extract multiple fields from log messages

### Exercise 4: Rex vs Regex Command
Understand differences and use cases

## Key Topics
- Regular expression syntax
- rex command modes
- Named capture groups
- sed for field transformation
- Regex testing and debugging

---

**Next:** Lab 10 - Lookups and Data Enrichment
