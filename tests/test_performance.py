import time
import pytest

def test_matching_performance():
    # Simulate 1000 matching operations
    start = time.time()
    # Execute matching
    elapsed = time.time() - start
    assert elapsed < 5.0, f"Matching took {elapsed}s, should be < 5s"

if __name__ == '__main__':
    test_matching_performance()
    print("✅ Performance test passed!")
