from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from pymongo import MongoClient

client = MongoClient("your_mongo_connection_string")
db = client["moderation_bot"]
collection = db["filters"]

def get_filters(chat_id):
    return collection.find_one({"chat_id": chat_id}) or {"filters": {}}

def save_filters(chat_id, filters):
    collection.update_one(
        {"chat_id": chat_id},
        {"$set": {"filters": filters}},
        upsert=True
    )

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        return await update.message.reply_text("Usage: /filter [word] [response]")

    word = context.args[0].lower()
    response = " ".join(context.args[1:])

    filters_data = get_filters(update.effective_chat.id)["filters"]
    filters_data[word] = response
    save_filters(update.effective_chat.id, filters_data)

    await update.message.reply_text(f"Filter for '{word}' added!")

async def remove_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /stop [word]")

    word = context.args[0].lower()
    filters_data = get_filters(update.effective_chat.id)["filters"]
    if word in filters_data:
        del filters_data[word]
        save_filters(update.effective_chat.id, filters_data)
        await update.message.reply_text(f"Filter for '{word}' removed.")
    else:
        await update.message.reply_text(f"No filter found for '{word}'.")

async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    filters_data = get_filters(update.effective_chat.id)["filters"]
    if not filters_data:
        await update.message.reply_text("No filters set.")
    else:
        text = "**Active Filters:**\n" + "\n".join(f"• `{k}`" for k in filters_data.keys())
        await update.message.reply_text(text, parse_mode="Markdown")

async def check_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    text = update.message.text.lower()
    filters_data = get_filters(chat_id)["filters"]

    for word, response in filters_data.items():
        if word in text:
            await update.message.reply_text(response)
            break
          
