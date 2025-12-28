import asyncio
from web3 import AsyncWeb3
from web3.providers import AsyncHTTPProvider # Можна змінити на AsyncWebsocketProvider
from app.core.config import settings

class BlockchainService:
    def __init__(self, queue: asyncio.Queue):
        # Ініціалізуємо підключення до RPC (Monad / BSC)
        self.w3 = AsyncWeb3(AsyncHTTPProvider(settings.RPC_WS_URL))
        self.queue = queue
        self.last_scanned_block = None

    async def is_connected(self) -> bool:
        """Перевірка зв'язку з нодою"""
        return await self.w3.is_connected()

    async def fetch_block_worker(self):
        """
        Основний цикл (Ingestor).
        Слухає нові блоки та відправляє їх у чергу.
        """
        print("🚀 Запуск Ingestion Layer: Очікування нових блоків...")

        while True:
            try:
                # Отримуємо номер останнього блоку
                latest_block_number = await self.w3.eth.block_number

                # Якщо це перший запуск — починаємо з поточного
                if self.last_scanned_block is None:
                    self.last_scanned_block = latest_block_number - 1

                # Якщо з'явилися нові блоки
                if latest_block_number > self.last_scanned_block:
                    for block_num in range(self.last_scanned_block + 1, latest_block_number + 1):
                        # full_transactions=True дозволяє відразу отримати об'єкти, а не лише хеші
                        block = await self.w3.eth.get_block(block_num, full_transactions=True)

                        # Кладемо блок у чергу для обробки іншими частинами системи
                        await self.queue.put(block)

                        print(f"📦 Блок #{block_num} отримано. Транзакцій: {len(block.transactions)}")
                        self.last_scanned_block = block_num

                # Невелика пауза, щоб не "спамити" RPC (для Monad можна зменшити до 0.1)
                await asyncio.sleep(1)

            except Exception as e:
                print(f"❌ Помилка при отриманні блоку: {e}")
                await asyncio.sleep(2)

# --- Блок для швидкого тестування (можна запустити як окремий скрипт) ---
if __name__ == "__main__":
    async def test():
        # Створюємо локальну чергу
        test_queue = asyncio.Queue()
        # Створюємо сервіс (переконайтеся, що RPC_WS_URL у .env правильний)
        service = BlockchainService(test_queue)

        if await service.is_connected():
            print("✅ Підключено до блокчейну!")
            await service.fetch_block_worker()
        else:
            print("❌ Не вдалося підключитися. Перевірте RPC_WS_URL.")

    asyncio.run(test())