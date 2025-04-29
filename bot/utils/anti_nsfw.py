# bot/utils/anti_nsfw.py
import requests
from telegram import Update
from telegram.ext import ContextTypes

DEEPAI_API_KEY = "c4d2e8ee-987b-48e0-ae51-9f4e81a42152"  # Replace this with your actual key

async def anti_nsfw_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    # Skip admin messages
    if user and user.id in context.bot_data.get("approved_admins", []):
        return

    # Handle media
    if message.photo or message.video or message.document or message.sticker:
        file = message.photo[-1] if message.photo else (
            message.video or message.document or message.sticker
        )
        file_path = await file.get_file()
        file_bytes = await file_path.download_as_bytearray()

        response = requests.post(
            "https://api.deepai.org/api/nsfw-detector",
            files={"image": file_bytes},
            headers={"api-key": DEEPAI_API_KEY}
        )

        if response.ok and response.json().get("output", {}).get("nsfw_score", 0) > 0.7:
            await message.delete()
            return

    # Handle links
    if message.text:
        keywords = ["porn", "sex", "xxx", "nsfw", "xvideos", "redtube", "xnxx"]
        if any(word in message.text.lower() for word in keywords):
            await message.delete()
            
