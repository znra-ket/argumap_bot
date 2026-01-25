from os import getenv
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
DATABASE = getenv("DATABASE")

if not TOKEN:
    raise ValueError("нет токена")

if not DATABASE:
    raise ValueError("Нет бд")