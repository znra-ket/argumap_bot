from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .keyboard import show_main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! \n"
    "Этот бот создан для хранения переписок-дискуссий, которые вы ведете! \n" 
    "Сохраняйте тезисы и аргументы с обеих сторон, а потом возвращайтесь к ним!")

    await show_main_menu(update, context)