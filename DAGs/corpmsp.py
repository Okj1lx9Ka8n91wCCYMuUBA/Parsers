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

S3_BUCKET_NAME = "hackava2024"
S3_KEY = "datasets/corpmsp_programs.csv"

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

async def parse_support_programs():
    base_url = "https://fasie.ru/programs/"
    result = []

    async with ClientSession() as session:
        html = await fetch_html(session, base_url)
        if not html:
            return []

        selector = Selector(html)
        program_list = selector.css("ul.programms_list li")

        if not program_list:
            return []

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

def fetch_and_save_programs_to_csv():
    async def main():
        result = await parse_support_programs()
        if result:
            with open("programs.csv", mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["title", "url", "description"])
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
    s3_client.upload_file("programs.csv", S3_BUCKET_NAME, S3_KEY)
    print(f"Файл успешно загружен в S3: s3://{S3_BUCKET_NAME}/{S3_KEY}")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "corpmsp_programs_producer",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["corpmsp", "scraping"],
) as producer_dag:

    fetch_and_save_task = PythonOperator(
        task_id="fetch_and_save_programs_to_csv",
        python_callable=fetch_and_save_programs_to_csv,
    )

    upload_to_s3_task = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_csv_to_s3,
        outlets=[example_dataset],
    )

    fetch_and_save_task >> upload_to_s3_task

with DAG(
    "corpmsp_programs_consumer",
    default_args=default_args,
    schedule=[example_dataset],
    catchup=False,
    tags=["corpmsp", "s3", "consume"],
) as consumer_dag:

    def process_s3_data():
        print(f"Данные доступны по адресу: s3://{S3_BUCKET_NAME}/{S3_KEY}")

    process_s3_data_task = PythonOperator(
        task_id="process_s3_data",
        python_callable=process_s3_data,
    )