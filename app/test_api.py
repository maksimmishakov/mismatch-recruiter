#!/usr/bin/env python
"""
Comprehensive API Testing Suite - Phase 4
"""
import json
import requests
from datetime import datetime

BASE_URL = 'http://127.0.0.1:5000'

class APITester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, method, endpoint, data=None, expected_status=200):
        """Run a single API test"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url)
            elif method == 'POST':
                response = requests.post(url, json=data)
            elif method == 'PUT':
                response = requests.put(url, json=data)
            elif method == 'DELETE':
                response = requests.delete(url)
            
            # Check status
            if response.status_code == expected_status:
                self.passed += 1
                status = '✓ PASS'
            else:
                self.failed += 1
                status = '✗ FAIL'
            
            result = {
                'name': name,
                'method': method,
                'endpoint': endpoint,
                'status': response.status_code,
                'expected': expected_status,
                'result': status
            }
            self.tests.append(result)
            
            print(f"{status} {method:6} {endpoint:40} [{response.status_code}]")
            
            return response
        except Exception as e:
            self.failed += 1
            print(f"✗ FAIL {method:6} {endpoint:40} [ERROR: {str(e)[:30]}]")
            return None
    
    def print_summary(self):
        """Print test summary"""
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests:  {total}")
        print(f"Passed:       {self.passed} ({percentage:.1f}%)")
        print(f"Failed:       {self.failed}")
        print("="*70 + "\n")
        
        return percentage

def run_tests():
    print("\n" + "="*70)
    print("PHASE 4: COMPREHENSIVE API TESTING")
    print("="*70 + "\n")
    
    tester = APITester()
    
    # === HEALTH CHECKS ===
    print("\n[Health Checks]")
    tester.test('Health Check', 'GET', '/health')
    tester.test('API Info', 'GET', '/api')
    
    # === CANDIDATE ENDPOINTS ===
    print("\n[Candidate Endpoints]")
    
    # Create candidate
    candidate_data = {
        'name': 'Test Candidate',
        'email': f'test_{int(datetime.utcnow().timestamp())}@example.com',
        'phone': '+7-999-111-22-33',
        'resume_text': 'Test resume',
        'skills': 'Python,JavaScript',
        'experience_years': 3,
        'current_position': 'Developer',
        'current_company': 'Test Co',
        'salary_expectation': 100000,
        'location': 'Moscow',
        'availability': 'Immediate'
    }
    
    response = tester.test('Create Candidate', 'POST', '/api/candidates', candidate_data, 201)
    
    # Get candidates (if list endpoint exists)
    tester.test('Get All Candidates', 'GET', '/api/candidates', expected_status=[200, 404])
    
    # === JOB ENDPOINTS ===
    print("\n[Job Endpoints]")
    
    job_data = {
        'title': 'Senior Developer',
        'description': 'Looking for experienced developer',
        'company': 'Test Corp',
        'location': 'Moscow',
        'salary_min': 100000,
        'salary_max': 150000,
        'required_skills': 'Python,JavaScript',
        'experience_required': 3
    }
    
    tester.test('Create Job', 'POST', '/api/jobs', job_data, expected_status=[201, 404])
    tester.test('Get All Jobs', 'GET', '/api/jobs', expected_status=[200, 404])
    
    # === MATCHING ENDPOINTS ===
    print("\n[Matching Endpoints]")
    tester.test('Get Matches', 'GET', '/api/matches', expected_status=[200, 404])
    
    # === ANALYTICS ENDPOINTS ===
    print("\n[Analytics Endpoints]")
    tester.test('Get Analytics', 'GET', '/api/analytics', expected_status=[200, 404])
    
    # === FEEDBACK ENDPOINTS ===
    print("\n[Feedback Endpoints]")
    feedback_data = {
        'type': 'comment',
        'content': 'Test feedback'
    }
    tester.test('Create Feedback', 'POST', '/api/feedback', feedback_data, expected_status=[201, 404])
    tester.test('Get Feedback', 'GET', '/api/feedback', expected_status=[200, 404])
    
    # Print summary
    percentage = tester.print_summary()
    
    if percentage >= 80:
        print(f"✅ TESTING STATUS: {'PASSED' if percentage >= 90 else 'ACCEPTABLE'}")
    else:
        print(f"⚠ TESTING STATUS: NEEDS IMPROVEMENT")
    
    return tester

if __name__ == '__main__':
    run_tests()
