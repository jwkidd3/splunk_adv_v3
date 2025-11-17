#!/usr/bin/env python3
"""
Lab 1: Review of Search Basics - Test Suite
Tests all operations from Lab 1
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.test_base import LabTestBase, LabTestResult


class Lab01Tests(LabTestBase):
    """Tests for Lab 1: Review of Search Basics"""

    def __init__(self, client):
        super().__init__(client, 1, "Review of Search Basics")

    def test_exercise1_basic_searches(self):
        """Exercise 1: Basic Search Operations"""

        # Test 1: Simple keyword search
        result = self.run_query_test(
            test_name="Simple keyword search (error)",
            query="error",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Wildcard search
        result = self.run_query_test(
            test_name="Wildcard search (error*)",
            query="error*",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Boolean AND
        result = self.run_query_test(
            test_name="Boolean AND (error AND failed)",
            query="error AND failed",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 4: Boolean OR
        result = self.run_query_test(
            test_name="Boolean OR (error OR failed)",
            query="error OR failed",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 5: Boolean NOT
        result = self.run_query_test(
            test_name="Boolean NOT (error NOT warning)",
            query="error NOT warning",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_exercise2_field_extraction(self):
        """Exercise 2: Field Extraction and Filtering"""

        # Test 1: Fields command
        result = self.run_query_test(
            test_name="Fields command",
            query="index=web | fields host, source, sourcetype | head 10",
            expected_min_results=1,
            required_fields=["host", "sourcetype"],
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Field value filtering
        result = self.run_query_test(
            test_name="Filter by field value (status=404)",
            query="index=web status=404 | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Field range filtering
        result = self.run_query_test(
            test_name="Field range filter (status>=400 status<500)",
            query="index=web status>=400 status<500 | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 4: Where command basic
        result = self.run_query_test(
            test_name="Where command (status=404)",
            query="index=web | where status=404 | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 5: Where with complex logic
        result = self.run_query_test(
            test_name="Where with AND logic",
            query="index=web | where status > 400 AND status < 500 | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 6: Where with isnotnull
        result = self.run_query_test(
            test_name="Where isnotnull(user_id)",
            query="index=web | where isnotnull(user_id) | head 10",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_exercise3_statistical_commands(self):
        """Exercise 3: Statistical Commands"""

        # Test 1: Simple count
        result = self.run_query_test(
            test_name="Stats count",
            query="index=web | stats count",
            expected_min_results=1,
            required_fields=["count"],
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Count by field
        result = self.run_query_test(
            test_name="Stats count by status",
            query="index=web | stats count by status",
            expected_min_results=1,
            required_fields=["count", "status"],
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Multiple statistics
        result = self.run_query_test(
            test_name="Multiple stats (count, avg, max)",
            query="index=web | stats count, avg(response_time) as avg_time, max(response_time) as max_time by host",
            expected_min_results=1,
            required_fields=["count", "host"],
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 4: Top command
        result = self.run_query_test(
            test_name="Top command (top 10 user)",
            query="index=web | top limit=10 user",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 5: Rare command
        result = self.run_query_test(
            test_name="Rare command (rare 10 source)",
            query="index=web | rare limit=10 source",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_challenges(self):
        """Test Challenge Scenarios"""

        # Challenge 1: Search efficiency
        result = self.run_query_test(
            test_name="Challenge 1: Authentication failures",
            query='index=auth action=login_failed | fields _time, user, src_ip | sort -_time | head 10',
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Challenge 2: Error analysis
        result = self.run_query_test(
            test_name="Challenge 2: Error count by sourcetype",
            query="index=app level=ERROR | stats count by sourcetype | sort -count",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Challenge 3: Performance metrics
        result = self.run_query_test(
            test_name="Challenge 3: Response time stats by status",
            query="index=web | stats avg(response_time) as avg_time, min(response_time) as min_time, max(response_time) as max_time by status | sort -avg_time",
            expected_min_results=1,
            required_fields=["avg_time", "status"],
            earliest_time="-30d"
        )
        self.add_result(result)

    def run_all_tests(self):
        """Run all Lab 1 tests"""
        print(f"\nRunning Lab {self.lab_number} Tests: {self.lab_name}")
        print("=" * 70)

        self.test_exercise1_basic_searches()
        self.test_exercise2_field_extraction()
        self.test_exercise3_statistical_commands()
        self.test_challenges()

        self.print_summary()
        return self.get_summary()
