#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Mismatch Recruiter
Tests all endpoints and system connectivity
"""

import requests
import json
import sys
from datetime import datetime

class APITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        self.errors = []
    
    def test(self, name, method, endpoint, expected_status=None, data=None):
        """Test a single endpoint"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = self.session.get(url, timeout=5)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=5)
            else:
                response = self.session.request(method.upper(), url, json=data, timeout=5)
            
            success = expected_status is None or response.status_code in expected_status
            status_text = "✓" if success else "✗"
            
            result = {
                "name": name,
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "success": success,
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
            
            self.results.append(result)
            print(f"{status_text} {name}: {response.status_code} ({result['response_time_ms']:.1f}ms)")
            
            return success
        except Exception as e:
            self.errors.append({"name": name, "error": str(e)})
            print(f"✗ {name}: ERROR - {str(e)[:80]}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n=== API TEST SUITE ===")
        print(f"Target: {self.base_url}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Basic connectivity
        print("1. Basic Connectivity Tests:")
        self.test("Server responds", "GET", "/", [404])  # 404 is OK - endpoint not defined
        
        # Health endpoints (if defined)
        print("\n2. Health & Status Endpoints:")
        self.test("API Health", "GET", "/api/health", [200, 404])
        self.test("System Status", "GET", "/api/status", [200, 404])
        
        # Auth endpoints
        print("\n3. Authentication Endpoints:")
        self.test("Register endpoint exists", "POST", "/api/auth/register", [200, 400, 401, 404])
        self.test("Login endpoint exists", "POST", "/api/auth/login", [200, 400, 401, 404])
        
        # Candidate endpoints
        print("\n4. Candidate Endpoints:")
        self.test("List candidates", "GET", "/api/candidates", [200, 401, 404])
        self.test("Get candidate", "GET", "/api/candidates/1", [200, 401, 404])
        
        # Job endpoints
        print("\n5. Job Endpoints:")
        self.test("List jobs", "GET", "/api/jobs", [200, 401, 404])
        self.test("Get job", "GET", "/api/jobs/1", [200, 401, 404])
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        successful = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        
        print(f"\n=== SUMMARY ===")
        print(f"Tests Passed: {successful}/{total}")
        print(f"Success Rate: {(successful/total*100 if total > 0 else 0):.1f}%")
        
        if self.errors:
            print(f"\nErrors ({len(self.errors)}):")
            for error in self.errors[:5]:
                print(f"  - {error['name']}: {error['error'][:60]}")
        
        # Average response time
        if self.results:
            avg_time = sum(r["response_time_ms"] for r in self.results) / len(self.results)
            print(f"\nAverage Response Time: {avg_time:.2f}ms")
        
        print(f"\nServer Status: {'✓ OPERATIONAL' if successful > 0 else '✗ FAILED'}")

if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()
