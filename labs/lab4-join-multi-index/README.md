# Lab 4: Join Command and Multi-Index Searches

**Duration:** 45 minutes
**Difficulty:** Advanced
**Prerequisites:** Labs 1-3 completed

## Lab Objectives

- Use join command to combine data from multiple sources
- Understand join types (inner, left, outer)
- Work with multiple indexes
- Use append and union commands
- Optimize multi-source searches

## Exercises

### Exercise 1: Basic Join
```spl
index=web | join user_id [search index=users | fields user_id, email, name]
```

### Exercise 2: Left Join
```spl
index=web | join type=left user_id [search index=users]
```

### Exercise 3: Append Command
```spl
index=web earliest=-1h | append [search index=app earliest=-1h]
```

## Key Topics
- join vs subsearch vs lookup
- Join performance considerations
- append and union commands
- Multi-index search strategies

---

**Next:** Lab 5 - Time-Based Searches
