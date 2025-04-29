from telegram import Update
from telegram.ext import ContextTypes

async def welcome_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            await update.message.reply_text(
                f"Hey {member.mention_html()}, welcome to the group! "
                "Feel free to introduce yourself and jump into the conversation. "
                "We're glad to have you here!",
                parse_mode="HTML"
            )

async def goodbye_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.left_chat_member:
        await update.message.reply_text(
            f"We’ll miss you, {update.message.left_chat_member.full_name}. "
            "Hope to see you again someday. The group won’t be the same without you!"
        )
