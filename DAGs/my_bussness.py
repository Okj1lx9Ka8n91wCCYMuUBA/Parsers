from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset
from airflow.utils.dates import days_ago
from airflow.models import Variable
import asyncio
import csv
from aiohttp import ClientSession
from parsel import Selector
import boto3

BASE_URL = "https://мойбизнес.рф"
PAGE_URL = f"{BASE_URL}/anticrisis"
S3_BUCKET_NAME = "hackava2024"
S3_KEY = "datasets/support_measures.csv"

S3_ENDPOINT = Variable.get("S3_ENDPOINT")
S3_ACCESS_KEY = Variable.get("S3_ACCESS_KEY")
S3_SECRET_KEY = Variable.get("S3_SECRET_KEY")

example_dataset = Dataset(f"s3://{S3_BUCKET_NAME}/{S3_KEY}")

async def fetch_html(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(f"Ошибка при запросе {url}: {e}")
        return ""

async def parse_support_measures():
    result = []

    async with ClientSession() as session:
        html = await fetch_html(session, PAGE_URL)
        if not html:
            return []

        selector = Selector(html)
        support_blocks = selector.css("a.support__block")

        if not support_blocks:
            return []

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

    return result

def fetch_and_save_support_measures_to_csv():
    async def main():
        result = await parse_support_measures()
        if result:
            with open("parsed_support_measures.csv", mode="w", newline='', encoding="utf-8") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["title", "url", "description"])
                writer.writeheader()
                writer.writerows(result)
    asyncio.run(main())

def upload_csv_to_s3():
    s3_client = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
    )
    s3_client.upload_file("parsed_support_measures.csv", S3_BUCKET_NAME, S3_KEY)
    print(f"Файл успешно загружен в S3: s3://{S3_BUCKET_NAME}/{S3_KEY}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "business_support_measures_producer",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["business_support", "scraping"],
) as producer_dag:

    fetch_and_save_task = PythonOperator(
        task_id="fetch_and_save_support_measures_to_csv",
        python_callable=fetch_and_save_support_measures_to_csv,
    )

    upload_to_s3_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_csv_to_s3,
        outlets=[example_dataset],
    )

    fetch_and_save_task >> upload_to_s3_task

with DAG(
    "business_support_measures_consumer",
    default_args=default_args,
    schedule=[example_dataset],
    catchup=False,
    tags=["business_support", "s3", "consume"],
) as consumer_dag:

    def process_s3_data():
        print(f"Данные доступны по адресу: s3://{S3_BUCKET_NAME}/{S3_KEY}")

    process_s3_data_task = PythonOperator(
        task_id="process_s3_data",
        python_callable=process_s3_data,
    )