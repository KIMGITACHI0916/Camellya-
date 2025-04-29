from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils.permissions import is_admin
from utils.database import warn_user

from bot.utils.permissions import is_admin

async def sban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)

async def smute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    if update.message.reply_to_message:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            update.message.reply_to_message.from_user.id,
            permissions={"can_send_messages": False}
        )

async def skick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    if update.message.reply_to_message:
        await context.bot.ban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, update.message.reply_to_message.from_user.id)

async def swarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return
    if update.message.reply_to_message:
        await warn_user(update.message.reply_to_message.from_user.id, update.effective_chat.id)

def silent_handlers():
    return [
        CommandHandler("sban", sban),
        CommandHandler("smute", smute),
        CommandHandler("skick", skick),
        CommandHandler("swarn", swarn),
    ]
  
