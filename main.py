import asyncio
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers.start import start
from bot.handlers.help import help_command
from bot.handlers import afk
from bot.handlers.welcome import welcome_handler, goodbye_handler
from bot.handlers.filters import add_filter, remove_filter, check_filter
from bot.handlers.silent import sban, smute, skick, swarn
from bot.handlers.temp import tban, tmute, tkick
from bot.handlers.utils import tag_all, lock, unlock
from bot.utils.permissions import is_admin
from bot.utils.anti_nsfw import anti_nsfw_filter
from middlewares.anti_edit import anti_edit_filter
from pymongo import MongoClient

# MongoDB setup
TOKEN = "7968316763:AAFbirkPbHvEqTJWM8l-SJaDuofQnvf_DS0"
MONGO_URI = "mongodb+srv://pop300k:tE4m7yVI6DNtXWsk@cluster0.y3knwm0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client['moderation_bot']

async def main():
    app = Application.builder().token(TOKEN).build()

    # Optional: Add approved admin IDs for NSFW bypass
    app.bot_data["approved_admins"] = [123456789, 987654321]  # Replace with real Telegram IDs

    # Register AFK handlers
    for handler in afk.get_afk_handlers():
        app.add_handler(handler)

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sban", sban))
    app.add_handler(CommandHandler("smute", smute))
    app.add_handler(CommandHandler("skick", skick))
    app.add_handler(CommandHandler("swarn", swarn))
    app.add_handler(CommandHandler("tban", tban))
    app.add_handler(CommandHandler("tmute", tmute))
    app.add_handler(CommandHandler("tkick", tkick))
    app.add_handler(CommandHandler("addfilter", add_filter))
    app.add_handler(CommandHandler("removefilter", remove_filter))
    app.add_handler(CommandHandler("tagall", tag_all))
    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))

    # Callback handler
    app.add_handler(CallbackQueryHandler(help_command))

    # NSFW and Edit filters applied to all incoming messages
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, anti_nsfw_filter))
    app.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, anti_edit_filter))

    # Welcome / Leave
    app.add_handler(welcome_handler)
    app.add_handler(goodbye_handler)

    print("Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
    
