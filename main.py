from telegram.ext import Application, CommandHandler
from bot.handlers.start import start

app = Application.builder().token("7968316763:AAFbirkPbHvEqTJWM8l-SJaDuofQnvf_DS0").build()

app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run_polling()
