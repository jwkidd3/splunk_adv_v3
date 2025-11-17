#!/usr/bin/env python3
"""
Load generated sample data into Splunk
Creates indexes and loads all data files

Cross-platform compatible (Windows, Mac, Linux)
"""

import requests
import os
import sys
import time
import json
import urllib3
import platform
from pathlib import Path

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration
SPLUNK_HOST = "localhost"
SPLUNK_PORT = 8089
SPLUNK_USERNAME = "admin"
SPLUNK_PASSWORD = "password"

# Get the script directory and data directory (cross-platform)
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR.parent / "data"

# Index configuration
INDEXES = [
    {"name": "web", "datatype": "event"},
    {"name": "app", "datatype": "event"},
    {"name": "auth", "datatype": "event"},
    {"name": "sales", "datatype": "event"},
    {"name": "performance", "datatype": "event"},
    {"name": "api", "datatype": "event"}
]

# Data file mappings
DATA_FILES = [
    {"file": "web_access.log", "index": "web", "sourcetype": "access_combined"},
    {"file": "application.log", "index": "app", "sourcetype": "syslog"},
    {"file": "auth.log", "index": "auth", "sourcetype": "linux_secure"},
    {"file": "sales.log", "index": "sales", "sourcetype": "_json"},
    {"file": "performance.log", "index": "performance", "sourcetype": "_json"},
    {"file": "api.log", "index": "api", "sourcetype": "_json"}
]

