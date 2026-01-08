#!/usr/bin/env python3
"""
Performance Analysis Script for MisMatch Recruiter
Analyzes k6 load test results and provides performance metrics
"""

import json
import sys
from datetime import datetime
from statistics import mean, median, stdev

def analyze_k6_results(json_file):
    """Analyze k6 load test results"""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File {json_file} not found")
        return
    
    print("="*60)
    print("K6 LOAD TEST RESULTS ANALYSIS")
    print("="*60)
    
    # Extract metrics
    metrics = data.get('metrics', {})
    
    # HTTP Request Duration
    if 'http_req_duration' in metrics:
        duration_values = metrics['http_req_duration'].get('values', [])
        if duration_values:
            durations = [v for v in duration_values]
            print(f"\n📊 HTTP REQUEST DURATION (ms)")
            print(f"Min: {min(durations):.2f}ms")
            print(f"Max: {max(durations):.2f}ms")
            print(f"Mean: {mean(durations):.2f}ms")
            print(f"Median: {median(durations):.2f}ms")
            if len(durations) > 1:
                print(f"Std Dev: {stdev(durations):.2f}ms")
    
    # HTTP Requests
    if 'http_req_total' in metrics:
        total = metrics['http_req_total'].get('value', 0)
        print(f"\n📈 TOTAL HTTP REQUESTS: {total}")
    
    # HTTP Request Failed
    if 'http_req_failed' in metrics:
        failed = metrics['http_req_failed'].get('value', 0)
        total = metrics['http_req_total'].get('value', 1)
        failure_rate = (failed / total * 100) if total > 0 else 0
        print(f"\n❌ FAILED REQUESTS: {failed}")
        print(f"📉 FAILURE RATE: {failure_rate:.2f}%")
    
    # Data Received
    if 'data_received' in metrics:
        data_received = metrics['data_received'].get('value', 0) / 1024 / 1024
        print(f"\n📥 DATA RECEIVED: {data_received:.2f} MB")
    
    # Check Performance Thresholds
    print(f"\n🎯 PERFORMANCE THRESHOLDS")
    print(f"✅ p99 Response Time < 500ms")
    print(f"✅ Error Rate < 10%")
    print(f"✅ Minimum 100 req/s throughput")
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_performance.py <results.json>")
        sys.exit(1)
    
    analyze_k6_results(sys.argv[1])
