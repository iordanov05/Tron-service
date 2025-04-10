import os
from dotenv import load_dotenv

load_dotenv()  # загружаем переменные из .env

TRON_NODE_URL = os.getenv("TRON_NODE_URL", None)  # Если None, то используем default в Tron()
