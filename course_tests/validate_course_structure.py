#!/usr/bin/env python3
"""
Validate complete course structure, presentations, and lab alignment
"""

import os
import sys
from pathlib import Path
import re

class CourseValidator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.errors = []
        self.warnings = []

    def print_header(self, text):
        print("\n" + "=" * 80)
        print(f"  {text}")
        print("=" * 80 + "\n")

    def print_section(self, text):
        print(f"\n{text}")
        print("-" * 80)

    def validate_presentations(self):
        """Validate all presentation files exist and are properly structured"""
        self.print_section("Validating Presentations")

        presentations = {
            "content1_presentation.html": {
                "title": "Introduction & Search Review",
                "labs": [1]
            },
            "content2_presentation.html": {
                "title": "Subsearches, Macros & Statistical Commands",
                "labs": [2, 3]
            },
            "content3_presentation.html": {
                "title": "Join Command, Multi-Index Searches & Time-Based Analysis",
                "labs": [4, 5]
            },
            "content4_presentation.html": {
                "title": "Dashboards, Visualizations & Search Optimization",
                "labs": [6, 7]
            },
            "content5_presentation.html": {
                "title": "Data Transformation with Eval, Rex & Lookups",
                "labs": [8, 9, 10]
            },
            "content6_presentation.html": {
                "title": "Machine Learning, Analytics & System Administration",
                "labs": [11, 12, 13, 14]
            }
        }

        presentations_dir = self.base_dir / "presentations"

        for filename, info in presentations.items():
            filepath = presentations_dir / filename
            if not filepath.exists():
                self.errors.append(f"Missing presentation: {filename}")
                print(f"  ✗ {filename} - NOT FOUND")
            else:
                # Check file size
                size_kb = filepath.stat().st_size / 1024
                print(f"  ✓ {filename} ({size_kb:.1f}KB)")
                print(f"    Title: {info['title']}")
                print(f"    Covers Labs: {', '.join(map(str, info['labs']))}")

                # Verify it's valid HTML
                try:
                    content = filepath.read_text(encoding='utf-8')
                    if '<html' not in content.lower():
                        self.errors.append(f"{filename} doesn't appear to be valid HTML")
                    if len(content) < 5000:
                        self.warnings.append(f"{filename} seems too small ({len(content)} bytes)")
                except Exception as e:
                    self.errors.append(f"Error reading {filename}: {e}")

        return len(self.errors) == 0

    def validate_labs(self):
        """Validate all lab directories and README files"""
        self.print_section("Validating Labs")

        labs = [
            {"num": 1, "dir": "lab1-review-search-basics", "name": "Review of Search Basics"},
            {"num": 2, "dir": "lab2-subsearches-macros", "name": "Subsearches and Macros"},
            {"num": 3, "dir": "lab3-statistical-commands", "name": "Statistical Commands"},
            {"num": 4, "dir": "lab4-join-multi-index", "name": "Join Command and Multi-Index Searches"},
            {"num": 5, "dir": "lab5-time-based-searches", "name": "Time-Based Searches"},
            {"num": 6, "dir": "lab6-dashboards-visualizations", "name": "Custom Dashboards and Visualizations"},
            {"num": 7, "dir": "lab7-search-optimization", "name": "Search Optimization"},
            {"num": 8, "dir": "lab8-eval-data-manipulation", "name": "Eval Command and Data Manipulation"},
            {"num": 9, "dir": "lab9-regex-rex", "name": "Regular Expressions with Rex"},
            {"num": 10, "dir": "lab10-lookups-enrichment", "name": "Lookups and Data Enrichment"},
            {"num": 11, "dir": "lab11-ml-toolkit-intro", "name": "Machine Learning Toolkit Introduction"},
            {"num": 12, "dir": "lab12-time-series-analysis", "name": "Time Series Analysis"},
            {"num": 13, "dir": "lab13-user-role-management", "name": "User and Role Management"},
            {"num": 14, "dir": "lab14-system-admin-monitoring", "name": "System Administration and Monitoring"}
        ]

        labs_dir = self.base_dir / "labs"

        for lab in labs:
            lab_path = labs_dir / lab["dir"]
            readme_path = lab_path / "README.md"

            if not lab_path.exists():
                self.errors.append(f"Missing lab directory: {lab['dir']}")
                print(f"  ✗ Lab {lab['num']}: {lab['name']} - DIRECTORY NOT FOUND")
            elif not readme_path.exists():
                self.errors.append(f"Missing README in {lab['dir']}")
                print(f"  ✗ Lab {lab['num']}: {lab['name']} - README.md NOT FOUND")
            else:
                readme_content = readme_path.read_text(encoding='utf-8')

                # Check for proper lab structure
                has_objectives = "## Lab Objectives" in readme_content or "## Objectives" in readme_content
                has_exercises = "## Exercises" in readme_content or "### Exercise" in readme_content

                status = "✓" if has_objectives and has_exercises else "⚠"
                print(f"  {status} Lab {lab['num']}: {lab['name']}")

                if not has_objectives:
                    self.warnings.append(f"Lab {lab['num']} missing 'Lab Objectives' section")
                if not has_exercises:
                    self.warnings.append(f"Lab {lab['num']} missing 'Exercises' section")

                # Check prerequisites
                if lab['num'] > 1:
                    prereq_patterns = [
                        f"Lab {lab['num']-1}",
                        f"Labs 1-{lab['num']-1}",
                        "Prerequisites",
                        "prereq"
                    ]
                    has_prereq = any(pattern.lower() in readme_content.lower() for pattern in prereq_patterns)
                    if not has_prereq:
                        self.warnings.append(f"Lab {lab['num']} should reference previous labs")

        return len(self.errors) == 0

    def validate_presentation_lab_alignment(self):
        """Validate that presentations and labs are properly aligned"""
        self.print_section("Validating Presentation-Lab Alignment")

        # Expected structure from README
        sessions = [
            {"session": 1, "presentation": "content1", "labs": [1], "name": "Introduction & Search Basics"},
            {"session": 2, "presentation": "content2", "labs": [2, 3], "name": "Advanced Search Techniques"},
            {"session": 3, "presentation": "content3", "labs": [4, 5], "name": "Data Correlation & Time Analysis"},
            {"session": 4, "presentation": "content4", "labs": [6, 7], "name": "Visualization & Optimization"},
            {"session": 5, "presentation": "content5", "labs": [8, 9, 10], "name": "Data Transformation"},
            {"session": 6, "presentation": "content6", "labs": [11, 12, 13, 14], "name": "Machine Learning & Administration"}
        ]

        for session in sessions:
            pres_file = f"{session['presentation']}_presentation.html"
            pres_path = self.base_dir / "presentations" / pres_file

            print(f"\n  Session {session['session']}: {session['name']}")
            print(f"    Presentation: {pres_file}")
            print(f"    Covers Labs: {', '.join(map(str, session['labs']))}")

            if pres_path.exists():
                print(f"    ✓ Presentation exists")
            else:
                self.errors.append(f"Session {session['session']} missing presentation")
                print(f"    ✗ Presentation missing")

            # Verify all labs exist
            all_labs_exist = True
            for lab_num in session['labs']:
                lab_dirs = list((self.base_dir / "labs").glob(f"lab{lab_num}-*"))
                if not lab_dirs:
                    all_labs_exist = False
                    self.errors.append(f"Session {session['session']} references missing Lab {lab_num}")

            if all_labs_exist:
                print(f"    ✓ All labs exist")
            else:
                print(f"    ✗ Some labs missing")

        return len(self.errors) == 0

    def validate_readme_structure(self):
        """Validate main README.md structure"""
        self.print_section("Validating Main README.md")

        readme_path = self.base_dir / "README.md"

        if not readme_path.exists():
            self.errors.append("Main README.md not found")
            print("  ✗ README.md NOT FOUND")
            return False

        content = readme_path.read_text(encoding='utf-8')

        # Check for required sections
        required_sections = [
            "# Splunk Advanced Course",
            "## Table of Contents",
            "## Course Structure",
            "## Detailed Course Flow",
            "## Lab Quick Reference",
            "Session 1:",
            "Session 2:",
            "Session 3:",
            "Session 4:",
            "Session 5:",
            "Session 6:"
        ]

        for section in required_sections:
            if section in content:
                print(f"  ✓ {section}")
            else:
                self.errors.append(f"README missing section: {section}")
                print(f"  ✗ {section} - MISSING")

        # Verify no "Day 1" or "Day 2" references
        if "Day 1" in content or "Day 2" in content or "2-day" in content:
            self.warnings.append("README still contains day references (should be Part 1/Part 2)")
            print("  ⚠ Found day references (should be removed)")
        else:
            print("  ✓ No day references found")

        # Check for 6 presentations mentioned
        if "6 comprehensive Reveal.js presentations" in content:
            print("  ✓ References 6 presentations")
        else:
            self.warnings.append("README should mention 6 presentations")

        return len(self.errors) == 0

    def validate_data_files(self):
        """Validate required data files exist"""
        self.print_section("Validating Data Files")

        required_files = [
            "web_access.log",
            "application.log",
            "auth.log",
            "sales.log",
            "performance.log",
            "api.log",
            "users.csv"
        ]

        data_dir = self.base_dir / "data"

        for filename in required_files:
            filepath = data_dir / filename
            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"  ✓ {filename} ({size_mb:.1f}MB)")
            else:
                self.errors.append(f"Missing data file: {filename}")
                print(f"  ✗ {filename} - NOT FOUND")

        return len(self.errors) == 0

    def validate_scripts(self):
        """Validate utility scripts exist"""
        self.print_section("Validating Scripts")

        scripts_dir = self.base_dir / "scripts"
        required_scripts = [
            "generate_sample_data.py",
            "load_data_to_splunk.py",
            "README.md"
        ]

        for script in required_scripts:
            filepath = scripts_dir / script
            if filepath.exists():
                if script.endswith('.py'):
                    size_kb = filepath.stat().st_size / 1024
                    print(f"  ✓ {script} ({size_kb:.1f}KB)")
                else:
                    print(f"  ✓ {script}")
            else:
                self.errors.append(f"Missing script: {script}")
                print(f"  ✗ {script} - NOT FOUND")

        return len(self.errors) == 0

    def run_validation(self):
        """Run complete validation"""
        self.print_header("SPLUNK ADVANCED COURSE - STRUCTURE VALIDATION")

        results = {
            "Presentations": self.validate_presentations(),
            "Labs": self.validate_labs(),
            "Presentation-Lab Alignment": self.validate_presentation_lab_alignment(),
            "README Structure": self.validate_readme_structure(),
            "Data Files": self.validate_data_files(),
            "Scripts": self.validate_scripts()
        }

        # Print summary
        self.print_header("VALIDATION SUMMARY")

        for component, passed in results.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"  {status}: {component}")

        if self.warnings:
            print(f"\n⚠ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.errors:
            print(f"\n✗ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            print("\n❌ VALIDATION FAILED")
            return False
        else:
            print("\n✅ ALL VALIDATIONS PASSED")
            if self.warnings:
                print(f"   (with {len(self.warnings)} warnings)")
            return True

def main():
    validator = CourseValidator()
    success = validator.run_validation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
