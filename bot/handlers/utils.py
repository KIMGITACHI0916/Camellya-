from telegram import Update, ChatPermissions
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ChatAction

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action(ChatAction.TYPING)
    members = await context.bot.get_chat_administrators(update.effective_chat.id)

    mentions = []
    async for member in context.bot.get_chat_members(update.effective_chat.id):
        if not member.user.is_bot:
            mentions.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")
            if len(mentions) >= 30:  # Telegram has limits
                break

    mention_text = " ".join(mentions)
    await update.message.reply_text(mention_text, parse_mode="Markdown")

async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permissions = ChatPermissions(
        can_send_messages=False,
        can_send_media_messages=False,
        can_send_other_messages=False,
        can_add_web_page_previews=False
    )
    await context.bot.set_chat_permissions(update.effective_chat.id, permissions)
    await update.message.reply_text("Group has been locked.")

async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    permissions = ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True
    )
    await context.bot.set_chat_permissions(update.effective_chat.id, permissions)
    await update.message.reply_text("Group has been unlocked.")
  
