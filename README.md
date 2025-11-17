# Splunk Advanced Course (Level 2)

A comprehensive 2-day intensive Splunk training course covering advanced search techniques, data transformation, analytics, and administration.

**Duration:** 2 days (14 hours total)
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

### 3. Start Your First Lab

1. Access Splunk Web Interface
2. Open Search & Reporting app
3. Open `labs/lab1-review-search-basics/README.md`
4. Follow the instructions and run all searches in Search interface

💡 **All labs are designed to be run in Splunk Web Interface**

---

## Course Structure

### Day 1: Advanced Searching and Reporting (7 hours)
**Labs 1-7:** Advanced search techniques and visualization

| Lab | Title | Key Topics |
|-----|-------|------------|
| **Lab 1** | Review of Search Basics | Search operators, wildcards, field extraction |
| **Lab 2** | Subsearches and Macros | Building complex search pipelines, reusable searches |
| **Lab 3** | Statistical Commands | sum, avg, min, max, count, stats command |
| **Lab 4** | Join Command and Multi-Index Searches | Combining data from multiple indexes |
| **Lab 5** | Time-Based Searches | Analyzing trends and patterns over time |
| **Lab 6** | Custom Dashboards and Visualizations | Creating charts, graphs, and dashboards |
| **Lab 7** | Search Optimization | Performance optimization, filtering, summary indexing |

### Day 2: Data Transformation, Analytics, and Administration (7 hours)
**Labs 8-14:** Data manipulation and system administration

| Lab | Title | Key Topics |
|-----|-------|------------|
| **Lab 8** | Eval Command and Data Manipulation | Calculations, data transformation |
| **Lab 9** | Regular Expressions with Rex | Advanced data parsing, field extraction |
| **Lab 10** | Lookups and Data Enrichment | Enriching data with external information |
| **Lab 11** | Machine Learning Toolkit Introduction | Anomaly detection, clustering, forecasting |
| **Lab 12** | Time Series Analysis | Linear regression, forecasting |
| **Lab 13** | User and Role Management | Authentication, authorization, RBAC |
| **Lab 14** | System Administration and Monitoring | Index optimization, health monitoring, troubleshooting |

---

## Detailed Course Flow

This section shows the exact order of presentations and labs for each day.

### Day 1: Advanced Searching and Reporting (7 hours)

**Morning Session (3.5 hours)**

1. **Presentation 1: Introduction & Search Review** (45 min)
   - File: `presentations/content1_presentation.html`
   - Topics: Course overview, search operators, wildcards, field extraction

2. **Lab 1: Review of Search Basics** (30 min)
   - Directory: `labs/lab1-review-search-basics/`
   - Activities: Practice basic searches, field extraction, filters

3. **Presentation 2: Advanced Search Techniques** (50 min)
   - File: `presentations/content2_presentation.html`
   - Topics: Subsearches, macros, statistical commands

4. **Lab 2: Subsearches and Macros** (45 min)
   - Directory: `labs/lab2-subsearches-macros/`
   - Activities: Build complex search pipelines, create reusable macros

5. **Lab 3: Statistical Commands** (30 min)
   - Directory: `labs/lab3-statistical-commands/`
   - Activities: Use stats, chart, timechart commands

**Break** (15 min)

**Afternoon Session (3.5 hours)**

6. **Lab 4: Join Command and Multi-Index Searches** (45 min)
   - Directory: `labs/lab4-join-multi-index/`
   - Activities: Combine data from multiple sources

7. **Lab 5: Time-Based Searches** (40 min)
   - Directory: `labs/lab5-time-based-searches/`
   - Activities: Analyze trends, create time-based visualizations

8. **Presentation 3: Advanced Reporting and Dashboards** (50 min)
   - File: `presentations/content3_presentation.html`
   - Topics: Dashboard creation, visualization types, drill-downs

9. **Lab 6: Custom Dashboards and Visualizations** (45 min)
   - Directory: `labs/lab6-dashboards-visualizations/`
   - Activities: Create interactive dashboards with various chart types

10. **Lab 7: Search Optimization** (40 min)
    - Directory: `labs/lab7-search-optimization/`
    - Activities: Optimize searches, implement best practices

---

### Day 2: Data Transformation, Analytics, and Administration (7 hours)

**Morning Session (3.5 hours)**

1. **Presentation 4: Data Transformation** (50 min)
   - File: `presentations/content4_presentation.html`
   - Topics: Eval command, field calculations, rex command, regular expressions

