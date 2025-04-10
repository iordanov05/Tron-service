from fastapi import FastAPI
from app.api.endpoints import tron

app = FastAPI()

# Подключаем роуты
app.include_router(tron.router)
