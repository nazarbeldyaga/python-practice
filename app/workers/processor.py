import asyncio
import json
from app.core.state import state
from app.schemas.transaction import QNPayload

QUEUE_NAME = "scanner_tx_queue"

async def transaction_processor():
    print(f"⚙️  Redis-Processor підключено до черги '{QUEUE_NAME}'")

    while True:
        try:
            result = await state.redis.blpop(QUEUE_NAME, timeout=0)

            if not result:
                continue

            _, raw_body = result

            try:
                json_data = json.loads(raw_body)
                payload = QNPayload(**json_data)

                tx_count = sum(len(block) for block in payload.data)

                state.metrics.tx_processed += tx_count

            except Exception as e:
                print(f"⚠️ Помилка парсингу: {e}")

        except Exception as e:
            print(f"🔥 Помилка з'єднання з Redis: {e}")
            await asyncio.sleep(5)