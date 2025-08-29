# config.py
import os
import logging
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from dataclasses import dataclass

load_dotenv()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

TOKEN: str = os.getenv("BOT_TOKEN")
DB_URL: str = os.getenv("DATABASE_URL")
OPENAI_KEY = os.getenv("OPEN_AI_KEY")

engine = create_async_engine(DB_URL, echo=False)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

def get_token() -> str:
    return TOKEN

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@dataclass
class SmtpData:
    smtp_user: str = os.getenv("SMTP_USER")
    smtp_password: str = os.getenv("SMTP_PASSWORD")
    smtp_host: str = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT"))
    smtp_ssl: bool = os.getenv("SMTP_SSL") == "True"
    smtp_tsl: bool = os.getenv("SMTP_TLS") == "True"
    smtp_from: str = os.getenv("SMTP_USER")
    smtp_receiver: str = os.getenv("SMTP_MESSAGE_RECEIVER")
    smtp_subject: str = os.getenv("SMTP_MESSAGE_SUBJECT")


@dataclass
class AnotherConfig:
    CHANNEL_NAME: str = os.getenv("CHANNEL_NAME")

def get_smtp_data() -> SmtpData:
    return SmtpData()

def get_openai_key() -> str:
    return OPENAI_KEY