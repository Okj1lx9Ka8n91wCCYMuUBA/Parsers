from fastapi import FastAPI
from src.parser import find_inn
import asyncio

app = FastAPI()

@app.get("/")
async def root(inn: str):
    """
    Аргументы:
    - inn (str): Тип инн для парсинга.
    """
    try:
        result = await find_inn(inn)
        return {
            "message": "Парсинг завершен!",
            "asked" : inn,
            "data": result,
        }
    except Exception as e:
        return {"message": "Ошибка парсинга", "error": str(e)}
