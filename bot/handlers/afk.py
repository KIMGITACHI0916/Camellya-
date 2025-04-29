# bot/handlers/afk.py

from telegram import Update, ChatAction
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("your_mongo_uri_here")  # Replace with your actual URI
db = client["moderation_bot"]
afk_collection = db["afk"]

# Set AFK
async def set_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reason = " ".join(context.args) if context.args else "No reason provided."
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    afk_collection.update_one(
        {"user_id": user_id},
        {"$set": {"reason": reason}},
        upsert=True
    )

    await update.message.reply_text(f"{user_name} is now AFK.\nReason: {reason}")

# Check if AFK user is mentioned and notify
async def check_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    for entity in update.message.entities:
        if entity.type == "mention":
            username = update.message.text[entity.offset: entity.offset + entity.length]
            user_data = afk_collection.find_one({"username": username.replace("@", "")})
            if user_data:
                await update.message.reply_text(f"{username} is AFK: {user_data['reason']}")

# Disable AFK on any message
async def remove_afk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    afk = afk_collection.find_one({"user_id": user_id})
    if afk:
        afk_collection.delete_one({"user_id": user_id})
        await update.message.reply_text("Welcome back! You're no longer AFK.")

# Handlers to register
def get_afk_handlers():
    return [
        CommandHandler("afk", set_afk),
        MessageHandler(filters.ALL & (~filters.COMMAND), remove_afk),
        MessageHandler(filters.ALL, check_afk)
    ]
