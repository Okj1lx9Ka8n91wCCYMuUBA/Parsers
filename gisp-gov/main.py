import asyncio
import csv
from aiohttp import ClientSession
from parsel import Selector

USE_KAFKA = False
BASE_URL = "https://gisp.gov.ru"
PAGE_URL_TEMPLATE = f"{BASE_URL}/nmp/main/{{page_number}}"
MAX_CONCURRENT_REQUESTS = 10  # Максимальное число одновременных запросов

async def fetch_html(session, url):
    """Функция для получения HTML страницы."""
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def parse_measures(page_number, session):
    """Функция для извлечения данных о мерах поддержки с указанной страницы."""
    url = PAGE_URL_TEMPLATE.format(page_number=page_number)
    result = []

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

async def save_to_csv(data, filename="parsed_data.csv"):
    """Функция для сохранения данных в CSV файл."""
    keys = ["title", "url", "status", "timing"]
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

async def process_page(page_number, session, semaphore):
    """Обработка одной страницы с использованием семафора."""
    async with semaphore:
        print(f"Обработка страницы {page_number}...")
        result = await parse_measures(page_number, session)

        if isinstance(result, dict) and "error" in result:
            print(f"Ошибка: {result['error']}")
            return []

        print(f"Обработано {len(result)} записей с страницы {page_number}.")
        return result

async def parallel_processor(start_page, end_page, should_save_to_csv=False):
    """Параллельная обработка страниц."""
    all_data = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with ClientSession() as session:
        tasks = [
            process_page(page_number, session, semaphore)
            for page_number in range(start_page, end_page + 1)
        ]
        results = await asyncio.gather(*tasks)

    # Собираем результаты
    for result in results:
        all_data.extend(result)

    if should_save_to_csv and all_data:
        await save_to_csv(all_data)
        print(f"Данные сохранены в файл 'parsed_data.csv'.")

if __name__ == "__main__":
    SAVE_TO_CSV = True
    START_PAGE = 1
    END_PAGE = 250  # Задайте конечную страницу

    if USE_KAFKA:
        # Заглушка для Kafka, если потребуется в будущем
        print("Kafka обработка не реализована.")
    else:
        asyncio.run(parallel_processor(START_PAGE, END_PAGE, should_save_to_csv=SAVE_TO_CSV))