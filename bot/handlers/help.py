from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

HELP_TEXT = """
Available Commands:
/start - Start the bot
/help - Show this help message
/warn - Warn a user
/mute - Mute a user
/unmute - Unmute a user
/kick - Kick a user
/ban - Ban a user
/unban - Unban a user
/tagall - Mention all members
/afk - Set your AFK status
/locks - View group lock settings
"""

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)

def get_help_handler():
    return CommandHandler("help", help_command)
  
