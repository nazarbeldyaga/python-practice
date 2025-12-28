import asyncio
import sys
import os

sys.path.append(os.getcwd())

from app.workers.processor import transaction_processor

if __name__ == "__main__":
    try:
        print("🚀 Запуск окремого процесу Worker...")
        asyncio.run(transaction_processor())
    except KeyboardInterrupt:
        print("🛑 Worker зупинено.")