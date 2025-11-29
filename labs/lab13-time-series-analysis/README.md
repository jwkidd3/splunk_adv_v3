# Lab 12: Time Series Analysis

**Duration:** 40 minutes
**Difficulty:** Advanced
**Prerequisites:** Lab 11 completed

## Lab Objectives

- Perform linear regression analysis
- Implement forecasting with predict command
- Use autoregression for time series
- Analyze trends and seasonality
- Make data-driven predictions

## Exercises

### Exercise 1: Linear Regression
```spl
index=sales | timechart span=1d sum(revenue) as daily_revenue
| fit LinearRegression daily_revenue
```

### Exercise 2: Forecasting with Predict
```spl
index=web | timechart span=1h count
| predict count as predicted_count future_timespan=24
```

### Exercise 3: Trend Analysis
Identify upward/downward trends in metrics

### Exercise 4: Seasonal Decomposition
Analyze seasonal patterns in data

## Key Topics
- Linear regression in Splunk
- predict command
- Trend analysis
- Seasonality detection
- Forecast accuracy

---

**Next:** Lab 13 - User and Role Management
