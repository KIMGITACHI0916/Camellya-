from pyrogram import Client, filters

def register(bot: Client):
    @bot.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message):
        await message.reply_text("Hello! Your bot is alive and working.")
