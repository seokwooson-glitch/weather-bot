import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from weather import get_weather, format_weather

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MODE = os.getenv("MODE", "weather")

async def send_weather():
    bot = Bot(token=TOKEN)
    w = get_weather("bundang")

    if MODE == "morning":
        msg = "Good Morning!\n\n" + format_weather(w)
        await bot.send_message(chat_id=CHAT_ID, text=msg)

    elif MODE == "hourly":
        pty = w.get("pty", "")
        if pty:
            msg = "Rain Alert!\n\n" + format_weather(w)
            await bot.send_message(chat_id=CHAT_ID, text=msg)

    elif MODE == "weather":
        msg = "Current Weather\n\n" + format_weather(w)
        await bot.send_message(chat_id=CHAT_ID, text=msg)

if __name__ == "__main__":
    asyncio.run(send_weather())
