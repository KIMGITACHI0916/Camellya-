from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from datetime import timedelta
from bot.utils.admin_check import admin_only  # Ensure this exists and is correctly implemented

# --- Basic Commands ---

@admin_only
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text("User banned.")

@admin_only
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        user_id = int(context.args[0])
        await update.effective_chat.unban_member(user_id)
        await update.message.reply_text("User unbanned.")

@admin_only
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await update.effective_chat.ban_member(user_id)
        await update.effective_chat.unban_member(user_id)
        await update.message.reply_text("User kicked.")

@admin_only
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await update.effective_chat.restrict_member(user_id, ChatPermissions())
        await update.message.reply_text("User muted.")

@admin_only
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        perms = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        await update.effective_chat.restrict_member(user_id, perms)
        await update.message.reply_text("User unmuted.")

# --- Silent Commands (No reply to admin) ---

@admin_only
async def sban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id)

@admin_only
async def sunban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        await update.effective_chat.unban_member(int(context.args[0]))

@admin_only
async def skick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user_id = update.message.reply_to_message.from_user.id
        await update.effective_chat.ban_member(user_id)
        await update.effective_chat.unban_member(user_id)

@admin_only
async def smute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions())

@admin_only
async def sunmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        perms = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, perms)

# Placeholder warn/swarn system (you can expand this with counters and reasons)
@admin_only
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("User warned.")

@admin_only
async def swarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@admin_only
async def sunwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

# --- Temporary Commands ---

def parse_duration(duration_str):
    unit = duration_str[-1]
    value = int(duration_str[:-1])
    if unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    else:
        return timedelta(minutes=5)  # default fallback

@admin_only
async def tban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and context.args:
        duration = parse_duration(context.args[0])
        until = update.message.date + duration
        await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id, until_date=until)
        await update.message.reply_text(f"User temporarily banned for {context.args[0]}.")

@admin_only
async def tkick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await kick(update, context)

@admin_only
async def tmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and context.args:
        duration = parse_duration(context.args[0])
        until = update.message.date + duration
        await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(), until_date=until)
        await update.message.reply_text(f"User temporarily muted for {context.args[0]}.")

@admin_only
async def twarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("User temporarily warned.")
                
