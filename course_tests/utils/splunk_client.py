#!/usr/bin/env python3
"""
Splunk API Client for Course Testing
Provides interface to execute searches and validate results
"""

import requests
import time
import json
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin


class SplunkClient:
    """Client for interacting with Splunk REST API"""

    def __init__(self, host: str = "localhost", port: int = 8089,
                 username: str = "admin", password: str = "changeme"):
        """
        Initialize Splunk client

        Args:
            host: Splunk server hostname
            port: Splunk management port (default 8089)
            username: Splunk username
            password: Splunk password
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_url = f"https://{host}:{port}"
        self.session_key = None
        self.session = requests.Session()
        self.session.verify = False  # Disable SSL verification for testing

    def login(self) -> bool:
        """
        Authenticate with Splunk and get session key

        Returns:
            True if login successful, False otherwise
        """
        url = urljoin(self.base_url, "/services/auth/login")
        data = {
            "username": self.username,
            "password": self.password
        }

        try:
            response = self.session.post(url, data=data, verify=False, timeout=30)

            if response.status_code != 200:
                print(f"Login failed with status code: {response.status_code}")
                print(f"Response: {response.text[:200]}")
                return False

            # Parse XML response to get session key
            root = ET.fromstring(response.text)
            # Try with namespace first, then without
            session_key = root.find(".//{http://dev.splunk.com/ns/rest}sessionKey")
            if session_key is None:
                session_key = root.find(".//sessionKey")

            if session_key is not None:
                self.session_key = session_key.text
                self.session.headers.update({
                    "Authorization": f"Splunk {self.session_key}"
                })
                return True

            print("Login failed: No session key in response")
            return False

        except Exception as e:
            print(f"Login failed with exception: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return False

    def create_search(self, query: str, earliest_time: str = "-24h",
                     latest_time: str = "now") -> Optional[str]:
        """
        Create a search job

        Args:
            query: SPL search query
            earliest_time: Earliest time for search
            latest_time: Latest time for search

        Returns:
            Search job ID (sid) if successful, None otherwise
        """
        # Ensure query starts with search or generating command
        if not query.strip().startswith(("search", "|", "Search", "SEARCH")):
            query = f"search {query}"

        # Add index=* if no index is specified (to search all custom indexes)
        # Don't add if it's a generating command (starts with |) or already has index=
        query_lower = query.lower()
        if not query_lower.startswith("|") and "index=" not in query_lower and "| inputlookup" not in query_lower:
            # Insert index=* after 'search' keyword
            if query_lower.startswith("search "):
                query = query[:7] + "index=* " + query[7:]

        url = urljoin(self.base_url, "/services/search/jobs")
        data = {
            "search": query,
            "earliest_time": earliest_time,
            "latest_time": latest_time,
            "output_mode": "json"
        }

        try:
            response = self.session.post(url, data=data)
            response.raise_for_status()

            result = response.json()
            return result.get("sid")

        except Exception as e:
            print(f"Failed to create search: {e}")
            return None

    def wait_for_job(self, sid: str, timeout: int = 300) -> bool:
        """
        Wait for search job to complete

        Args:
            sid: Search job ID
            timeout: Maximum time to wait in seconds

        Returns:
            True if job completed successfully, False otherwise
        """
        url = urljoin(self.base_url, f"/services/search/jobs/{sid}")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = self.session.get(url, params={"output_mode": "json"})
                response.raise_for_status()

                result = response.json()
                entry = result.get("entry", [{}])[0]
                content = entry.get("content", {})

                dispatch_state = content.get("dispatchState")
                is_done = content.get("isDone", False)

                if dispatch_state == "DONE" or is_done:
                    return True
                elif dispatch_state == "FAILED":
                    return False

                time.sleep(1)

            except Exception as e:
                print(f"Error checking job status: {e}")
                return False

        print(f"Job {sid} timed out after {timeout} seconds")
        return False

    def get_results(self, sid: str, count: int = 0) -> List[Dict[str, Any]]:
        """
        Get search results

        Args:
            sid: Search job ID
            count: Maximum number of results (0 = all)

        Returns:
            List of result dictionaries
        """
        url = urljoin(self.base_url, f"/services/search/jobs/{sid}/results")
        params = {
            "output_mode": "json",
            "count": count
        }

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()

            result = response.json()
            return result.get("results", [])

        except Exception as e:
            print(f"Failed to get results: {e}")
            return []

    def execute_search(self, query: str, earliest_time: str = "-24h",
                      latest_time: str = "now", timeout: int = 300) -> Dict[str, Any]:
        """
        Execute a search and return results

        Args:
            query: SPL search query
            earliest_time: Earliest time for search
            latest_time: Latest time for search
            timeout: Maximum time to wait for results

        Returns:
            Dictionary with 'success', 'results', and 'count' keys
        """
        if not self.session_key:
            if not self.login():
                return {"success": False, "error": "Login failed", "results": [], "count": 0}

        # Create search job
        sid = self.create_search(query, earliest_time, latest_time)
        if not sid:
            return {"success": False, "error": "Failed to create search", "results": [], "count": 0}

        # Wait for job to complete
        if not self.wait_for_job(sid, timeout):
            return {"success": False, "error": "Search job failed or timed out", "results": [], "count": 0}

        # Get results
        results = self.get_results(sid)

        return {
            "success": True,
            "sid": sid,
            "results": results,
            "count": len(results)
        }

    def check_index_data(self, index: str) -> Dict[str, Any]:
        """
        Check if an index has data

        Args:
            index: Index name

        Returns:
            Dictionary with index statistics
        """
        query = f"search index={index} | stats count"
        result = self.execute_search(query, earliest_time="0")

        if result["success"] and result["count"] > 0:
            count = int(result["results"][0].get("count", 0))
            return {
                "exists": True,
                "has_data": count > 0,
                "event_count": count
            }

        return {
            "exists": False,
            "has_data": False,
            "event_count": 0
        }

    def check_lookup(self, lookup_name: str) -> Dict[str, Any]:
        """
        Check if a lookup file exists and has data

        Args:
            lookup_name: Lookup file name

        Returns:
            Dictionary with lookup statistics
        """
        query = f"| inputlookup {lookup_name} | stats count"
        result = self.execute_search(query)

        if result["success"] and result["count"] > 0:
            count = int(result["results"][0].get("count", 0))
            return {
                "exists": True,
                "has_data": count > 0,
                "row_count": count
            }

        return {
            "exists": False,
            "has_data": False,
            "row_count": 0
        }

    def get_search_job_info(self, sid: str) -> Dict[str, Any]:
        """
        Get detailed information about a search job

        Args:
            sid: Search job ID

        Returns:
            Dictionary with job information
        """
        url = urljoin(self.base_url, f"/services/search/jobs/{sid}")

        try:
            response = self.session.get(url, params={"output_mode": "json"})
            response.raise_for_status()

            result = response.json()
            entry = result.get("entry", [{}])[0]
            content = entry.get("content", {})

            return {
                "success": True,
                "dispatch_state": content.get("dispatchState"),
                "is_done": content.get("isDone"),
                "is_failed": content.get("isFailed"),
                "result_count": content.get("resultCount", 0),
                "scan_count": content.get("scanCount", 0),
                "run_duration": content.get("runDuration", 0)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
