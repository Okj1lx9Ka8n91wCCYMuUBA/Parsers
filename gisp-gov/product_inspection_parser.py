import aiohttp
import asyncio
import csv
import os
from parsel import Selector

INPUT_CSV = "parsed_data.csv"
OUTPUT_FOLDER = "products_content"
MAX_CONCURRENT_REQUESTS = 10
RETRY_COUNT = 3
RETRY_DELAY = 1

async def fetch_html(url, session, retries=RETRY_COUNT):
    """Загрузка HTML с повторными попытками."""
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Ошибка {response.status} при запросе {url}")
        except Exception as e:
            print(f"Ошибка подключения к {url}: {e}")
        

        if attempt < retries - 1:
            await asyncio.sleep(RETRY_DELAY)
    
    print(f"Не удалось загрузить страницу {url} после {retries} попыток")
    return None

def parse_info(html):
    """Парсинг HTML для извлечения содержимого div.info__wrapper."""
    selector = Selector(html)
    info_div = selector.css("div.info__wrapper").get()
    if info_div:
        text_content = Selector(info_div).xpath("//text()").getall()
        cleaned_text = "\n".join(line.strip() for line in text_content if line.strip())
        return cleaned_text
    else:
        return None

async def process_row(index, url, session, semaphore):
    """Обработка одной строки CSV с использованием семафора."""
    async with semaphore:
        print(f"Обработка {index}: {url}")
        html = await fetch_html(url, session)
        if html:
            content = parse_info(html)
            if content:
                filename = os.path.join(OUTPUT_FOLDER, f"{index}.txt")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Файл {filename} успешно сохранен.")
            else:
                print(f"Не удалось извлечь содержимое для {url}")
        else:
            print(f"Не удалось загрузить страницу {url}")

async def process_csv(input_csv):
    """Чтение CSV и обработка всех строк с контролем числа запросов."""
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        tasks = []
        with open(input_csv, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for index, row in enumerate(reader, start=1):
                url = row["url"]
                tasks.append(process_row(index, url, session, semaphore))
        
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(process_csv(INPUT_CSV))