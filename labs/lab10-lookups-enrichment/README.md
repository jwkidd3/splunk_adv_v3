# Lab 10: Lookups and Data Enrichment

**Duration:** 45 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 8-9 completed

## Lab Objectives

- Create and manage lookup files
- Use lookup command to enrich data
- Implement automatic lookups
- Use inputlookup and outputlookup
- Create CSV and KV store lookups

## Exercises

### Exercise 1: Create CSV Lookup
Create a user lookup file with user details

### Exercise 2: Manual Lookup
```spl
index=web | lookup user_info.csv user_id OUTPUT email, department
```

### Exercise 3: Automatic Lookup Configuration
Configure automatic field enrichment

### Exercise 4: KV Store Lookup
Create and use a KV store collection

## Key Topics
- Lookup file types (CSV, KV store)
- lookup vs inputlookup vs outputlookup
- Automatic lookups
- Lookup performance
- Updating lookup files

---

**Next:** Lab 11 - Machine Learning Toolkit Introduction
