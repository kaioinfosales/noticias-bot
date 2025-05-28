import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CANAL_ID = os.getenv("CANAL_ID")

bot = Bot(token=TELEGRAM_TOKEN)

async def teste_envio():
    await bot.send_message(chat_id=CANAL_ID, text="Teste rápido do bot 🚀")

if __name__ == "__main__":
    asyncio.run(teste_envio())
