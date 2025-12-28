from fastapi import APIRouter, Response, Request
from app.core.state import state
import json

router = APIRouter()
QUEUE_NAME = "scanner_tx_queue"

@router.post("/webhook")
async def quicknode_webhook(request: Request):
    body_bytes = await request.body()

    if len(body_bytes) < 150:
        try:
            data = json.loads(body_bytes)
            if data.get("message") == "PING":
                return Response(content="PONG", status_code=200)
        except:
            pass

    await state.redis.rpush(QUEUE_NAME, body_bytes)

    state.metrics.blocks_received += 1

    return Response(status_code=200)