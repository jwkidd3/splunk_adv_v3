# Lab 5: Time-Based Searches

**Duration:** 40 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 1-4 completed

## Lab Objectives

- Master time modifiers and ranges
- Use timechart for trend analysis
- Implement bucket command for time grouping
- Analyze patterns over time
- Use predict command for forecasting

## Exercises

### Exercise 1: Time Modifiers
```spl
index=web earliest=-24h latest=-1h
```

### Exercise 2: Timechart Analysis
```spl
index=web | timechart span=1h count by status
```

### Exercise 3: Bucket Command
```spl
index=web | bucket _time span=15m | stats count by _time, host
```

### Exercise 4: Trend Analysis
```spl
index=web | timechart span=1d avg(response_time) | predict "avg(response_time)" as predicted
```

## Key Topics
- Time range specifications
- timechart vs bucket
- Trend analysis
- Forecasting with predict

---

**Next:** Lab 6 - Custom Dashboards and Visualizations
