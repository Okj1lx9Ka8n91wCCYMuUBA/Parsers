from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset
from airflow.utils.dates import days_ago
from airflow.models import Variable
import asyncio
import csv
from aiohttp import ClientSession
from parsel import Selector
import os
import boto3

BASE_URL = "https://gisp.gov.ru"
PAGE_URL_TEMPLATE = f"{BASE_URL}/nmp/main/{{page_number}}"
MAX_CONCURRENT_REQUESTS = 10
INPUT_CSV = "parsed_data.csv"
OUTPUT_FOLDER = "products_content"
S3_BUCKET_NAME = "hackava2024"
S3_KEY = "datasets/gisp_data.csv"

S3_ENDPOINT = Variable.get("S3_ENDPOINT")
S3_ACCESS_KEY = Variable.get("S3_ACCESS_KEY")
S3_SECRET_KEY = Variable.get("S3_SECRET_KEY")

example_dataset = Dataset(f"s3://{S3_BUCKET_NAME}/{S3_KEY}")

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        return ""

async def parse_measures(page_number, session):
    url = PAGE_URL_TEMPLATE.format(page_number=page_number)
    result = []
    html = await fetch_html(session, url)
    if not html:
        return []
    selector = Selector(html)
    measures = selector.css("li > div.catalog__list-info")
    for measure in measures:
        title = measure.css("h3 a::text").get()
        link = measure.css("h3 a::attr(href)").get()
        status = measure.css("ul.tags-card li.active::text").get()
        timing = measure.css("div.catalog__list-text span::text").getall()
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

async def process_page(page_number, semaphore, session):
    async with semaphore:
        return await parse_measures(page_number, session)

def extract_pages_to_csv(start_page, end_page):
    async def main():
        semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        async with ClientSession() as session:
            tasks = [
                process_page(page_number, semaphore, session)
                for page_number in range(start_page, end_page + 1)
            ]
            results = await asyncio.gather(*tasks)
        all_data = [item for sublist in results for item in sublist]
        if all_data:
            keys = ["title", "url", "status", "timing"]
            with open(INPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=keys)
                writer.writeheader()
                writer.writerows(all_data)
    asyncio.run(main())

def upload_csv_to_s3():
    s3_client = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
    )
    s3_client.upload_file(INPUT_CSV, S3_BUCKET_NAME, S3_KEY)
    print(f"Файл {INPUT_CSV} успешно загружен в S3: s3://{S3_BUCKET_NAME}/{S3_KEY}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "gisp_data_producer",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["gisp", "scraping"],
) as producer_dag:

    extract_pages_task = PythonOperator(
        task_id="extract_pages_to_csv",
        python_callable=extract_pages_to_csv,
        op_kwargs={
            "start_page": 1,
            "end_page": 250,
        },
    )

    upload_to_s3_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_csv_to_s3,
        outlets=[example_dataset],
    )

    extract_pages_task >> upload_to_s3_task

with DAG(
    "gisp_data_consumer",
    default_args=default_args,
    schedule=[example_dataset],
    catchup=False,
    tags=["gisp", "s3", "consume"],
) as consumer_dag:

    def process_s3_data():
        print(f"Данные доступны по адресу: s3://{S3_BUCKET_NAME}/{S3_KEY}")

    process_s3_data_task = PythonOperator(
        task_id="process_s3_data",
        python_callable=process_s3_data,
    )