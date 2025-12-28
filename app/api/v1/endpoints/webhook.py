from fastapi import APIRouter, Response
from typing import Union
import asyncio
from app.schemas.transaction import QNPayload, PingPayload

router = APIRouter()

# Це наша "пуповина" між FastAPI та Processor
data_queue = asyncio.Queue()

@router.post("/webhook")
async def quicknode_webhook(payload: Union[QNPayload, PingPayload]):
    if isinstance(payload, PingPayload):
        return Response(content="PONG", status_code=200)

    # Додаємо транзакції в чергу
    count = 0
    for block_transactions in payload.data:
        for tx in block_transactions:
            await data_queue.put(tx)
            count += 1

    print(f"📥 [BSC] Отримано блок {payload.metadata.batch_start_range}: {count} транзакцій додано в чергу.")
    return Response(status_code=200)