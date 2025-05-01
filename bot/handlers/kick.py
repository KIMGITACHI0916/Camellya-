# bot/handlers/kick.py
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.reply_to_message:
        await update.message.reply_text("Reply to the user's message to kick them.")
        return

    user = update.effective_user
    member = await update.effective_chat.get_member(user.id)
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await update.message.reply_text("Only admins can use this command.")
        return

    target_user = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id, until_date=0)
        await context.bot.unban_chat_member(chat_id=update.effective_chat.id, user_id=target_user.id)
        await update.message.reply_text(f"Kicked {target_user.full_name}.")
    except Exception as e:
        await update.message.reply_text(f"Failed to kick user: {e}")
      
