#!/usr/bin/env python3
"""
Splunk Advanced Course - Full Validation Runner
Coordinates: Start Splunk → Generate Data → Load Data → Run Tests
Retries until 100% passing or max attempts reached
"""

import subprocess
import sys
import os
import time
import json
from datetime import datetime
import platform

# Configuration
MAX_ATTEMPTS = 3
SPLUNK_PASSWORD = "password"
SPLUNK_CONTAINER = "splunk-course"

class ValidationRunner:
    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.script_ext = ".bat" if self.is_windows else ".sh"
        self.python_cmd = "python" if self.is_windows else "python3"
        self.scripts_dir = "scripts"
        self.attempt = 0
        self.results = []

    def run_command(self, command, cwd=None, shell=False):
        """Run a shell command and return success status"""
        try:
            if isinstance(command, str) and not shell:
                command = command.split()

            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                shell=shell
            )

            return result.returncode == 0, result.stdout, result.stderr

        except Exception as e:
            return False, "", str(e)

    def print_header(self, text):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(text.center(80))
        print("=" * 80 + "\n")

    def print_step(self, step_num, total_steps, description):
        """Print step information"""
        print(f"\n[Step {step_num}/{total_steps}] {description}")
        print("-" * 80)

    def cleanup_splunk(self):
        """Stop and remove Splunk container"""
        print("Cleaning up existing Splunk container...")

        if self.is_windows:
            # Windows - forcefully remove
            subprocess.run(f"docker stop {SPLUNK_CONTAINER}", shell=True, capture_output=True)
            subprocess.run(f"docker rm {SPLUNK_CONTAINER}", shell=True, capture_output=True)
        else:
            # Mac/Linux
            subprocess.run(["docker", "stop", SPLUNK_CONTAINER], capture_output=True)
            subprocess.run(["docker", "rm", SPLUNK_CONTAINER], capture_output=True)

        time.sleep(2)

    def start_splunk(self):
        """Start Splunk container"""
        self.print_step(1, 5, "Starting Splunk Enterprise")

        script = os.path.join(self.scripts_dir, f"start-splunk{self.script_ext}")

        if self.is_windows:
            # Windows - need to handle interactive script
            success, stdout, stderr = self.run_command(f'"{script}"', shell=True)
        else:
            # Mac/Linux
            success, stdout, stderr = self.run_command(["bash", script])

        if success or "already running" in stdout.lower():
            print("✓ Splunk started successfully")
            return True
        else:
            print(f"✗ Failed to start Splunk")
            if stderr:
                print(f"Error: {stderr[:200]}")
            return False

    def generate_data(self):
        """Generate sample data"""
        self.print_step(2, 5, "Generating Sample Data")

        # Check if data already exists
        data_dir = "data"
        if os.path.exists(data_dir) and len(os.listdir(data_dir)) > 0:
            print("ℹ Sample data already exists, skipping generation")
            return True

        script = "generate_sample_data.py"
        success, stdout, stderr = self.run_command([self.python_cmd, script], cwd=self.scripts_dir)

        if success:
            print("✓ Data generated successfully")
            return True
        else:
            print(f"✗ Failed to generate data")
            if stderr:
                print(f"Error: {stderr[:200]}")
            return False

    def load_data(self):
        """Load data into Splunk"""
        self.print_step(3, 5, "Loading Data into Splunk")

        # Wait a bit for Splunk to be fully ready
        print("Waiting for Splunk to initialize...")
        time.sleep(10)

        script = "load_data_to_splunk.py"
        success, stdout, stderr = self.run_command([self.python_cmd, script], cwd=self.scripts_dir)

        if success:
            print("✓ Data loaded successfully")
            return True
        else:
            print(f"✗ Failed to load data")
            if stderr:
                print(f"Error: {stderr[:200]}")
            return False

    def wait_for_data_indexed(self):
        """Wait for data to be fully indexed"""
        print("\nWaiting for data to be indexed (30 seconds)...")
        time.sleep(30)

    def run_tests(self):
        """Run comprehensive test suite"""
        self.print_step(4, 5, "Running Comprehensive Test Suite")

        test_script = os.path.join("course_tests", "run_all_tests.py")
        success, stdout, stderr = self.run_command(
            [self.python_cmd, test_script, "--password", SPLUNK_PASSWORD, "--skip-validation"]
        )

        # Parse results from JSON report
        report_dir = os.path.join("course_tests", "reports")
        if os.path.exists(report_dir):
            # Find latest report
            reports = [f for f in os.listdir(report_dir) if f.startswith("test_results_")]
            if reports:
                latest_report = max(reports)
                report_path = os.path.join(report_dir, latest_report)

                try:
                    with open(report_path, 'r') as f:
                        result_data = json.load(f)

                    return {
                        "success": success,
                        "data": result_data,
                        "stdout": stdout
                    }
                except:
                    pass

        return {
            "success": success,
            "data": None,
            "stdout": stdout
        }

    def generate_final_report(self, final_result):
        """Generate comprehensive final report"""
        self.print_step(5, 5, "Generating Final Report")

        report = {
            "timestamp": datetime.now().isoformat(),
            "attempts": self.attempt,
            "max_attempts": MAX_ATTEMPTS,
            "final_success": final_result is not None,
            "results": self.results
        }

        # Save report
        report_file = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Print summary
        self.print_header("VALIDATION SUMMARY")

        if final_result:
            data = final_result["data"]
            print(f"✓ VALIDATION SUCCESSFUL")
            print()
            print(f"Total Attempts: {self.attempt}")
            print(f"Total Labs Tested: {data.get('total_labs', 0)}")
            print(f"Total Tests Run: {data.get('total_tests', 0)}")
            print(f"Total Passed: {data.get('total_passed', 0)}")
            print(f"Total Failed: {data.get('total_failed', 0)}")
            print(f"Pass Rate: {data.get('overall_pass_rate', 0):.1f}%")
            print()

            # Detailed breakdown
            print("Lab-by-Lab Results:")
            print("-" * 80)
            print(f"{'Lab':<6} {'Name':<40} {'Tests':<8} {'Pass':<8} {'Rate':<8}")
            print("-" * 80)

            for lab_result in data.get('lab_results', []):
                lab_num = lab_result['lab_number']
                lab_name = lab_result['lab_name'][:38]
                tests = lab_result['total_tests']
                passed = lab_result['passed']
                rate = lab_result['pass_rate']
                print(f"{lab_num:<6} {lab_name:<40} {tests:<8} {passed:<8} {rate:.1f}%")

            print("-" * 80)
            print()
            print(f"Detailed report saved to: {report_file}")

        else:
            print(f"✗ VALIDATION FAILED AFTER {MAX_ATTEMPTS} ATTEMPTS")
            print()
            print(f"Detailed report saved to: {report_file}")

        return report_file

    def run_validation_attempt(self):
        """Run single validation attempt"""
        self.attempt += 1

        self.print_header(f"VALIDATION ATTEMPT {self.attempt}/{MAX_ATTEMPTS}")

        # Step 1: Start Splunk
        if not self.start_splunk():
            return None

        # Step 2: Generate data
        if not self.generate_data():
            return None

        # Step 3: Load data
        if not self.load_data():
            return None

        # Wait for indexing
        self.wait_for_data_indexed()

        # Step 4: Run tests
        result = self.run_tests()

        # Store result
        self.results.append({
            "attempt": self.attempt,
            "timestamp": datetime.now().isoformat(),
            "success": result["success"],
            "data": result.get("data")
        })

        # Check if 100% passing
        if result["data"]:
            pass_rate = result["data"].get("overall_pass_rate", 0)
            if pass_rate == 100.0:
                print(f"\n✓ 100% PASS RATE ACHIEVED!")
                return result

        print(f"\n⚠ Pass rate: {result['data'].get('overall_pass_rate', 0) if result['data'] else 0:.1f}%")

        return None

    def run(self):
        """Main execution flow"""
        self.print_header("SPLUNK ADVANCED COURSE - FULL VALIDATION")

        print("This script will:")
        print("  1. Start Splunk Enterprise in Docker")
        print("  2. Generate sample data (~450,000 events)")
        print("  3. Load data into Splunk (6 indexes)")
        print("  4. Run comprehensive test suite (72+ tests)")
        print("  5. Retry until 100% pass rate or max attempts")
        print()
        print(f"Max Attempts: {MAX_ATTEMPTS}")
        print(f"Splunk Password: {SPLUNK_PASSWORD}")
        print()
        print("Starting automated validation...")
        print()

        # Cleanup any existing Splunk instance
        self.cleanup_splunk()

        # Run validation attempts
        final_result = None
        for _ in range(MAX_ATTEMPTS):
            result = self.run_validation_attempt()

            if result:
                final_result = result
                break

            if self.attempt < MAX_ATTEMPTS:
                print(f"\nRetrying in 10 seconds...")
                time.sleep(10)
                self.cleanup_splunk()

        # Generate final report
        report_file = self.generate_final_report(final_result)

        self.print_header("VALIDATION COMPLETE")

        if final_result:
            print("✓ All tests passing! Course is ready for delivery.")
            return 0
        else:
            print("✗ Validation incomplete. Review the report for details.")
            return 1

def main():
    try:
        runner = ValidationRunner()
        exit_code = runner.run()
        sys.exit(exit_code)

    except KeyboardInterrupt:
        print("\n\nValidation cancelled by user.")
        sys.exit(1)

    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