2. **Lab 8: Eval Command and Data Manipulation** (40 min)
   - Directory: `labs/lab8-eval-data-manipulation/`
   - Activities: Create calculated fields, transform data

3. **Lab 9: Regular Expressions with Rex** (45 min)
   - Directory: `labs/lab9-regex-rex/`
   - Activities: Extract fields using regex, advanced parsing

4. **Lab 10: Lookups and Data Enrichment** (45 min)
   - Directory: `labs/lab10-lookups-enrichment/`
   - Activities: Create and use lookups, enrich data

**Break** (15 min)

**Afternoon Session (3.5 hours)**

5. **Presentation 5: Analytics and Machine Learning** (45 min)
   - File: `presentations/content5_presentation.html`
   - Topics: ML Toolkit overview, anomaly detection, clustering, forecasting

6. **Lab 11: Machine Learning Toolkit Introduction** (50 min)
   - Directory: `labs/lab11-ml-toolkit-intro/`
   - Activities: Anomaly detection, clustering analysis

7. **Lab 12: Time Series Analysis** (40 min)
   - Directory: `labs/lab12-time-series-analysis/`
   - Activities: Linear regression, forecasting

8. **Presentation 6: Splunk Administration** (40 min)
   - File: `presentations/content6_presentation.html`
   - Topics: User management, authentication, index optimization, monitoring

9. **Lab 13: User and Role Management** (30 min)
   - Directory: `labs/lab13-user-role-management/`
   - Activities: Create users, configure roles, set permissions

10. **Lab 14: System Administration and Monitoring** (35 min)
    - Directory: `labs/lab14-system-admin-monitoring/`
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

### Day 1 Labs
| Lab | Duration | Difficulty | Key Commands |
|-----|----------|------------|--------------|
| Lab 1 | 30 min | Beginner | search, fields, where, stats |
| Lab 2 | 45 min | Intermediate | subsearch, macro, savedsearch |
| Lab 3 | 30 min | Intermediate | stats, chart, timechart |
| Lab 4 | 45 min | Advanced | join, append, union |
| Lab 5 | 40 min | Intermediate | timechart, bucket, predict |
| Lab 6 | 45 min | Intermediate | Dashboard Studio, XML |
| Lab 7 | 40 min | Advanced | tstats, summary indexing |

### Day 2 Labs
| Lab | Duration | Difficulty | Key Commands |
|-----|----------|------------|--------------|
| Lab 8 | 40 min | Intermediate | eval, if, case, coalesce |
| Lab 9 | 45 min | Advanced | rex, regex, sed |
| Lab 10 | 45 min | Intermediate | lookup, inputlookup, outputlookup |
| Lab 11 | 50 min | Advanced | fit, apply, anomalies |
| Lab 12 | 40 min | Advanced | predict, forecast |
| Lab 13 | 30 min | Intermediate | Settings, Users, Roles |
| Lab 14 | 35 min | Advanced | index, monitoring console |

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

### Day 1
- [ ] Complete Lab 1: Search Basics Review
- [ ] Complete Lab 2: Subsearches and Macros
- [ ] Complete Lab 3: Statistical Commands
- [ ] Complete Lab 4: Join and Multi-Index Searches
- [ ] Complete Lab 5: Time-Based Searches
- [ ] Complete Lab 6: Dashboards and Visualizations
- [ ] Complete Lab 7: Search Optimization

### Day 2
- [ ] Complete Lab 8: Eval and Data Manipulation
- [ ] Complete Lab 9: Regular Expressions
- [ ] Complete Lab 10: Lookups and Enrichment
- [ ] Complete Lab 11: ML Toolkit Introduction
- [ ] Complete Lab 12: Time Series Analysis
- [ ] Complete Lab 13: User and Role Management
- [ ] Complete Lab 14: System Administration

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
- 14 hands-on labs with detailed instructions
- 6 Reveal.js presentations
- Sample data sets
- SPL query examples
- Solution guides
- Utility scripts

### Additional Resources
- Splunk Documentation: https://docs.splunk.com
- Splunk Answers: https://community.splunk.com/answers
- Splunk Education: https://education.splunk.com
- Search Reference: https://docs.splunk.com/Documentation/Splunk/latest/SearchReference

---

**Course Version:** 3.0
**Last Updated:** November 2025
**Instructor Support:** Available during course hours
