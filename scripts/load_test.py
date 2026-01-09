#!/usr/bin/env python3
import concurrent.futures
import time
import requests
from statistics import mean, stdev

class LoadTester:
    def __init__(self, base_url="http://localhost:5000", num_workers=5, num_requests=20):
        self.base_url = base_url
        self.num_workers = num_workers
        self.num_requests = num_requests
        self.results = []
        self.session = requests.Session()
        
    def test_endpoint(self, method: str, endpoint: str, data: dict = None):
        try:
            url = f"{self.base_url}{endpoint}"
            start_time = time.time()
            
            if method.upper() == "GET":
                response = self.session.get(url, timeout=5)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=5)
            else:
                return {"error": f"Unsupported method: {method}", "status_code": 0}
            
            elapsed = (time.time() - start_time) * 1000
            
            return {
                "status_code": response.status_code,
                "elapsed_ms": elapsed,
                "success": 200 <= response.status_code < 300,
                "response_size": len(response.content)
            }
        except Exception as e:
            return {
                "status_code": 0,
                "elapsed_ms": 0,
                "success": False,
                "error": str(e)
            }
    
    def run_load_test(self, method: str, endpoint: str):
        print(f"\nTesting: {method} {self.base_url}{endpoint}")
        print(f"Workers: {self.num_workers}, Requests: {self.num_requests}")
        print("-" * 50)
        
        self.results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(self.test_endpoint, method, endpoint) 
                      for _ in range(self.num_workers * self.num_requests)]
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                self.results.append(result)
                if (i + 1) % 10 == 0:
                    print(f"Completed: {i + 1}/{self.num_workers * self.num_requests}")
        
        self.print_results()
    
    def print_results(self):
        print("\n" + "="*50)
        successful = [r for r in self.results if r.get("success", False)]
        failed = [r for r in self.results if not r.get("success", False)]
        response_times = [r["elapsed_ms"] for r in successful]
        
        print(f"Total: {len(self.results)} | Success: {len(successful)} | Failed: {len(failed)}")
        
        if response_times:
            print(f"Response Time: Min={min(response_times):.1f}ms, Max={max(response_times):.1f}ms, Avg={mean(response_times):.1f}ms")
        
        if failed:
            errors = [r.get("error", "unknown") for r in failed[:3]]
            print(f"Errors: {errors}")
        print("="*50)

if __name__ == "__main__":
    tester = LoadTester()
    print("Starting Load Test")
    print(f"Target: {tester.base_url}")
    tester.run_load_test("GET", "/")
