# Парсер Корпорация МСП corpmsp.ru

import asyncio
import json
from aiohttp import ClientSession
from parsel import Selector

USE_KAFKA = False

async def fetch_html(session, url):
    """Функция для получения HTML страницы."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def parse_support_programs():
    """Функция для извлечения актуальных мер поддержки бизнеса."""
    base_url = "https://fasie.ru/programs/"
    result = []

    async with ClientSession() as session:
        html = await fetch_html(session, base_url)
        if not html:
            return {"error": "Не удалось получить HTML"}

        selector = Selector(html)
        program_list = selector.css("ul.programms_list li")

        if not program_list:
            return {"error": "Верстка сайта была обновлена или элементы отсутствуют"}

        for program in program_list:
            title = program.css("h4::text").get()
            url = program.css("a::attr(href)").get()
            description = program.css("p::text").get()

            if title and url and description:
                result.append({
                    "title": title.strip(),
                    "url": f"https://fasie.ru{url.strip()}",
                    "description": description.strip()
                })

    return result

async def process_message(message):
    resource = message.get('resource', '')
    if resource != 'corpmsp':
        print(f"Сообщение игнорируется, так как resource='{resource}'")
        return None
    
    print(f"Обработка задачи для ресурса: {resource}")
    return await parse_support_programs()

async def kafka_processor():
    """Процессор с использованием Kafka."""
    from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

    consumer = AIOKafkaConsumer(
        'upd_parse_tasks',
        bootstrap_servers='localhost:9093',
        group_id='flipped_processor_group',
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

async def console_processor():
    """Процессор без использования Kafka."""
    print("Начало обработки...")
    result = await parse_support_programs()
    print(f"Результат: {json.dumps(result, indent=4, ensure_ascii=False)}")

if __name__ == "__main__":
    if USE_KAFKA:
        asyncio.run(kafka_processor())
    else:
        asyncio.run(console_processor())