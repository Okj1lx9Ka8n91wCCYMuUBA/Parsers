import asyncio
import json
from aiohttp import ClientSession
from parsel import Selector
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

USE_KAFKA = False

BASE_URL = "https://gisp.gov.ru"
PAGE_URL_TEMPLATE = f"{BASE_URL}/nmp/main/{{page_number}}"

async def fetch_html(session, url):
    """Функция для получения HTML страницы."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def parse_measures(page_number):
    """Функция для извлечения данных о мерах поддержки с указанной страницы."""
    url = PAGE_URL_TEMPLATE.format(page_number=page_number)
    result = []

    async with ClientSession() as session:
        html = await fetch_html(session, url)
        if not html:
            return {"error": f"Не удалось получить HTML с {url}"}

        selector = Selector(html)
        measures = selector.css("li > div.catalog__list-info")

        if not measures:
            return {"error": "Верстка сайта была обновлена или элементы отсутствуют"}

        for measure in measures:
            title = measure.css("h3 a::text").get()
            link = measure.css("h3 a::attr(href)").get()
            status = measure.css("ul.tags-card li.active::text").get()
            timing = measure.css("div.catalog__list-text span::text").getall()
            
            # Обработка полей
            status = status.strip() if status else "Неактивная"
            timing = ", ".join(t.strip() for t in timing if t.strip())

            if title and link:
                result.append({
                    "title": title.strip(),
                    "url": f"{BASE_URL}{link.strip()}",
                    "status": status,
                    "timing": timing
                })

    return result

async def process_message(message):
    """Обработка сообщения из Kafka."""
    page_number = message.get("page_number")
    if not page_number:
        print("Ошибка: номер страницы отсутствует в сообщении.")
        return None

    print(f"Обработка страницы {page_number}...")
    return await parse_measures(page_number)

async def kafka_processor():
    """Процессор с использованием Kafka."""
    consumer = AIOKafkaConsumer(
        'gisp_parse_tasks',
        bootstrap_servers='localhost:9093',
        group_id='gisp_parser_group',
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
            result = await process_message(message.value)
            if result is not None:  # Если задача обработана
                print(f"Отправка результата: {result}")
                await producer.send_and_wait('parse_results', result)
            else:
                print("Сообщение пропущено.")
    finally:
        await consumer.stop()
        await producer.stop()

async def console_processor(page_number):
    """Процессор для вывода данных в консоль."""
    print(f"Обработка страницы {page_number}...")
    result = await parse_measures(page_number)
    print(f"Результат: {json.dumps(result, indent=4, ensure_ascii=False)}")

if __name__ == "__main__":
    if USE_KAFKA:
        asyncio.run(kafka_processor())
    else:
        PAGE_NUMBER = 2
        asyncio.run(console_processor(PAGE_NUMBER))