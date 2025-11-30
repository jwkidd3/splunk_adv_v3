# Splunk Advanced Course (Level 2)

A comprehensive intensive Splunk training course covering advanced search techniques, data transformation, analytics, and administration.

**Format:** 30% theory, 70% hands-on labs
**Prerequisites:** Splunk Fundamentals - Level 1 or equivalent practical experience
**Platform:** Splunk Enterprise

## Table of Contents

- [Quick Start](#quick-start)
- [Course Structure](#course-structure)
- [Detailed Course Flow](#detailed-course-flow)
- [Prerequisites & Installation](#prerequisites--installation)
- [Running Labs](#running-labs)
- [Lab Quick Reference](#lab-quick-reference)
- [Key Concepts](#key-concepts-covered)
- [Troubleshooting](#troubleshooting)
- [Course Completion](#course-completion-checklist)

---

## Quick Start

### 1. Start Splunk Environment

**Windows:**
```cmd
cd scripts
start-splunk.bat
```

**Stop Splunk:**
```cmd
cd scripts
stop-splunk.bat
```

📖 **See `scripts/README.md` for detailed Splunk server management**

### 2. Access Splunk Web Interface

1. Open browser to http://localhost:8000
2. Login with credentials provided by instructor
3. Navigate to Search & Reporting app

### 3. Complete Lab 1: Setup Data Environment

1. Access Splunk Web Interface
2. Open `labs/lab1-setup-data-environment/README.md`
3. Create indexes and load all course data (~30 minutes)
4. Configure field extractions

💡 **Lab 1 must be completed before starting any other labs**

### 4. Continue with Remaining Labs

After completing Lab 1, proceed with labs 2-15 in order. All labs are designed to be run in the Splunk Web Interface.

---

## Course Structure

### Setup
**Lab 1:** Environment setup and data loading (required first)

| Lab | Title | Key Topics |
|-----|-------|------------|
| **Lab 1** | Setup Data Environment | Create indexes, load data, configure field extractions |

### Part 1: Advanced Searching and Reporting
**Labs 2-8:** Advanced search techniques and visualization

| Lab | Title | Key Topics |
|-----|-------|------------|
| **Lab 2** | Review of Search Basics | Search operators, wildcards, field extraction |
| **Lab 3** | Subsearches and Macros | Building complex search pipelines, reusable searches |
| **Lab 4** | Statistical Commands | sum, avg, min, max, count, stats command |
| **Lab 5** | Join Command and Multi-Index Searches | Combining data from multiple indexes |
| **Lab 6** | Time-Based Searches | Analyzing trends and patterns over time |
| **Lab 7** | Custom Dashboards and Visualizations | Creating charts, graphs, and dashboards |
| **Lab 8** | Search Optimization | Performance optimization, filtering, summary indexing |

### Part 2: Data Transformation, Analytics, and Administration
**Labs 9-15:** Data manipulation and system administration

| Lab | Title | Key Topics |
|-----|-------|------------|
| **Lab 9** | Eval Command and Data Manipulation | Calculations, data transformation |
| **Lab 10** | Regular Expressions with Rex | Advanced data parsing, field extraction |
| **Lab 11** | Lookups and Data Enrichment | Enriching data with external information |
| **Lab 12** | Machine Learning Toolkit Introduction | Anomaly detection, clustering, forecasting |
| **Lab 13** | Time Series Analysis | Linear regression, forecasting |
| **Lab 14** | User and Role Management | Authentication, authorization, RBAC |
| **Lab 15** | System Administration and Monitoring | Index optimization, health monitoring, troubleshooting |

---

## Detailed Course Flow

This section shows the exact order of presentations and labs throughout the course.

### Part 1: Advanced Searching and Reporting

**Session 1: Introduction & Search Basics**

1. **Presentation 1: Introduction & Search Review**
   - File: `presentations/content1_presentation.html`
   - Topics: Course overview, data environment setup, search operators, wildcards, field extraction, best practices

2. **Lab 1: Setup Data Environment** (30 min)
   - Directory: `labs/lab1-setup-data-environment/`
   - Activities: Create indexes, load ~350,000 events, configure field extractions
   - **MUST BE COMPLETED FIRST - Required for all subsequent labs**

3. **Lab 2: Review of Search Basics** (30 min)
   - Directory: `labs/lab2-review-search-basics/`
   - Activities: Practice basic searches, field extraction, filters

---

**Session 2: Advanced Search Techniques**

4. **Presentation 2: Subsearches, Macros & Statistical Commands**
   - File: `presentations/content2_presentation.html`
   - Topics: Subsearch syntax and patterns, creating reusable macros, stats/chart/timechart commands

5. **Lab 3: Subsearches and Macros** (45 min)
   - Directory: `labs/lab3-subsearches-macros/`
   - Activities: Build complex search pipelines, create reusable macros

6. **Lab 4: Statistical Commands** (30 min)
   - Directory: `labs/lab4-statistical-commands/`
   - Activities: Use stats, chart, timechart commands for analysis

---

**Session 3: Data Correlation & Time Analysis**

7. **Presentation 3: Join Command, Multi-Index Searches & Time-Based Analysis**
   - File: `presentations/content3_presentation.html`
   - Topics: Join/append/union commands, multi-index strategies, time-based analysis, trend detection

8. **Lab 5: Join Command and Multi-Index Searches** (45 min)
   - Directory: `labs/lab5-join-multi-index/`
   - Activities: Combine data from multiple sources, perform correlations

9. **Lab 6: Time-Based Searches** (40 min)
   - Directory: `labs/lab6-time-based-searches/`
   - Activities: Analyze trends, create time-based visualizations

---

**Session 4: Visualization & Optimization**

10. **Presentation 4: Dashboards, Visualizations & Search Optimization**
    - File: `presentations/content4_presentation.html`
    - Topics: Dashboard Studio, visualization types, drilldowns, tstats, summary indexing, performance tuning

11. **Lab 7: Custom Dashboards and Visualizations** (45 min)
    - Directory: `labs/lab7-dashboards-visualizations/`
    - Activities: Create interactive dashboards with various chart types

12. **Lab 8: Search Optimization** (40 min)
    - Directory: `labs/lab8-search-optimization/`
    - Activities: Optimize searches, implement best practices, use tstats

---

### Part 2: Data Transformation, Analytics, and Administration

**Session 5: Data Transformation**

13. **Presentation 5: Data Transformation with Eval, Rex & Lookups**
    - File: `presentations/content5_presentation.html`
    - Topics: Eval functions, conditional logic, regular expressions, rex/sed commands, lookup types, data enrichment

14. **Lab 9: Eval Command and Data Manipulation** (40 min)
    - Directory: `labs/lab9-eval-data-manipulation/`
    - Activities: Create calculated fields, transform data, implement conditional logic

15. **Lab 10: Regular Expressions with Rex** (45 min)
    - Directory: `labs/lab10-regex-rex/`
    - Activities: Extract fields using regex, advanced parsing techniques

16. **Lab 11: Lookups and Data Enrichment** (45 min)
    - Directory: `labs/lab11-lookups-enrichment/`
    - Activities: Create and use lookups, enrich data with external information

---

**Session 6: Machine Learning & Administration**

17. **Presentation 6: Machine Learning, Analytics & System Administration**
    - File: `presentations/content6_presentation.html`
    - Topics: ML Toolkit algorithms, anomaly detection, clustering, forecasting, user management, authentication, index optimization, monitoring

18. **Lab 12: Machine Learning Toolkit Introduction** (50 min)
    - Directory: `labs/lab12-ml-toolkit-intro/`
    - Activities: Anomaly detection, clustering analysis, pattern recognition

19. **Lab 13: Time Series Analysis** (40 min)
    - Directory: `labs/lab13-time-series-analysis/`
    - Activities: Linear regression, forecasting, trend prediction

20. **Lab 14: User and Role Management** (30 min)
    - Directory: `labs/lab14-user-role-management/`
    - Activities: Create users, configure roles, set permissions, implement RBAC

21. **Lab 15: System Administration and Monitoring** (35 min)
    - Directory: `labs/lab15-system-admin-monitoring/`
    - Activities: Monitor Splunk health, optimize indexes, troubleshoot issues

---

## Prerequisites & Installation

### Required Knowledge
- Splunk Fundamentals - Level 1 or equivalent
- Basic understanding of log files and data formats
- Familiarity with search concepts
- Basic regular expression knowledge (helpful but not required)

### Software Requirements
- Splunk Enterprise (version 9.x or higher)
- Web browser (Chrome, Firefox, or Safari recommended)
- Text editor (VS Code, Notepad++, or similar)
- Minimum 8GB RAM, 20GB free disk space

### Installation

**Windows:**
```cmd
# Scripts provided in scripts/ folder
cd scripts
start-splunk.bat
```

**Mac/Linux:**
```bash
# Follow Splunk installation guide
# Or use Docker:
docker run -d -p 8000:8000 -p 8088:8088 --name splunk splunk/splunk:latest
```

📖 **Detailed installation instructions in `scripts/README.md`**

---

## Running Labs

### Lab Structure
Each lab contains:
- **README.md** - Lab instructions and objectives
- **sample_searches.spl** - Example SPL queries
- **data/** - Sample data files (if applicable)
- **solutions/** - Solution guides

### How to Run a Lab

1. **Navigate to Lab Directory**
   ```bash
   cd labs/lab1-review-search-basics
   ```

2. **Read README.md**
   - Open `README.md` in text editor or browser
   - Review objectives and prerequisites

3. **Execute Searches**
   - Copy searches from README or sample_searches.spl
   - Paste into Splunk Search & Reporting app
   - Run and analyze results

4. **Complete Exercises**
   - Follow step-by-step instructions
   - Complete all exercises
   - Check solutions if needed

---

## Lab Quick Reference

| Lab | Duration | Difficulty | Key Commands |
|-----|----------|------------|--------------|
| Lab 1 | 30 min | Beginner | Settings, Add Data, Field Extractions |
| Lab 2 | 30 min | Beginner | search, fields, where, stats |
| Lab 3 | 45 min | Intermediate | subsearch, macro, savedsearch |
| Lab 4 | 30 min | Intermediate | stats, chart, timechart |
| Lab 5 | 45 min | Advanced | join, append, union |
| Lab 6 | 40 min | Intermediate | timechart, bucket, predict |
| Lab 7 | 45 min | Intermediate | Dashboard Studio, XML |
| Lab 8 | 40 min | Advanced | tstats, summary indexing |
| Lab 9 | 40 min | Intermediate | eval, if, case, coalesce |
| Lab 10 | 45 min | Advanced | rex, regex, sed |
| Lab 11 | 45 min | Intermediate | lookup, inputlookup, outputlookup |
| Lab 12 | 50 min | Advanced | fit, apply, anomalies |
| Lab 13 | 40 min | Advanced | predict, forecast |
| Lab 14 | 30 min | Intermediate | Settings, Users, Roles |
| Lab 15 | 35 min | Advanced | index, monitoring console |

---

## Key Concepts Covered

### Advanced Search Techniques
- Subsearches and search pipeline optimization
- Macros for reusable search logic
- Statistical functions and aggregations
- Multi-index searches and joins
- Time-based analysis and trending

### Data Transformation
- Field calculations with eval
- Regular expression field extraction
- Data type conversions
- Conditional logic and case statements

### Analytics & Machine Learning
- Anomaly detection algorithms
- Clustering and pattern recognition
- Time series forecasting
- Linear regression analysis

### Administration
- User and role-based access control
- Authentication methods (LDAP, SAML)
- Index lifecycle management
- Performance monitoring and tuning
- System health checks
- Troubleshooting methodologies

### Visualization & Reporting
- Dashboard design principles
- Chart types and best practices
- Drill-down capabilities
- Scheduled reports
- Alert configuration

---

## Troubleshooting

### Common Issues

**Splunk Won't Start**
```bash
# Check if Splunk is already running
ps aux | grep splunk

# Check Splunk logs
tail -f $SPLUNK_HOME/var/log/splunk/splunkd.log
```

**Search Performance Issues**
- Use time range filters
- Filter early in search pipeline
- Avoid wildcards at beginning of search terms
- Use summary indexing for frequently-run searches
- Leverage data models and accelerated searches

**Connection Issues**
- Verify Splunk is running: `./splunk status`
- Check firewall settings
- Verify port 8000 is not blocked
- Clear browser cache

**Lab Data Not Available**
```bash
# Reload sample data
cd scripts
./load-sample-data.bat  # Windows
bash load-sample-data.sh  # Mac/Linux
```

### Getting Help
- Check `scripts/README.md` for environment setup
- Review lab solutions in `solutions/` folder
- Consult Splunk documentation: https://docs.splunk.com
- Use Splunk Community: https://community.splunk.com

---

## Course Completion Checklist

### Labs
- [ ] Complete Lab 1: Setup Data Environment (REQUIRED FIRST)
- [ ] Complete Lab 2: Search Basics Review
- [ ] Complete Lab 3: Subsearches and Macros
- [ ] Complete Lab 4: Statistical Commands
- [ ] Complete Lab 5: Join and Multi-Index Searches
- [ ] Complete Lab 6: Time-Based Searches
- [ ] Complete Lab 7: Dashboards and Visualizations
- [ ] Complete Lab 8: Search Optimization
- [ ] Complete Lab 9: Eval and Data Manipulation
- [ ] Complete Lab 10: Regular Expressions
- [ ] Complete Lab 11: Lookups and Enrichment
- [ ] Complete Lab 12: ML Toolkit Introduction
- [ ] Complete Lab 13: Time Series Analysis
- [ ] Complete Lab 14: User and Role Management
- [ ] Complete Lab 15: System Administration

### Knowledge Validation
- [ ] Can build complex search pipelines using subsearches
- [ ] Understand statistical commands and aggregations
- [ ] Can create interactive dashboards
- [ ] Proficient with eval and rex commands
- [ ] Can implement lookups for data enrichment
- [ ] Understand ML Toolkit capabilities
- [ ] Can manage users and configure security
- [ ] Know how to monitor and optimize Splunk

---

## Next Steps

After completing this course, consider:
- **Splunk Enterprise Security (ES)** - Security operations
- **Splunk IT Service Intelligence (ITSI)** - IT monitoring
- **Splunk Architect Course** - System design and scaling
- **Splunk Certified Power User** - Certification exam
- **Splunk Certified Admin** - Administration certification

---

## Course Materials

### Included in This Repository
- 15 hands-on labs with detailed instructions (including data setup lab)
- 6 comprehensive Reveal.js presentations (one for each session)
- Pre-generated sample data sets (~350,000 events, ~53MB)
- SPL query examples
- Solution guides
- Utility scripts for Splunk management

### Additional Resources
- Splunk Documentation: https://docs.splunk.com
- Splunk Answers: https://community.splunk.com/answers
- Splunk Education: https://education.splunk.com
- Search Reference: https://docs.splunk.com/Documentation/Splunk/latest/SearchReference

---

**Course Version:** 3.0
**Last Updated:** November 2025
**Instructor Support:** Available during course hours
