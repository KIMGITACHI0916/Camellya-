import re
import aiohttp
from telegram import Message
from bot.utils.database import is_user_admin  # Make sure this exists

# Add common adult keywords or domains
BAD_LINK_PATTERNS = [
    r"(porn|xxx|sex|hentai|xvideos|xnxx|redtube|onlyfans|nude|nsfw)",
    r"(https?:\/\/)?(www\.)?(pornhub|xhamster|rule34|erome|onlyfans|nsfw)\.com",
]

async def check_nsfw_image(file_url: str) -> bool:
    api_key = "YOUR_DEEPAI_API_KEY"
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.deepai.org/api/nsfw-detector",
            data={'image': file_url},
            headers={'api-key': api_key}
        ) as resp:
            data = await resp.json()
            score = data.get("output", {}).get("nsfw_score", 0)
            return score > 0.7

async def is_nsfw_message(message: Message, bot) -> bool:
    # Admin bypass check
    chat_id = message.chat_id
    user_id = message.from_user.id
    if await is_user_admin(chat_id, user_id):
        return False

    # Text-based porn link check
    if message.text:
        for pattern in BAD_LINK_PATTERNS:
            if re.search(pattern, message.text, re.IGNORECASE):
                return True

    # Image/Video/Sticker NSFW check
    media = message.photo or message.video or message.sticker
    if media:
        try:
            file = await media[-1].get_file() if isinstance(media, list) else await media.get_file()
            file_url = file.file_path
            return await check_nsfw_image(file_url)
        except:
            return True  # Fail safe: delete if error occurs

    return False
  
