from openai import AsyncOpenAI
from config import get_openai_key

client = AsyncOpenAI(api_key=get_openai_key())

async def ask_gpt(prompt: str, language: str = "ENGLISH") -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": f"You are Rocky AI assistant. The user's language is {language}."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise e
