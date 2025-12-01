# Lab 12: Splunk AI Toolkit Introduction

**Duration:** 50 minutes
**Difficulty:** Advanced
**Prerequisites:** Labs 1-11 completed

## Lab Objectives

- Understand Splunk AI Toolkit capabilities
- Implement anomaly detection
- Perform clustering analysis
- Use forecasting algorithms
- Apply AI/ML algorithms to real data

## Prerequisites

### Installing Splunk AI Toolkit

**Note:** The Splunk AI Toolkit (formerly ML Toolkit) requires a Splunk account to download and install.

1. **Create a Splunk Account** (if you don't have one):
   - Visit https://www.splunk.com
   - Click "Free Splunk" or "Sign Up"
   - Complete registration

2. **Install Splunk AI Toolkit**:
   - In Splunk Web, go to **Apps** → **Find More Apps**
   - Search for "Splunk AI Toolkit"
   - Click **Install**
   - Log in with your Splunk account credentials
   - Accept the terms and complete installation

3. **Install Python for Scientific Computing**:
   - Required for AI Toolkit to function
   - Install from Splunk Apps or follow AI Toolkit setup wizard
   - This provides libraries like scikit-learn, NumPy, pandas

4. **Restart Splunk** after installation

## Exercises

### Exercise 1: Anomaly Detection
```spl
index=web | timechart span=1h avg(response_time) as avg_time
| fit DensityFunction avg_time threshold=0.01
```

### Exercise 2: Clustering
```spl
index=users | fit KMeans user_age user_purchases k=3
```

### Exercise 3: Outlier Detection
Identify unusual patterns in data

### Exercise 4: AI Toolkit Showcase
Explore AI Toolkit examples and built-in assistants

## Key Topics
- AI Toolkit algorithms (regression, classification, clustering)
- Anomaly detection methods
- Clustering techniques
- Model training and application
- AI/ML best practices in Splunk

## Additional Resources
- [Splunk AI Toolkit Documentation](https://docs.splunk.com/Documentation/MLApp)
- Built-in AI Toolkit examples and assistants
- Splunk Machine Learning Showcase app

---

**Next:** Lab 13 - Time Series Analysis
