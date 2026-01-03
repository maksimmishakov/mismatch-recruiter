from typing import List, Callable, Any
import time

class QueueProcessor:
    def __init__(self, batch_size: int = 50):
        self.batch_size = batch_size
        self.queue: List[Any] = []
    
    def add(self, item: Any) -> None:
        self.queue.append(item)
    
    def process_batch(self, processor: Callable) -> List[Any]:
        results = []
        for i in range(0, len(self.queue), self.batch_size):
            batch = self.queue[i:i + self.batch_size]
            batch_results = [processor(item) for item in batch]
            results.extend(batch_results)
            time.sleep(0.1)  # Prevent overwhelming
        self.queue.clear()
        return results

if __name__ == '__main__':
    processor = QueueProcessor(batch_size=10)
    for i in range(25):
        processor.add(f"item_{i}")
    results = processor.process_batch(lambda x: f"processed_{x}")
    print(f"Processed {len(results)} items")
