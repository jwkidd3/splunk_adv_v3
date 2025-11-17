#!/usr/bin/env python3
"""
Labs 4-14: Comprehensive Test Suite
Tests all operations from Labs 4 through 14
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.test_base import LabTestBase


class Lab04Tests(LabTestBase):
    """Tests for Lab 4: Join Command and Multi-Index Searches"""

    def __init__(self, client):
        super().__init__(client, 4, "Join Command and Multi-Index Searches")

    def run_all_tests(self):
        # Test 1: Basic join
        result = self.run_query_test(
            test_name="Basic join operation",
            query="index=web | join type=inner user [search index=auth action=login | fields user, src_ip] | head 10",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Left join
        result = self.run_query_test(
            test_name="Left join operation",
            query="index=web | join type=left user [search index=auth | fields user, action] | head 10",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Append command
        result = self.run_query_test(
            test_name="Append command",
            query="index=web earliest=-1h | append [search index=app earliest=-1h] | head 20",
            expected_min_results=1,
            earliest_time="-1h"
        )
        self.add_result(result)

        # Test 4: Union command (alternative syntax)
        result = self.run_query_test(
            test_name="Multi-index search",
            query="(index=web OR index=app) earliest=-1h | stats count by index",
            expected_min_results=1,
            earliest_time="-1h"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab05Tests(LabTestBase):
    """Tests for Lab 5: Time-Based Searches"""

    def __init__(self, client):
        super().__init__(client, 5, "Time-Based Searches")

    def run_all_tests(self):
        # Test 1: Time modifiers
        result = self.run_query_test(
            test_name="Time range with earliest/latest",
            query="index=web earliest=-24h latest=-1h | stats count",
            expected_min_results=1,
            earliest_time="-24h",
            latest_time="-1h"
        )
        self.add_result(result)

        # Test 2: Timechart
        result = self.run_query_test(
            test_name="Timechart with span",
            query="index=web | timechart span=1h count by status",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Bucket command
        result = self.run_query_test(
            test_name="Bucket command for time grouping",
            query="index=web | bucket _time span=15m | stats count by _time, host | head 20",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 4: Trend analysis with predict
        result = self.run_query_test(
            test_name="Timechart for prediction",
            query='index=web | timechart span=1d count as daily_count',
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab06Tests(LabTestBase):
    """Tests for Lab 6: Custom Dashboards and Visualizations"""

    def __init__(self, client):
        super().__init__(client, 6, "Custom Dashboards and Visualizations")

    def run_all_tests(self):
        # Test 1: Data for line chart
        result = self.run_query_test(
            test_name="Line chart data (timechart)",
            query="index=web | timechart span=1h avg(response_time) as avg_response",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 2: Data for bar chart
        result = self.run_query_test(
            test_name="Bar chart data (stats by category)",
            query="index=web | stats count by status | sort -count",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Data for pie chart
        result = self.run_query_test(
            test_name="Pie chart data (distribution)",
            query="index=web | stats count by host",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 4: Single value KPI
        result = self.run_query_test(
            test_name="Single value KPI",
            query="index=web | stats avg(response_time) as avg_response_time",
            expected_min_results=1,
            earliest_time="-24h"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab07Tests(LabTestBase):
    """Tests for Lab 7: Search Optimization"""

    def __init__(self, client):
        super().__init__(client, 7, "Search Optimization")

    def run_all_tests(self):
        # Test 1: Optimized search with index filter
        result = self.run_query_test(
            test_name="Optimized search (specific index and time)",
            query="index=web earliest=-1h sourcetype=* status>=500 | stats count by host",
            expected_min_results=0,
            earliest_time="-1h"
        )
        self.add_result(result)

        # Test 2: Fields command for performance
        result = self.run_query_test(
            test_name="Early field extraction",
            query="index=web | fields status, response_time, host | stats avg(response_time) by status",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Stats vs transaction performance
        result = self.run_query_test(
            test_name="Stats-based aggregation",
            query="index=web | stats count, values(status) as statuses by src_ip | head 100",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab08Tests(LabTestBase):
    """Tests for Lab 8: Eval Command and Data Manipulation"""

    def __init__(self, client):
        super().__init__(client, 8, "Eval Command and Data Manipulation")

    def run_all_tests(self):
        # Test 1: Basic eval calculations
        result = self.run_query_test(
            test_name="Eval basic calculation",
            query="index=web | eval response_time_sec = response_time / 1000 | head 10",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 2: If statement
        result = self.run_query_test(
            test_name="Eval if statement",
            query="index=web | eval status_category = if(status < 400, \"Success\", \"Error\") | stats count by status_category",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Case statement
        result = self.run_query_test(
            test_name="Eval case statement",
            query='index=web | eval status_type = case(status >= 200 AND status < 300, "Success", status >= 300 AND status < 400, "Redirect", status >= 400 AND status < 500, "Client Error", status >= 500, "Server Error", 1=1, "Unknown") | stats count by status_type',
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 4: Coalesce function
        result = self.run_query_test(
            test_name="Eval coalesce",
            query="index=web | eval user_field = coalesce(user, \"anonymous\") | stats count by user_field",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 5: String functions
        result = self.run_query_test(
            test_name="Eval string functions",
            query="index=web | eval url_length = len(url), url_upper = upper(url) | head 10",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 6: Date/time functions
        result = self.run_query_test(
            test_name="Eval date/time functions",
            query='index=web | eval hour = strftime(_time, "%H"), day_of_week = strftime(_time, "%A") | stats count by hour',
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab09Tests(LabTestBase):
    """Tests for Lab 9: Regular Expressions with Rex"""

    def __init__(self, client):
        super().__init__(client, 9, "Regular Expressions with Rex")

    def run_all_tests(self):
        # Test 1: Basic rex extraction
        result = self.run_query_test(
            test_name="Rex basic field extraction",
            query='index=web | rex field=url "/(?<endpoint>[^/]+)$" | stats count by endpoint | head 10',
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 2: Multiple field extraction
        result = self.run_query_test(
            test_name="Rex multiple fields",
            query='index=app | rex "user=(?<username>\\w+).*level=(?<log_level>\\w+)" | stats count by log_level | head 10',
            expected_min_results=0,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Rex with named groups
        result = self.run_query_test(
            test_name="Rex named capture groups",
            query='index=web | rex field=_raw "(?<ip_addr>\\d+\\.\\d+\\.\\d+\\.\\d+)" | stats dc(ip_addr) as unique_ips',
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab10Tests(LabTestBase):
    """Tests for Lab 10: Lookups and Data Enrichment"""

    def __init__(self, client):
        super().__init__(client, 10, "Lookups and Data Enrichment")

    def run_all_tests(self):
        # Test 1: Inputlookup
        result = self.run_query_test(
            test_name="Inputlookup users.csv",
            query="| inputlookup users.csv | head 10",
            expected_min_results=1
        )
        self.add_result(result)

        # Test 2: Lookup command (manual)
        result = self.run_query_test(
            test_name="Lookup enrichment",
            query="index=web | lookup users.csv user_id OUTPUT email, department | head 10",
            expected_min_results=0,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Stats with lookup data
        result = self.run_query_test(
            test_name="Stats with lookup fields",
            query="index=web | lookup users.csv user_id OUTPUT department | stats count by department",
            expected_min_results=0,
            earliest_time="-7d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab11Tests(LabTestBase):
    """Tests for Lab 11: Machine Learning Toolkit Introduction"""

    def __init__(self, client):
        super().__init__(client, 11, "Machine Learning Toolkit Introduction")

    def run_all_tests(self):
        # Note: ML Toolkit tests require MLTK to be installed

        # Test 1: Data preparation for ML
        result = self.run_query_test(
            test_name="Prepare data for ML (timechart)",
            query="index=web | timechart span=1h avg(response_time) as avg_time",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Statistical baseline
        result = self.run_query_test(
            test_name="Statistical baseline calculation",
            query="index=web | stats avg(response_time) as avg_response, stdev(response_time) as stdev_response by host",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab12Tests(LabTestBase):
    """Tests for Lab 12: Time Series Analysis"""

    def __init__(self, client):
        super().__init__(client, 12, "Time Series Analysis")

    def run_all_tests(self):
        # Test 1: Time series data preparation
        result = self.run_query_test(
            test_name="Time series data (daily aggregation)",
            query="index=sales | timechart span=1d sum(final_amount) as daily_revenue",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Trend calculation
        result = self.run_query_test(
            test_name="Trend analysis with trendline",
            query="index=sales | timechart span=1d sum(final_amount) as revenue | trendline sma3(revenue) as trend",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab13Tests(LabTestBase):
    """Tests for Lab 13: User and Role Management"""

    def __init__(self, client):
        super().__init__(client, 13, "User and Role Management")

    def run_all_tests(self):
        # Test 1: Check internal logs for user activity
        result = self.run_query_test(
            test_name="User activity in internal logs",
            query='index=_audit action=login | stats count by user | head 10',
            expected_min_results=0,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 2: Search activity
        result = self.run_query_test(
            test_name="Search activity audit",
            query='index=_audit action=search | stats count by user | head 10',
            expected_min_results=0,
            earliest_time="-7d"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()


class Lab14Tests(LabTestBase):
    """Tests for Lab 14: System Administration and Monitoring"""

    def __init__(self, client):
        super().__init__(client, 14, "System Administration and Monitoring")

    def run_all_tests(self):
        # Test 1: Index statistics
        result = self.run_query_test(
            test_name="Index event counts",
            query="index=* | stats count by index",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 2: Sourcetype distribution
        result = self.run_query_test(
            test_name="Sourcetype distribution",
            query="index=* | stats count by sourcetype | sort -count",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Internal metrics
        result = self.run_query_test(
            test_name="Splunk internal metrics",
            query='index=_internal source=*metrics.log | stats count by source',
            expected_min_results=0,
            earliest_time="-1h"
        )
        self.add_result(result)

        # Test 4: License usage
        result = self.run_query_test(
            test_name="License usage check",
            query='index=_internal source=*license_usage.log | stats sum(b) as bytes_indexed by idx',
            expected_min_results=0,
            earliest_time="-24h"
        )
        self.add_result(result)

        self.print_summary()
        return self.get_summary()
