# Lab 3: Statistical Commands

**Duration:** 30 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 1-2 completed

## Lab Objectives

- Master stats, chart, and timechart commands
- Calculate aggregations (sum, avg, min, max, count)
- Create statistical visualizations
- Use eval with statistical functions

## Exercises

### Exercise 1: Stats Command Mastery
```spl
index=web | stats count, avg(response_time), max(response_time), min(response_time) by status
```

### Exercise 2: Chart Command
```spl
index=web | chart count over host by status
```

### Exercise 3: Timechart Command
```spl
index=web | timechart span=1h avg(response_time) by status
```

## Key Topics
- stats vs chart vs timechart
- Aggregation functions
- Grouping with by clause
- Time-based aggregations

---

**Next:** Lab 4 - Join Command and Multi-Index Searches
