from telegram.ext import Application, CommandHandler
from bot.handlers.start import start

app = Application.builder().token("YOUR_BOT_TOKEN").build()

app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run_polling()
