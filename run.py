import asyncio
import yaml
import logging
from datetime import datetime
from telegram import Bot
from telegram.constants import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

BOT_TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]

bot = Bot(token=BOT_TOKEN)

async def send_test_message():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = f"🚀 Pump Paper Agent đang hoạt động\n⏰ {now}"
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        parse_mode=ParseMode.HTML
    )

async def main():
    scheduler = AsyncIOScheduler()
    for t in config["report"]["times"]:
        hour, minute = map(int, t.split(":"))
        scheduler.add_job(send_test_message, "cron", hour=hour, minute=minute)

    scheduler.start()
    await send_test_message()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
