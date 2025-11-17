# Lab 7: Search Optimization

**Duration:** 40 minutes
**Difficulty:** Advanced
**Prerequisites:** Labs 1-6 completed

## Lab Objectives

- Optimize search performance
- Use tstats command for accelerated searches
- Implement summary indexing
- Understand search job inspector
- Apply search best practices

## Exercises

### Exercise 1: Search Job Inspector
Run a search and analyze performance metrics

### Exercise 2: tstats Command
```spl
| tstats count where index=web by host, status
```

### Exercise 3: Optimize Searches
Transform inefficient searches into optimized versions

### Exercise 4: Summary Indexing
Create a summary index for frequently-run searches

## Key Topics
- Search performance metrics
- tstats vs stats
- Data model acceleration
- Summary indexing
- Search optimization techniques

---

**Next:** Day 2 - Lab 8: Eval Command and Data Manipulation
