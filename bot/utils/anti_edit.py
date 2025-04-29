from telegram import Update
from telegram.ext import ContextTypes

from bot.utils.helper import is_user_admin  # Adjust path if needed

async def anti_edit_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    edited_message = update.edited_message

    if not edited_message:
        return

    chat = edited_message.chat
    user = edited_message.from_user

    # Don't delete messages from admins
    member = await chat.get_member(user.id)
    if member.status in ("administrator", "creator"):
        return

    try:
        await context.bot.delete_message(chat_id=chat.id, message_id=edited_message.message_id)
    except Exception as e:
        print(f"Failed to delete edited message: {e}")
      
