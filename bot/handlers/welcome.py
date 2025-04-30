from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# Welcome function
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"Welcome, {member.mention_html()}!", parse_mode='HTML')

# Goodbye function
async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    left_member = update.message.left_chat_member
    await update.message.reply_text(f"{left_member.full_name} has left the chat.")

# Handlers
welcome_handler = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome)
goodbye_handler = MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, goodbye)
