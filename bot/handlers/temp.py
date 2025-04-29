from telegram import Update
from telegram.ext import ContextTypes
from datetime import timedelta

async def tban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example: /tban @username 1h
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /tban <user> <duration>")
        return

    user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    duration = context.args[1]

    if not user:
        await update.message.reply_text("Reply to a user to ban.")
        return

    try:
        seconds = convert_to_seconds(duration)
        await context.bot.ban_chat_member(update.effective_chat.id, user.id, until_date=update.message.date + timedelta(seconds=seconds))
        await update.message.reply_text(f"{user.mention_html()} banned for {duration}", parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(str(e))

async def tmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Example: /tmute @username 10m
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /tmute <user> <duration>")
        return

    user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    duration = context.args[1]

    if not user:
        await update.message.reply_text("Reply to a user to mute.")
        return

    try:
        seconds = convert_to_seconds(duration)
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            permissions=telegram.ChatPermissions(can_send_messages=False),
            until_date=update.message.date + timedelta(seconds=seconds)
        )
        await update.message.reply_text(f"{user.mention_html()} muted for {duration}", parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(str(e))

async def tkick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else None

    if not user:
        await update.message.reply_text("Reply to a user to kick.")
        return

    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"{user.mention_html()} was kicked.", parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(str(e))

def convert_to_seconds(duration: str) -> int:
    unit = duration[-1]
    num = int(duration[:-1])
    if unit == "m":
        return num * 60
    elif unit == "h":
        return num * 3600
    elif unit == "d":
        return num * 86400
    else:
        raise ValueError("Invalid duration format. Use m/h/d.")
      
