from telegram import Update
from telegram.ext import ContextTypes
from functools import wraps

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        chat = update.effective_chat

        member = await chat.get_member(user.id)
        if member.status in ("administrator", "creator"):
            return await func(update, context)
        else:
            await update.message.reply_text("You must be an admin to use this command.")
    return wrapper
  
