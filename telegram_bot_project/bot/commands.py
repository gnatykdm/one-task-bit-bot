from typing import Any
from aiogram.types import Message

async def start_command(message: Message, **kwargs: Any) -> None:
    await message.answer("Hello!")