class SplunkLoader:
    def __init__(self, host, port, username, password):
        self.base_url = f"https://{host}:{port}"
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.verify = False

    def wait_for_splunk(self, timeout=180):
        """Wait for Splunk to be ready"""
        print("Waiting for Splunk to be ready...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = self.session.get(
                    f"{self.base_url}/services/server/info",
                    auth=self.auth
                )
                if response.status_code == 200:
                    print("✓ Splunk is ready")
                    return True
            except:
                pass

            print(".", end="", flush=True)
            time.sleep(2)

        print("\n✗ Timeout waiting for Splunk")
        return False

    def create_index(self, index_name, datatype="event"):
        """Create a Splunk index"""
        url = f"{self.base_url}/servicesNS/nobody/system/data/indexes"
        data = {
            "name": index_name,
            "datatype": datatype
        }

        try:
            response = self.session.post(url, auth=self.auth, data=data)

            if response.status_code == 201:
                print(f"  ✓ Created index: {index_name}")
                return True
            elif response.status_code == 409:
                print(f"  ℹ Index already exists: {index_name}")
                return True
            else:
                print(f"  ✗ Failed to create index {index_name}: {response.status_code}")
                return False

        except Exception as e:
            print(f"  ✗ Error creating index {index_name}: {e}")
            return False

    def create_hec_token(self):
        """Create HEC token for data loading"""
        url = f"{self.base_url}/servicesNS/admin/splunk_httpinput/data/inputs/http"
        data = {
            'name': 'course_hec',
            'index': 'web',
            'indexes': 'web,app,auth,sales,performance,api',
            'disabled': '0'
        }

        try:
            response = self.session.post(url, auth=self.auth, data=data)
            if response.status_code in [201, 409]:  # 201=created, 409=already exists
                # Extract token from response
                import re
                match = re.search(r'<s:key name="token">([a-f0-9\-]+)</s:key>', response.text)
                if match:
                    token = match.group(1)
                    print(f"  ✓ HEC token ready")
                    return token
                # If already exists, try to get existing token
                get_url = f"{url}/course_hec"
                get_response = self.session.get(get_url, auth=self.auth)
                match = re.search(r'<s:key name="token">([a-f0-9\-]+)</s:key>', get_response.text)
                if match:
                    token = match.group(1)
                    print(f"  ✓ HEC token retrieved")
                    return token
            return None
        except Exception as e:
            print(f"  ✗ Error creating HEC token: {e}")
            return None

    def parse_apache_log(self, line):
        """Parse Apache Combined Log Format into JSON fields"""
        import re
        import time

        pattern = r'^(\S+) \S+ (\S+) \[([^\]]+)\] "(\S+) (\S+) \S+" (\d+) (\d+) "([^"]*)" "([^"]*)" (\d+)ms$'
        match = re.match(pattern, line)

        if match:
            # Use current time instead of log timestamp for testing
            current_time = int(time.time())

            return {
                'src_ip': match.group(1),
                'user': match.group(2) if match.group(2) != '-' else None,
                'method': match.group(4),
                'url': match.group(5),
                'status': int(match.group(6)),
                'bytes': int(match.group(7)),
                'referer': match.group(8) if match.group(8) != '-' else None,
                'user_agent': match.group(9),
                'response_time': int(match.group(10)),
                '_time': current_time
            }
        return None

    def parse_kv_log(self, line):
        """Parse key=value log format into JSON fields"""
        import re
        import time

        # Extract timestamp first (format: 2025-10-18 04:14:34)
        timestamp_match = re.match(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(.+)$', line)
        if not timestamp_match:
            return None

        kv_part = timestamp_match.group(2)

        # Use current time instead of log timestamp for testing
        current_time = int(time.time())

        # Parse key=value pairs
        fields = {}
        # Match key=value or key="value with spaces"
        pattern = r'(\w+)=("(?:[^"\\]|\\.)*"|\S+)'
        for match in re.finditer(pattern, kv_part):
            key = match.group(1)
            value = match.group(2)
            # Remove quotes if present
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            # Convert numeric values
            if value != '-':
                try:
                    if '.' in value:
                        value = float(value)
                    else:
                        value = int(value)
                except (ValueError, TypeError):
                    pass
            fields[key] = value

        fields['_time'] = current_time
        return fields

    def parse_json_log(self, line):
        """Parse JSON log format"""
        import time
        try:
            data = json.loads(line)
            # Use current time instead of log timestamp for testing
            data['_time'] = int(time.time())
            return data
        except:
            return None

    def detect_log_format(self, filepath):
        """Detect log format from file"""
        if 'web_access' in filepath:
            return 'apache'
        elif 'api' in filepath:
            return 'json'
        else:
            return 'kv'  # key=value format

    def load_data_file(self, filepath, index, sourcetype, hec_token):
        """Load a data file into Splunk via HEC (HTTP Event Collector) as structured JSON"""
        # Use HEC event endpoint for structured data
        hec_url = f"{self.base_url.replace(':8089', ':8088')}/services/collector/event"

        # Convert to Path object for cross-platform compatibility
        filepath = Path(filepath)

        if not filepath.exists():
            print(f"  ✗ File not found: {filepath}")
            return False

        # Detect log format
        log_format = self.detect_log_format(str(filepath))

        file_size = filepath.stat().st_size
        print(f"  Loading {filepath.name} ({file_size / 1024 / 1024:.2f} MB)...")

        try:
            headers = {
                'Authorization': f'Splunk {hec_token}',
                'Content-Type': 'application/json'
            }

            # Process file in batches
            batch_size = 1000
            batch = []
            total_events = 0
            failed_parse = 0

            # Use Path.open() for cross-platform file handling
            with filepath.open('r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Parse the log line based on format
                    try:
                        if log_format == 'apache':
                            parsed = self.parse_apache_log(line)
                        elif log_format == 'json':
                            parsed = self.parse_json_log(line)
                        else:  # kv format
                            parsed = self.parse_kv_log(line)

                        if parsed:
                            event = {
                                'time': parsed.pop('_time'),
                                'index': index,
                                'sourcetype': sourcetype,
                                'host': 'course-data',
                                'event': parsed
                            }
                            batch.append(json.dumps(event))
                            total_events += 1
                        else:
                            failed_parse += 1
                    except Exception as e:
                        if failed_parse < 5:  # Only print first few errors
                            print(f"    Parse error on line: {str(e)[:100]}")
                        failed_parse += 1

                    # Send batch when it reaches batch_size
                    if len(batch) >= batch_size:
                        response = requests.post(
                            hec_url,
                            headers=headers,
                            data='\n'.join(batch),
                            verify=False,
                            timeout=60
                        )
                        if response.status_code not in [200, 201]:
                            print(f"  ✗ Batch failed: {response.status_code}")
                            return False
                        batch = []

                # Send remaining events
                if batch:
                    response = requests.post(
                        hec_url,
                        headers=headers,
                        data='\n'.join(batch),
                        verify=False,
                        timeout=60
                    )
                    if response.status_code not in [200, 201]:
                        print(f"  ✗ Final batch failed: {response.status_code}")
                        return False

            print(f"  ✓ Loaded {total_events} events from {filepath.name} to index {index}")
            if failed_parse > 0:
                print(f"    (Skipped {failed_parse} unparseable lines)")
            return True

        except Exception as e:
            print(f"  ✗ Error loading {filepath.name}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def upload_lookup(self, filepath, lookup_name):
        """Upload a lookup file to Splunk via docker cp (cross-platform)"""
        import subprocess

        # Convert to Path object for cross-platform compatibility
        filepath = Path(filepath)

        if not filepath.exists():
            print(f"  ✗ Lookup file not found: {filepath}")
            return False

        print(f"  Uploading lookup file: {lookup_name}...")

        try:
            # Copy file directly into Splunk Docker container
            container_name = "splunk-course"
            dest_path = f"/opt/splunk/etc/apps/search/lookups/{lookup_name}"

            # Use absolute path and convert to string for docker command
            source_path = str(filepath.resolve())

            # Docker cp command works on Windows, Mac, and Linux
            result = subprocess.run(
                ["docker", "cp", source_path, f"{container_name}:{dest_path}"],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print(f"  ✓ Uploaded lookup: {lookup_name}")
                return True
            else:
                print(f"  ✗ Failed to upload lookup: {result.stderr}")
                return False

        except Exception as e:
            print(f"  ✗ Error uploading lookup: {e}")
            return False

def main():
    print("=" * 70)
    print("Splunk Advanced Course - Data Loader")
    print("=" * 70)
    print()

    # Display platform information
    current_platform = platform.system()
    print(f"Platform: {current_platform}")
    print(f"Python: {platform.python_version()}")
    print(f"Data Directory: {DATA_DIR}")
    print()

    # Initialize loader
    loader = SplunkLoader(SPLUNK_HOST, SPLUNK_PORT, SPLUNK_USERNAME, SPLUNK_PASSWORD)

    # Wait for Splunk
    if not loader.wait_for_splunk():
        print("\n✗ Splunk is not ready. Please start Splunk first.")
        sys.exit(1)

    print()

    # Create indexes
    print("Creating indexes...")
    for index_config in INDEXES:
        loader.create_index(index_config["name"], index_config["datatype"])

    print()

    # Wait for indexes to be ready
    print("Waiting for indexes to initialize...")
    time.sleep(5)

    # Create HEC token
    print("\nCreating HEC token for data loading...")
    hec_token = loader.create_hec_token()
    if not hec_token:
        print("\n✗ Failed to create HEC token. Cannot load data.")
        sys.exit(1)

    # Load data files
    print("\nLoading data files...")
    success_count = 0
    fail_count = 0

    for data_file in DATA_FILES:
        # Use Path for cross-platform file path handling
        filepath = DATA_DIR / data_file["file"]
        if loader.load_data_file(filepath, data_file["index"], data_file["sourcetype"], hec_token):
            success_count += 1
        else:
            fail_count += 1

    print()

    # Upload lookup files
    print("Uploading lookup files...")
    lookup_file = DATA_DIR / "users.csv"
    if lookup_file.exists():
        loader.upload_lookup(lookup_file, "users.csv")
    else:
        print(f"  ✗ Lookup file not found: {lookup_file}")

    print()
    print("=" * 70)
    print("Data Loading Summary")
    print("=" * 70)
    print(f"Indexes created: {len(INDEXES)}")
    print(f"Data files loaded: {success_count}/{len(DATA_FILES)}")
    print(f"Failed: {fail_count}")
    print()

    if fail_count > 0:
        print("⚠ Some files failed to load. Check the errors above.")
        print()

    print("Next steps:")
    print("  1. Verify data in Splunk:")
    print("     index=* | stats count by index")
    print("  2. Run course tests:")
    print("     cd ../course_tests")
    print("     python3 run_all_tests.py")
    print("=" * 70)

    sys.exit(0 if fail_count == 0 else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nData loading cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
