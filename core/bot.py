from telegram.ext import Application, CommandHandler
from handlers import start, create_debate_handler, create_message_handler, show_debates_handler
from config import TOKEN

def create_bot():
    app = Application.builder().token(token=TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(create_debate_handler)
    app.add_handler(create_message_handler)
    app.add_handler(show_debates_handler)

    app.run_polling()