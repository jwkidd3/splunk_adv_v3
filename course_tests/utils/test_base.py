#!/usr/bin/env python3
"""
Base Test Class for Course Lab Validation
Provides common testing functionality
"""

import time
from typing import Dict, List, Any, Optional
from .splunk_client import SplunkClient


class LabTestResult:
    """Represents the result of a single test"""

    def __init__(self, test_name: str, lab_number: int):
        self.test_name = test_name
        self.lab_number = lab_number
        self.passed = False
        self.error_message = None
        self.query = None
        self.result_count = 0
        self.execution_time = 0.0
        self.details = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            "test_name": self.test_name,
            "lab_number": self.lab_number,
            "passed": self.passed,
            "error_message": self.error_message,
            "query": self.query,
            "result_count": self.result_count,
            "execution_time": self.execution_time,
            "details": self.details
        }


class LabTestBase:
    """Base class for lab tests"""

    def __init__(self, client: SplunkClient, lab_number: int, lab_name: str):
        """
        Initialize lab test

        Args:
            client: SplunkClient instance
            lab_number: Lab number (1-14)
            lab_name: Lab name/description
        """
        self.client = client
        self.lab_number = lab_number
        self.lab_name = lab_name
        self.results: List[LabTestResult] = []

    def run_query_test(self, test_name: str, query: str,
                      expected_min_results: int = 0,
                      expected_max_results: Optional[int] = None,
                      earliest_time: str = "-24h",
                      latest_time: str = "now",
                      required_fields: Optional[List[str]] = None) -> LabTestResult:
        """
        Run a single query test

        Args:
            test_name: Name of the test
            query: SPL query to execute
            expected_min_results: Minimum expected result count
            expected_max_results: Maximum expected result count (None = no limit)
            earliest_time: Search earliest time
            latest_time: Search latest time
            required_fields: List of fields that must exist in results

        Returns:
            LabTestResult object
        """
        result = LabTestResult(test_name, self.lab_number)
        result.query = query

        try:
            start_time = time.time()

            # Execute search
            search_result = self.client.execute_search(
                query=query,
                earliest_time=earliest_time,
                latest_time=latest_time
            )

            result.execution_time = time.time() - start_time

            if not search_result["success"]:
                result.passed = False
                result.error_message = search_result.get("error", "Unknown error")
                return result

            result.result_count = search_result["count"]
            results_data = search_result["results"]

            # Check minimum results
            if result.result_count < expected_min_results:
                result.passed = False
                result.error_message = f"Expected at least {expected_min_results} results, got {result.result_count}"
                return result

            # Check maximum results
            if expected_max_results is not None and result.result_count > expected_max_results:
                result.passed = False
                result.error_message = f"Expected at most {expected_max_results} results, got {result.result_count}"
                return result

            # Check required fields
            if required_fields and result.result_count > 0:
                first_result = results_data[0]
                missing_fields = [field for field in required_fields if field not in first_result]

                if missing_fields:
                    result.passed = False
                    result.error_message = f"Missing required fields: {', '.join(missing_fields)}"
                    return result

            # Test passed
            result.passed = True
            result.details = {
                "result_count": result.result_count,
                "execution_time": result.execution_time,
                "sample_results": results_data[:3] if results_data else []
            }

        except Exception as e:
            result.passed = False
            result.error_message = f"Exception during test: {str(e)}"

        return result

    def add_result(self, result: LabTestResult):
        """Add a test result to the collection"""
        self.results.append(result)

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary of all tests

        Returns:
            Dictionary with test summary
        """
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        return {
            "lab_number": self.lab_number,
            "lab_name": self.lab_name,
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "results": [r.to_dict() for r in self.results]
        }

    def print_summary(self):
        """Print test summary to console"""
        summary = self.get_summary()

        print(f"\n{'=' * 70}")
        print(f"Lab {self.lab_number}: {self.lab_name}")
        print(f"{'=' * 70}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"{'=' * 70}")

        if summary['failed'] > 0:
            print("\nFailed Tests:")
            for result in self.results:
                if not result.passed:
                    print(f"  ✗ {result.test_name}")
                    print(f"    Error: {result.error_message}")
                    if result.query:
                        print(f"    Query: {result.query[:100]}...")

        print()

    def run_all_tests(self):
        """
        Run all tests for this lab
        This method should be overridden by subclasses
        """
        raise NotImplementedError("Subclasses must implement run_all_tests()")


class DataValidator:
    """Validates that required data exists for labs"""

    def __init__(self, client: SplunkClient):
        self.client = client

    def validate_index(self, index: str, min_events: int = 1000) -> Dict[str, Any]:
        """
        Validate that an index exists and has sufficient data

        Args:
            index: Index name
            min_events: Minimum expected events

        Returns:
            Validation result dictionary
        """
        result = self.client.check_index_data(index)

        if not result["has_data"]:
            return {
                "valid": False,
                "index": index,
                "message": f"Index '{index}' has no data or does not exist"
            }

        if result["event_count"] < min_events:
            return {
                "valid": False,
                "index": index,
                "event_count": result["event_count"],
                "message": f"Index '{index}' has only {result['event_count']} events, expected at least {min_events}"
            }

        return {
            "valid": True,
            "index": index,
            "event_count": result["event_count"],
            "message": f"Index '{index}' validated with {result['event_count']} events"
        }

    def validate_lookup(self, lookup_name: str, min_rows: int = 1) -> Dict[str, Any]:
        """
        Validate that a lookup file exists and has data

        Args:
            lookup_name: Lookup file name
            min_rows: Minimum expected rows

        Returns:
            Validation result dictionary
        """
        result = self.client.check_lookup(lookup_name)

        if not result["has_data"]:
            return {
                "valid": False,
                "lookup": lookup_name,
                "message": f"Lookup '{lookup_name}' has no data or does not exist"
            }

        if result["row_count"] < min_rows:
            return {
                "valid": False,
                "lookup": lookup_name,
                "row_count": result["row_count"],
                "message": f"Lookup '{lookup_name}' has only {result['row_count']} rows, expected at least {min_rows}"
            }

        return {
            "valid": True,
            "lookup": lookup_name,
            "row_count": result["row_count"],
            "message": f"Lookup '{lookup_name}' validated with {result['row_count']} rows"
        }

    def validate_all_course_data(self) -> Dict[str, Any]:
        """
        Validate all required data for the course

        Returns:
            Comprehensive validation results
        """
        validations = {
            "indexes": [],
            "lookups": [],
            "overall_valid": True
        }

        # Validate indexes
        required_indexes = [
            ("web", 10000),
            ("app", 5000),
            ("auth", 1000),
            ("sales", 5000),
            ("performance", 1000),
            ("api", 5000)
        ]

        for index, min_events in required_indexes:
            validation = self.validate_index(index, min_events)
            validations["indexes"].append(validation)
            if not validation["valid"]:
                validations["overall_valid"] = False

        # Validate lookups
        required_lookups = [
            ("users.csv", 100)
        ]

        for lookup, min_rows in required_lookups:
            validation = self.validate_lookup(lookup, min_rows)
            validations["lookups"].append(validation)
            if not validation["valid"]:
                validations["overall_valid"] = False

        return validations
