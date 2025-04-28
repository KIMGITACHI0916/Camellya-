from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Add to Your Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    photo = InputFile("IMG_20250427_025638.jpg")  # Your selected anime image

    caption = (
        "*✨ HELLO... ✨*\n\n"
        "*I'M A CHARACTER SNATCH BOT!*\n\n"
        "➤ Add me to your group and I will send random characters!\n\n"
        "➤ Tap 'Help' to see all available commands.\n\n"
        "_Let's make your group more fun!_\n\n"
        "`➛ PING:` 1.00 ms\n"
        "`➛ UPTIME:` 0h 0m 0s"
    )

    await update.message.reply_photo(
        photo=photo,
        caption=caption,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )
