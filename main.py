import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers.start import start
from bot.handlers.help import get_help_handlers
from bot.handlers import afk
from bot.handlers.welcome import welcome_handler, goodbye_handler
from bot.handlers.filters import add_filter, remove_filter, check_filter
from bot.handlers.silent import sban, smute, skick, swarn
from bot.handlers.temp import tban, tmute, tkick
from bot.handlers.utils import tag_all, lock, unlock
from bot.utils.anti_nsfw import anti_nsfw_filter
from bot.utils.anti_edit import anti_edit_filter
from pymongo import MongoClient

TOKEN = "7968316763:AAH5XsSeWaQOucSKHQdYQ9M6HVijFnanOJA"
MONGO_URI = "mongodb+srv://pop300k:tE4m7yVI6DNtXWsk@cluster0.y3knwm0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['moderation_bot']

async def main():
    app = Application.builder().token(TOKEN).build()
    app.bot_data["approved_admins"] = [123456789]  # Replace with real admin user IDs

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    for handler in get_help_handlers():
        app.add_handler(handler)
    for handler in afk.get_afk_handlers():
        app.add_handler(handler)

    app.add_handler(CommandHandler("sban", sban))
    app.add_handler(CommandHandler("smute", smute))
    app.add_handler(CommandHandler("skick", skick))
    app.add_handler(CommandHandler("swarn", swarn))

    app.add_handler(CommandHandler("tban", tban))
    app.add_handler(CommandHandler("tmute", tmute))
    app.add_handler(CommandHandler("tkick", tkick))

    app.add_handler(CommandHandler("addfilter", add_filter))
    app.add_handler(CommandHandler("removefilter", remove_filter))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_filter))

    app.add_handler(CommandHandler("tagall", tag_all))
    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))

    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, anti_nsfw_filter))
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, anti_edit_filter))

    app.add_handler(welcome_handler)
    app.add_handler(goodbye_handler)

    print("Bot is initializing...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("Bot is running...")

    # Keeps the bot running
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
        
