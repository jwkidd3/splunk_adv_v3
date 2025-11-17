#!/usr/bin/env python3
"""
Lab 3: Statistical Commands - Test Suite
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.test_base import LabTestBase


class Lab03Tests(LabTestBase):
    """Tests for Lab 3: Statistical Commands"""

    def __init__(self, client):
        super().__init__(client, 3, "Statistical Commands")

    def test_stats_command(self):
        """Test stats command variations"""

        # Test 1: Basic stats with aggregations
        result = self.run_query_test(
            test_name="Stats with multiple aggregations",
            query="index=web | stats count, avg(response_time) as avg_time, max(response_time) as max_time, min(response_time) as min_time by status",
            expected_min_results=1,
            required_fields=["count", "status"],
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Stats with eval
        result = self.run_query_test(
            test_name="Stats with eval calculations",
            query="index=web | stats sum(bytes) as total_bytes by host | eval total_mb = round(total_bytes/1024/1024, 2)",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Distinct count
        result = self.run_query_test(
            test_name="Stats with distinct count (dc)",
            query="index=web | stats dc(user) as unique_users, count as total_requests by host",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 4: Values and list
        result = self.run_query_test(
            test_name="Stats with values() function",
            query="index=web | stats values(status) as status_codes, count by host",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_chart_command(self):
        """Test chart command"""

        # Test 1: Basic chart
        result = self.run_query_test(
            test_name="Chart count over host by status",
            query="index=web | chart count over host by status",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Chart with limit
        result = self.run_query_test(
            test_name="Chart with useother and limit",
            query="index=web | chart count over status by host limit=5",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_timechart_command(self):
        """Test timechart command"""

        # Test 1: Basic timechart
        result = self.run_query_test(
            test_name="Timechart span=1h avg response time",
            query="index=web | timechart span=1h avg(response_time) as avg_time",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 2: Timechart with by clause
        result = self.run_query_test(
            test_name="Timechart count by status",
            query="index=web | timechart span=1h count by status",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

        # Test 3: Timechart with multiple stats
        result = self.run_query_test(
            test_name="Timechart multiple statistics",
            query="index=web | timechart span=1h avg(response_time) as avg_time, max(response_time) as max_time, count",
            expected_min_results=1,
            earliest_time="-7d"
        )
        self.add_result(result)

    def run_all_tests(self):
        """Run all Lab 3 tests"""
        print(f"\nRunning Lab {self.lab_number} Tests: {self.lab_name}")
        print("=" * 70)

        self.test_stats_command()
        self.test_chart_command()
        self.test_timechart_command()

        self.print_summary()
        return self.get_summary()
