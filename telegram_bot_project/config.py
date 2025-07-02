import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

load_dotenv()

TOKEN: str = os.getenv("BOT_TOKEN")
DB_URL: str = os.getenv("DATABASE_URL")

engine = create_async_engine(DB_URL, echo=True)

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
