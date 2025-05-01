from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        chat = update.effective_chat
        user = update.effective_user
        member = await chat.get_member(user.id)
        if member.status not in ['administrator', 'creator']:
            await update.message.reply_text("You must be an admin to use this command.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper
