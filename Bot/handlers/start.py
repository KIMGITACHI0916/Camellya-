from pyrogram import Client, filters

def register(Bot: Client):
    @Bot.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message):
        await message.reply_text("Hello! Your bot is alive and working.")
