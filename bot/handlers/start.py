from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Add Me to Your Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("ℹ️ Help & Commands", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    caption = (
        "👋 *Hello!*\n\n"
        "🔧 *I'm your Group Management Assistant.*\n\n"
        "➤ Add me to your group to unlock powerful moderation and management features.\n"
        "➤ Tap *Help* below to view all available commands.\n\n"
        "⚡ *Fast • Secure • Reliable*"
    )

    image_url = "https://i.imgur.com/h0LhYD3.jpeg"

    await update.message.reply_photo(
        photo=image_url,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
