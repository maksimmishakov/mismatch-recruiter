import asyncio
from typing import Callable, Any, List

class AsyncProcessor:
    @staticmethod
    async def process_batch(items: List[Any], func: Callable) -> List[Any]:
        tasks = [func(item) for item in items]
        return await asyncio.gather(*tasks)
