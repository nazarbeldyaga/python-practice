import asyncio
import aiohttp
import time

async def fetch_url(session, url, i):
    """Функція для одного запиту"""
    async with session.get(url) as response:
        # Чекаємо на тіло відповіді (це теж I/O операція)
        status = response.status
        # Уявно читаємо дані
        data = await response.text()
        print(f"Запит №{i} завершено зі статусом: {status}")
        return len(data)

async def main():
    urls = ["https://httpbin.org/delay/1"] * 10  # 10 запитів до API з затримкою 1с

    start_time = time.perf_counter()

    # Створюємо одну сесію для всіх запитів (це важливо для швидкості!)
    async with aiohttp.ClientSession() as session:
        # Створюємо список завдань (корутин)
        tasks = []
        for i in range(len(urls)):
            # Ми НЕ пишемо await тут, ми просто створюємо об'єкти корутин
            tasks.append(fetch_url(session, urls[i], i))

        # asyncio.gather запускає всі корутини паралельно і чекає на їх завершення
        # Це і є момент "магії" асинхронності
        results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()

    print(f"---")
    print(f"Всього отримано байт: {sum(results)}")
    print(f"Час виконання: {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    # Запуск асинхронного циклу подій
    asyncio.run(main())