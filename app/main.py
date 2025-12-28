import asyncio
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.state import state

async def monitor_system():
    print("📊 Моніторинг запущено (Redis Mode)...")
    last_time = time.time()
    last_tx_count = 0

    while True:
        await asyncio.sleep(5)

        current_time = time.time()
        current_tx_count = state.metrics.tx_processed

        try:
            q_size = await state.redis.llen("scanner_tx_queue")
        except:
            q_size = -1

        delta_time = current_time - last_time
        delta_tx = current_tx_count - last_tx_count

        instant_tps = delta_tx / delta_time if delta_time > 0 else 0
        total_elapsed = current_time - state.metrics.start_time
        avg_tps = current_tx_count / total_elapsed if total_elapsed > 0 else 0

        print(f"\n--- ⏱️ REDIS STATUS ({delta_time:.1f}s) ---")
        print(f"🚀 Speed: {instant_tps:.1f} tx/s (Avg: {avg_tps:.1f})")
        print(f"✅ Processed: {current_tx_count}")
        print(f"📚 Redis Queue: {q_size} batches")

        last_time = current_time
        last_tx_count = current_tx_count


@asynccontextmanager
async def lifespan(_: FastAPI):
    monitor_task = asyncio.create_task(monitor_system())
    print("✅ Webhook Service (Ingestion) запущено.")

    yield

    print("🛑 Зупинка сервісів...")
    monitor_task.cancel()

    await state.close()
    print("💤 З'єднання з Redis закрито.")

    try:
        await monitor_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    try:
        q_len = await state.redis.llen("scanner_tx_queue")
    except:
        q_len = "Redis unavailable"

    return {
        "queue_size": q_len,
        "metrics": state.metrics
    }