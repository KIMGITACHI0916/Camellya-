import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers.start import start
from bot.handlers.help import get_help_handlers
from bot.handlers import afk
from bot.handlers.welcome import welcome_handler, goodbye_handler
from bot.handlers.filters import add_filter, remove_filter, check_filter
from bot.handlers import moderation
from bot.utils.admin_check import admin_only
from bot.handlers.utils import tag_all, lock, unlock
from bot.utils.anti_nsfw import anti_nsfw_filter
from bot.utils.anti_edit import anti_edit_filter
from pymongo import MongoClient

# Set your actual token and Mongo URI here securely
TOKEN = "7968316763:AAH5XsSeWaQOucSKHQdYQ9M6HVijFnanOJA"
MONGO_URI = "mongodb+srv://pop300k:tE4m7yVI6DNtXWsk@cluster0.y3knwm0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['moderation_bot']

async def main():
    app = Application.builder().token(TOKEN).build()

    # Basic command handlers
    app.add_handler(CommandHandler("start", start))
    for handler in get_help_handlers():
        app.add_handler(handler)
    for handler in afk.get_afk_handlers():
        app.add_handler(handler)

    # Moderation commands
    moderation_commands = [
        ("ban", moderation.ban),
        ("unban", moderation.unban),
        ("kick", moderation.kick),
        ("mute", moderation.mute),
        ("unmute", moderation.unmute),
        ("warn", moderation.warn),
        ("sban", moderation.sban),
        ("sunban", moderation.sunban),
        ("skick", moderation.skick),
        ("smute", moderation.smute),
        ("sunmute", moderation.sunmute),
        ("swarn", moderation.swarn),
        ("sunwarn", moderation.sunwarn),
        ("tban", moderation.tban),
        ("tkick", moderation.tkick),
        ("tmute", moderation.tmute),
        ("twarn", moderation.twarn),
    ]
    for cmd, func in moderation_commands:
        app.add_handler(CommandHandler(cmd, func))

    # Admin-only commands
    app.add_handler(CommandHandler("addfilter", admin_only(add_filter)))
    app.add_handler(CommandHandler("removefilter", admin_only(remove_filter)))
    app.add_handler(CommandHandler("tagall", admin_only(tag_all)))
    app.add_handler(CommandHandler("lock", admin_only(lock)))
    app.add_handler(CommandHandler("unlock", admin_only(unlock)))

    # Message-based filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_filter))
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, anti_nsfw_filter))
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, anti_edit_filter))

    # Welcome/leave
    app.add_handler(welcome_handler)
    app.add_handler(goodbye_handler)

    print("Bot is initializing...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("Bot is running...")

    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        print("Detected running event loop — using create_task.")
        loop.create_task(main())
    else:
        print("No running loop — using asyncio.run().")
        asyncio.run(main())
        
