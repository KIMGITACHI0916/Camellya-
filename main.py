from telegram.ext import Application, CommandHandler

from bot.handlers.start import start  # or your correct import path

async def main():
    app = Application.builder().token("7968316763:AAFbirkPbHvEqTJWM8l-SJaDuofQnvf_DS0").build()

    app.add_handler(CommandHandler("start", start))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
