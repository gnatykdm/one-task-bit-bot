import os
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv("BOT_TOKEN")

def get_token() -> str:
    return TOKEN