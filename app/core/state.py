import time
from dataclasses import dataclass
import redis.asyncio as redis

@dataclass
class AppMetrics:
    blocks_received: int = 0
    tx_received: int = 0
    tx_processed: int = 0
    start_time: float = time.time()

class AppState:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)
        self.metrics = AppMetrics()

    async def close(self):
        await self.redis.aclose()

state = AppState()