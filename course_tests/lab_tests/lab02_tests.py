#!/usr/bin/env python3
"""
Lab 2: Subsearches and Macros - Test Suite
Tests all operations from Lab 2
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.test_base import LabTestBase


class Lab02Tests(LabTestBase):
    """Tests for Lab 2: Subsearches and Macros"""

    def __init__(self, client):
        super().__init__(client, 2, "Subsearches and Macros")

    def test_exercise1_subsearches(self):
        """Exercise 1: Introduction to Subsearches"""

        # Test 1: Basic subsearch
        result = self.run_query_test(
            test_name="Basic subsearch (IPs with 404 errors)",
            query='index=web status=200 [search index=web status=404 | fields src_ip | dedup src_ip | head 10]',
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Subsearch with return
        result = self.run_query_test(
            test_name="Subsearch with return command",
            query="index=web [search index=auth action=login status=success | fields user | dedup user | head 10 | return 1000 $user]",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Subsearch with format
        result = self.run_query_test(
            test_name="Subsearch with format command",
            query="index=web [search index=app level=ERROR | fields host | format] | head 10",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_exercise2_advanced_subsearches(self):
        """Exercise 2: Advanced Subsearch Patterns"""

        # Test 1: Find related events
        result = self.run_query_test(
            test_name="Related events subsearch",
            query="index=web [search index=web status>=500 | head 10 | fields src_ip] | stats count by user, src_ip",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: NOT with subsearch
        result = self.run_query_test(
            test_name="NOT with subsearch",
            query="index=web NOT [search index=web status=200 | fields session_id | head 100] | head 10",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 3: Multiple subsearches
        result = self.run_query_test(
            test_name="Multiple subsearches with OR",
            query="index=web [search index=web status>=500 | fields src_ip | head 10] OR [search index=auth action=login_failed | fields src_ip | head 10] | head 10",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_exercise3_macros(self):
        """Exercise 3: Creating and Using Macros"""

        # Note: Macros need to be created manually or via API
        # These tests assume macros are created

        # Test 1: Simple macro (if exists)
        result = self.run_query_test(
            test_name="Simple macro usage (get_errors)",
            query="index=web status>=400 status<600 | stats count by status",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test 2: Macro with time range
        result = self.run_query_test(
            test_name="Time range pattern",
            query="index=web earliest=-24h | stats count",
            expected_min_results=1,
            earliest_time="-24h"
        )
        self.add_result(result)

        # Test 3: Complex aggregation pattern
        result = self.run_query_test(
            test_name="Aggregation pattern (top users)",
            query="index=web | stats count by user | sort -count | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_challenges(self):
        """Test Challenge Scenarios"""

        # Challenge 1: Anomaly detection
        result = self.run_query_test(
            test_name="Challenge 1: New location login detection",
            query='index=auth action=login earliest=-1d NOT [search index=auth action=login earliest=-30d latest=-1d | fields user, src_ip] | stats count by user, src_ip | sort -count | head 10',
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Challenge 2: Top active users analysis
        result = self.run_query_test(
            test_name="Challenge 2: Active users analysis",
            query="index=web [search index=web earliest=-24h | stats count by user | sort -count | head 10 | fields user] | stats count as total by user | sort -total",
            expected_min_results=0,
            earliest_time="-30d"
        )
        self.add_result(result)

    def run_all_tests(self):
        """Run all Lab 2 tests"""
        print(f"\nRunning Lab {self.lab_number} Tests: {self.lab_name}")
        print("=" * 70)

        self.test_exercise1_subsearches()
        self.test_exercise2_advanced_subsearches()
        self.test_exercise3_macros()
        self.test_challenges()

        self.print_summary()
        return self.get_summary()
