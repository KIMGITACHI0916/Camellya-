from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler

HELP_CATEGORIES = {
    "admin": "Commands to manage admins.",
    "bans": "Ban, kick, and mute users.",
    "filters": "Set up custom keyword replies.",
    "notes": "Save and get notes.",
    "locks": "Lock media, stickers, etc.",
    "warns": "Warn and manage rule breakers."
}

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Admin", callback_data="help_admin"),
         InlineKeyboardButton("Bans", callback_data="help_bans")],
        [InlineKeyboardButton("Filters", callback_data="help_filters"),
         InlineKeyboardButton("Notes", callback_data="help_notes")],
        [InlineKeyboardButton("Locks", callback_data="help_locks"),
         InlineKeyboardButton("Warnings", callback_data="help_warns")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Select a category to get help:",
        reply_markup=reply_markup
    )

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.replace("help_", "")
    text = HELP_CATEGORIES.get(category, "No help available for this category.")
    await query.edit_message_text(f"**{category.capitalize()} Help**\n\n{text}", parse_mode="Markdown")

def get_help_handlers():
    return [
        CommandHandler("help", help_command),
        CallbackQueryHandler(help_callback, pattern=r"^help_")
    ]
  
