import asyncio
import json
import csv
from aiohttp import ClientSession
from parsel import Selector
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from pathlib import Path

USE_KAFKA = False
SAVE_TO_CSV = True
BASE_URL = "https://мойбизнес.рф"
PAGE_URL = f"{BASE_URL}/anticrisis"

async def fetch_html(session, url):
    """Функция для получения HTML страницы."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def parse_support_measures():
    """Функция для извлечения данных о мерах поддержки."""
    result = []
    csv_file_path = Path("parsed_support_measures.csv")

    async with ClientSession() as session:
        html = await fetch_html(session, PAGE_URL)
        if not html:
            return {"error": f"Не удалось получить HTML с {PAGE_URL}"}

        selector = Selector(html)
        support_blocks = selector.css("a.support__block")

        if not support_blocks:
            return {"error": "Верстка сайта была обновлена или элементы отсутствуют"}

        for block in support_blocks:
            title = block.css("div.support__block-title::text").get()
            link = block.css("::attr(href)").get()
            description = block.css("div.support__block-description::text").get()

            if title and link and description:
                result.append({
                    "title": title.strip(),
                    "url": f"{BASE_URL}{link.strip()}",
                    "description": description.strip()
                })

    # Сохранение данных в CSV, если включено
    if SAVE_TO_CSV:
        try:
            with csv_file_path.open("w", newline='', encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["title", "url", "description"])
                writer.writeheader()
                writer.writerows(result)
            print(f"Данные сохранены в файл: {csv_file_path}")
        except Exception as e:
            print(f"Ошибка сохранения CSV: {e}")

    return result

async def process_message():
    """Обработка задачи (Kafka режим или консоль)."""
    print(f"Обработка страницы {PAGE_URL}...")
    result = await parse_support_measures()
    return result

async def kafka_processor():
    """Процессор с использованием Kafka."""
    consumer = AIOKafkaConsumer(
        'parse_tasks',
        bootstrap_servers='localhost:9093',
        group_id='business_support_parser',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9093',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    await consumer.start()
    await producer.start()

    try:
        async for message in consumer:
            print(f"Получено сообщение: {message.value}")
            result = await process_message()
            if result:
                print(f"Отправка результата: {result}")
                await producer.send_and_wait('parse_results', result)
            else:
                print("Не удалось получить данные.")
    finally:
        await consumer.stop()
        await producer.stop()

async def console_processor():
    """Процессор для вывода данных в консоль."""
    result = await process_message()
    print(f"Результат: {json.dumps(result, indent=4, ensure_ascii=False)}")

if __name__ == "__main__":
    if USE_KAFKA:
        asyncio.run(kafka_processor())
    else:
        asyncio.run(console_processor())