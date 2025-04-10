import os
from dotenv import load_dotenv

def pytest_configure():
    # Загрузим .env.test перед выполнением тестов
    load_dotenv(".env.test")
