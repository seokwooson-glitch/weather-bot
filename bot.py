import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from weather import get_weather, format_weather

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")

async def start(update, context):
    await update.message.reply_text(
        "🌤 분당 날씨 알림봇 시작!\n\n"
        "/weather - 지금 날씨 확인\n"
        "/alarm - 매시간 자동 알림 시작\n"
        "/stopalarm - 자동 알림 중지"
    )

async def weather_command(update, context):
    w = get_weather("분당")
    await update.message.reply_text(format_weather(w))

async def send_hourly_weather():
    bot = Bot(token=TOKEN)
    w = get_weather("분당")
    msg = "🕐 매시간 날씨 알림\n\n" + format_weather(w)
    await bot.send_message(chat_id=CHAT_ID, text=msg)

async def set_alarm(update, context):
    scheduler.add_job(send_hourly_weather, "cron", minute=0, id="hourly", replace_existing=True)
    await update.message.reply_text("⏰ 매시간 정각에 날씨를 알려드릴게요!")

async def stop_alarm(update, context):
    if scheduler.get_job("hourly"):
        scheduler.remove_job("hourly")
    await update.message.reply_text("🔕 자동 알림을 중지했어요.")

async def post_init(application):
    scheduler.start()

def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("alarm", set_alarm))
    app.add_handler(CommandHandler("stopalarm", stop_alarm))

    print("✅ 날씨봇 실행 중...")
    app.run_polling()

if __name__ == "__main__":
    main()