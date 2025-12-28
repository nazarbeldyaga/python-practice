import asyncio
from decimal import Decimal
from app.api.v1.endpoints.webhook import data_queue

def hex_to_dec(hex_str: str, decimals: int = 18) -> Decimal:
    """Конвертує Hex Wei у Decimal BNB/MON"""
    if not hex_str or hex_str == "0x":
        return Decimal(0)
    # Перетворюємо Hex у ціле число (int), потім ділимо на 10^18
    return Decimal(int(hex_str, 16)) / Decimal(10**decimals)

async def transaction_processor():
    """
    Постійний цикл обробки транзакцій з черги.
    """
    print("⚙️  Processor запрацював: Очікування транзакцій з черги...")

    while True:
        # Чекаємо на нову транзакцію
        tx = await data_queue.get()

        try:
            # Конвертуємо суму (Value)
            amount = hex_to_dec(tx.value)

            # Визначаємо тип дії
            if tx.input == "0x":
                action = "💰 Прямий переказ"
            else:
                # Беремо перші 10 символів (Method ID)
                action = f"📝 Контракт ({tx.input[:10]})"

            # Фільтруємо "цікаві" транзакції (наприклад, більше 0.1 BNB)
            if amount > 0.1:
                print(f"{action} | {amount:.4f} BNB | Від: {tx.from_address[:10]}... | Hash: {tx.hash[:10]}...")

        except Exception as e:
            print(f"⚠️ Помилка обробки транзакції {tx.hash}: {e}")
        finally:
            # Кажемо черзі, що завдання виконано
            data_queue.task_done()