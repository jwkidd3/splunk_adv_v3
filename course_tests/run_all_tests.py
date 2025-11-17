#!/usr/bin/env python3
"""
Splunk Advanced Course - Comprehensive Test Runner
Validates 100% of operations from all 14 labs
"""

import sys
import os
import json
import argparse
from datetime import datetime
from typing import List, Dict, Any
import urllib3

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.splunk_client import SplunkClient
from utils.test_base import DataValidator

# Import all lab tests
from lab_tests.lab01_tests import Lab01Tests
from lab_tests.lab02_tests import Lab02Tests
from lab_tests.lab03_tests import Lab03Tests
from lab_tests.lab04_to_14_tests import (
    Lab04Tests, Lab05Tests, Lab06Tests, Lab07Tests,
    Lab08Tests, Lab09Tests, Lab10Tests, Lab11Tests,
    Lab12Tests, Lab13Tests, Lab14Tests
)


class CourseTestRunner:
    """Main test runner for all course labs"""

    def __init__(self, host="localhost", port=8089, username="admin", password="changeme"):
        """
        Initialize test runner

        Args:
            host: Splunk host
            port: Splunk management port
            username: Splunk username
            password: Splunk password
        """
        self.client = SplunkClient(host, port, username, password)
        self.validator = DataValidator(self.client)
        self.results: List[Dict[str, Any]] = []
        self.start_time = None
        self.end_time = None

    def connect(self) -> bool:
        """
        Connect to Splunk

        Returns:
            True if connection successful
        """
        print("=" * 80)
        print("Splunk Advanced Course - Comprehensive Test Suite")
        print("=" * 80)
        print(f"\nConnecting to Splunk at {self.client.host}:{self.client.port}...")

        if not self.client.login():
            print("✗ Failed to connect to Splunk")
            print("\nPlease check:")
            print("  1. Splunk is running")
            print("  2. Splunk management port (8089) is accessible")
            print("  3. Username and password are correct")
            return False

        print("✓ Successfully connected to Splunk\n")
        return True

    def validate_data(self) -> bool:
        """
        Validate that required data exists

        Returns:
            True if all required data exists
        """
        print("=" * 80)
        print("Validating Course Data")
        print("=" * 80)

        validations = self.validator.validate_all_course_data()

        # Print index validations
        print("\nIndex Validation:")
        print("-" * 80)
        for idx_validation in validations["indexes"]:
            status = "✓" if idx_validation["valid"] else "✗"
            print(f"{status} {idx_validation['message']}")

        # Print lookup validations
        print("\nLookup Validation:")
        print("-" * 80)
        for lookup_validation in validations["lookups"]:
            status = "✓" if lookup_validation["valid"] else "✗"
            print(f"{status} {lookup_validation['message']}")

        print("\n" + "=" * 80)

        if not validations["overall_valid"]:
            print("\n⚠ WARNING: Some required data is missing!")
            print("Please run the data generation script:")
            print("  cd scripts")
            print("  ./generate-data.sh  (Mac/Linux)")
            print("  generate-data.bat   (Windows)")
            print("\nThen load the data into Splunk following scripts/README.md")
            print("\nTests will continue, but some may fail due to missing data.")
            input("\nPress Enter to continue anyway, or Ctrl+C to abort...")

        return validations["overall_valid"]

    def run_lab_tests(self, lab_number: int = None):
        """
        Run tests for specific lab or all labs

        Args:
            lab_number: Specific lab to test (1-14), or None for all
        """
        # Define all lab test classes
        lab_tests = [
            Lab01Tests(self.client),
            Lab02Tests(self.client),
            Lab03Tests(self.client),
            Lab04Tests(self.client),
            Lab05Tests(self.client),
            Lab06Tests(self.client),
            Lab07Tests(self.client),
            Lab08Tests(self.client),
            Lab09Tests(self.client),
            Lab10Tests(self.client),
            Lab11Tests(self.client),
            Lab12Tests(self.client),
            Lab13Tests(self.client),
            Lab14Tests(self.client)
        ]

        # Filter if specific lab requested
        if lab_number is not None:
            if 1 <= lab_number <= 14:
                lab_tests = [lab_tests[lab_number - 1]]
            else:
                print(f"Error: Invalid lab number {lab_number}. Must be 1-14.")
                return

        self.start_time = datetime.now()

        print("\n" + "=" * 80)
        print("Running Lab Tests")
        print("=" * 80)

        # Run all tests
        for lab_test in lab_tests:
            result = lab_test.run_all_tests()
            self.results.append(result)

        self.end_time = datetime.now()

    def print_overall_summary(self):
        """Print overall test summary"""
        print("\n" + "=" * 80)
        print("OVERALL TEST SUMMARY")
        print("=" * 80)

        total_labs = len(self.results)
        total_tests = sum(r["total_tests"] for r in self.results)
        total_passed = sum(r["passed"] for r in self.results)
        total_failed = sum(r["failed"] for r in self.results)

        duration = (self.end_time - self.start_time).total_seconds()

        print(f"\nTotal Labs Tested: {total_labs}")
        print(f"Total Tests Run: {total_tests}")
        print(f"Total Passed: {total_passed}")
        print(f"Total Failed: {total_failed}")
        print(f"Overall Pass Rate: {(total_passed / total_tests * 100) if total_tests > 0 else 0:.1f}%")
        print(f"Execution Time: {duration:.2f} seconds")

        # Lab-by-lab summary
        print("\n" + "-" * 80)
        print(f"{'Lab':<6} {'Name':<40} {'Tests':<8} {'Passed':<8} {'Failed':<8} {'Rate':<8}")
        print("-" * 80)

        for result in self.results:
            lab_num = result["lab_number"]
            lab_name = result["lab_name"][:38]
            tests = result["total_tests"]
            passed = result["passed"]
            failed = result["failed"]
            rate = result["pass_rate"]

            print(f"{lab_num:<6} {lab_name:<40} {tests:<8} {passed:<8} {failed:<8} {rate:.1f}%")

        print("=" * 80)

        # Failed tests detail
        failed_tests = [
            (r["lab_number"], r["lab_name"], test)
            for r in self.results
            for test in r["results"]
            if not test["passed"]
        ]

        if failed_tests:
            print("\n" + "=" * 80)
            print("FAILED TESTS DETAIL")
            print("=" * 80)

            for lab_num, lab_name, test in failed_tests:
                print(f"\nLab {lab_num}: {lab_name}")
                print(f"  Test: {test['test_name']}")
                print(f"  Error: {test['error_message']}")
                if test['query']:
                    print(f"  Query: {test['query'][:100]}...")

        print("\n" + "=" * 80)

    def save_report(self, filename: str = None):
        """
        Save test results to JSON file

        Args:
            filename: Output filename (default: test_results_TIMESTAMP.json)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"

        filepath = os.path.join("reports", filename)

        # Ensure reports directory exists
        os.makedirs("reports", exist_ok=True)

        report = {
            "timestamp": self.start_time.isoformat(),
            "duration_seconds": (self.end_time - self.start_time).total_seconds(),
            "total_labs": len(self.results),
            "total_tests": sum(r["total_tests"] for r in self.results),
            "total_passed": sum(r["passed"] for r in self.results),
            "total_failed": sum(r["failed"] for r in self.results),
            "overall_pass_rate": (sum(r["passed"] for r in self.results) / sum(r["total_tests"] for r in self.results) * 100) if sum(r["total_tests"] for r in self.results) > 0 else 0,
            "lab_results": self.results
        }

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Test report saved to: {filepath}")

        return filepath

    def run(self, lab_number: int = None, skip_validation: bool = False):
        """
        Run complete test suite

        Args:
            lab_number: Specific lab to test, or None for all
            skip_validation: Skip data validation
        """
        # Connect to Splunk
        if not self.connect():
            return False

        # Validate data
        if not skip_validation:
            self.validate_data()

        # Run tests
        self.run_lab_tests(lab_number)

        # Print summary
        self.print_overall_summary()

        # Save report
        self.save_report()

        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Splunk Advanced Course - Comprehensive Test Suite"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Splunk host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8089,
        help="Splunk management port (default: 8089)"
    )
    parser.add_argument(
        "--username",
        default="admin",
        help="Splunk username (default: admin)"
    )
    parser.add_argument(
        "--password",
        default="changeme",
        help="Splunk password (default: changeme)"
    )
    parser.add_argument(
        "--lab",
        type=int,
        choices=range(1, 15),
        help="Test specific lab only (1-14)"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip data validation check"
    )

    args = parser.parse_args()

    # Create and run test runner
    runner = CourseTestRunner(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )

    try:
        success = runner.run(
            lab_number=args.lab,
            skip_validation=args.skip_validation
        )
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\nTest execution cancelled by user.")
        sys.exit(1)

    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
