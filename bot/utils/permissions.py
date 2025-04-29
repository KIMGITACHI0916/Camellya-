from telegram import Update
from telegram.ext import ContextTypes

async def is_admin(update: Update) -> bool:
    user_id = update.effective_user.id
    chat_admins = await update.effective_chat.get_administrators()
    return any(admin.user.id == user_id for admin in chat_admins)
