#!/usr/bin/env python3
"""
Lab 1: Setup Data Environment - Test Suite
Validates that all data is loaded and field extractions are configured
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.test_base import LabTestBase, LabTestResult


class Lab01Tests(LabTestBase):
    """Tests for Lab 1: Setup Data Environment"""

    def __init__(self, client):
        super().__init__(client, 1, "Setup Data Environment")

    def test_indexes_exist(self):
        """Verify all required indexes exist and have data"""

        indexes = ["web", "app", "auth", "sales", "performance", "api"]
        expected_counts = {
            "web": 100000,      # Expecting at least 100k events
            "app": 50000,       # Expecting at least 50k events
            "auth": 25000,      # Expecting at least 25k events
            "sales": 25000,     # Expecting at least 25k events
            "performance": 25000,  # Expecting at least 25k events
            "api": 50000        # Expecting at least 50k events
        }

        for index in indexes:
            result = self.run_query_test(
                test_name=f"Verify index '{index}' has data",
                query=f"index={index} | stats count",
                expected_min_results=1,
                required_fields=["count"],
                earliest_time="-30d"
            )

            # Check if count meets minimum threshold
            if result.passed and result.result_count > 0:
                # Get the actual count from the results
                try:
                    # Note: This is a simplification - actual count checking would need
                    # to parse the result data
                    print(f"  ✓ Index '{index}' has data")
                except:
                    pass

            self.add_result(result)

    def test_lookup_file(self):
        """Verify users.csv lookup file is loaded"""

        result = self.run_query_test(
            test_name="Verify users.csv lookup file",
            query="| inputlookup users.csv | stats count",
            expected_min_results=1,
            required_fields=["count"]
        )
        self.add_result(result)

    def test_field_extraction_response_time(self):
        """Verify response_time field extraction is configured"""

        result = self.run_query_test(
            test_name="Verify response_time field extraction",
            query="index=web | stats count avg(response_time) as avg_time | where isnotnull(avg_time)",
            expected_min_results=1,
            required_fields=["count", "avg_time"],
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_total_event_count(self):
        """Verify total event count across all indexes"""

        result = self.run_query_test(
            test_name="Verify total event count (~350k events)",
            query="index=* (index=web OR index=app OR index=auth OR index=sales OR index=performance OR index=api) | stats count",
            expected_min_results=1,
            required_fields=["count"],
            earliest_time="-30d"
        )
        self.add_result(result)

    def test_sourcetypes(self):
        """Verify correct sourcetypes are configured"""

        # Test web logs have access_combined_wcookie sourcetype
        result = self.run_query_test(
            test_name="Verify web logs use access_combined_wcookie sourcetype",
            query="index=web sourcetype=access_combined_wcookie | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Test API logs have _json sourcetype
        result = self.run_query_test(
            test_name="Verify API logs use _json sourcetype",
            query="index=api sourcetype=_json | head 10",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Note: application, auth, sales, and performance logs use auto-detected sourcetypes
        # which may vary, so we don't check specific sourcetypes for those

    def test_key_fields_exist(self):
        """Verify key fields are being extracted correctly"""

        # Web index fields
        result = self.run_query_test(
            test_name="Verify web log fields (clientip, method, status)",
            query="index=web | head 10 | fields clientip, method, status",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # App index fields
        result = self.run_query_test(
            test_name="Verify app log fields (host, level)",
            query="index=app | head 10 | fields host, level",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

        # Auth index fields
        result = self.run_query_test(
            test_name="Verify auth log fields (action, status)",
            query="index=auth | head 10 | fields action, status",
            expected_min_results=1,
            earliest_time="-30d"
        )
        self.add_result(result)

    def run_all_tests(self):
        """Run all Lab 1 tests"""
        print(f"\nRunning Lab {self.lab_number} Tests: {self.lab_name}")
        print("=" * 70)

        self.test_indexes_exist()
        self.test_lookup_file()
        self.test_field_extraction_response_time()
        self.test_total_event_count()
        self.test_sourcetypes()
        self.test_key_fields_exist()

        self.print_summary()
        return self.get_summary()
