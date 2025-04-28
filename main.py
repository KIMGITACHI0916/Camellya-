import os
from dotenv import load_dotenv
from pyrogram import Client
from bot.handlers import start

# Load .env variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
bot = Client(
    "TelegramManagementBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Register handlers
start.register(bot)

# Start the bot
if __name__ == "__main__":
    bot.run()
