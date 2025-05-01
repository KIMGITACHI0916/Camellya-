from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from datetime import timedelta
from bot.utils.admin_check import admin_only

# --- Utility: Duration Parser ---
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


# --- Admin Moderation Commands ---

@admin_only
async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("This command only works in groups.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to ban them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    bot_member = await update.effective_chat.get_member(context.bot.id)

    if bot_member.status != "administrator" or not bot_member.can_restrict_members:
        await update.message.reply_text("I need to be an admin with ban rights.")
        return

    try:
        await update.effective_chat.ban_member(user_id)
        await update.message.reply_text("User banned.")
    except Exception as e:
        await update.message.reply_text(f"Failed to ban user: {e}")


@admin_only
async def unban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a user ID.")
        return

    try:
        user_id = int(context.args[0])
        await update.effective_chat.unban_member(user_id)
        await update.message.reply_text("User unbanned.")
    except Exception as e:
        await update.message.reply_text(f"Failed to unban user: {e}")


@admin_only
async def kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to kick them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    try:
        await update.effective_chat.ban_member(user_id)
        await update.effective_chat.unban_member(user_id)
        await update.message.reply_text("User kicked.")
    except Exception as e:
        await update.message.reply_text(f"Failed to kick user: {e}")


@admin_only
async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to mute them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    try:
        await update.effective_chat.restrict_member(user_id, ChatPermissions())
        await update.message.reply_text("User muted.")
    except Exception as e:
        await update.message.reply_text(f"Failed to mute user: {e}")


@admin_only
async def unmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to unmute them.")
        return

    user_id = update.message.reply_to_message.from_user.id
    perms = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
    )

    try:
        await update.effective_chat.restrict_member(user_id, perms)
        await update.message.reply_text("User unmuted.")
    except Exception as e:
        await update.message.reply_text(f"Failed to unmute user: {e}")


@admin_only
async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("User warned.")  # Expand with counter and reason


# --- Silent Commands ---

@admin_only
async def sban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try:
            await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id)
        except:
            pass

@admin_only
async def sunban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            await update.effective_chat.unban_member(int(context.args[0]))
        except:
            pass

@admin_only
async def skick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try:
            user_id = update.message.reply_to_message.from_user.id
            await update.effective_chat.ban_member(user_id)
            await update.effective_chat.unban_member(user_id)
        except:
            pass

@admin_only
async def smute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        try:
            await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions())
        except:
            pass

@admin_only
async def sunmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        perms = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        try:
            await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, perms)
        except:
            pass

@admin_only
async def swarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  # Silent warn logic here

@admin_only
async def sunwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass  # Silent unwarn logic here


# --- Temporary Commands ---

@admin_only
async def tban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and context.args:
        try:
            duration = parse_duration(context.args[0])
            until = update.message.date + duration
            await update.effective_chat.ban_member(update.message.reply_to_message.from_user.id, until_date=until)
            await update.message.reply_text(f"User temporarily banned for {context.args[0]}.")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")


@admin_only
async def tkick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await kick(update, context)


@admin_only
async def tmute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message and context.args:
        try:
            duration = parse_duration(context.args[0])
            until = update.message.date + duration
            await update.effective_chat.restrict_member(update.message.reply_to_message.from_user.id, ChatPermissions(), until_date=until)
            await update.message.reply_text(f"User temporarily muted for {context.args[0]}.")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")


@admin_only
async def twarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("User temporarily warned.")  # Extend with logic
