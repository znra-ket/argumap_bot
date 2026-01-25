# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ContextTypes
# from services import DebateService

# cancel_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Назад", callback_data="Назад")]])

# choice_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Тезис", callback_data="Тезис")], [InlineKeyboardButton(text="Аргумент", callback_data="Аргумент")]])

# choice_type_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Аргументы", callback_data="Аргументы"), InlineKeyboardButton(text="Тезисы", callback_data="Тезисы"), InlineKeyboardButton(text="Все сообщения", callback_data="Все сообщения")], [InlineKeyboardButton(text="Назад", callback_data="Назад")]])


# async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("Мои дебаты", callback_data="Мои дебаты"), InlineKeyboardButton("Создать дебат", callback_data="Создать дебат")],
#         [InlineKeyboardButton("Просмотреть дебат", callback_data="Просмотреть дебат")]
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text('Вы можете создать дебат по кнопке **Создать дебат**\n\n' \
#     'Так же можете активировать дебат, после чего пересылать и сохранять в нем сообщения ко кнопке **Мои дебаты**\n\n'
#     'После чего вы можете просмотреть сообщения из вашего дебата по кнопке **Просмотреть дебат**!', reply_markup=reply_markup)

# async def get_debates_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, debate_serv: DebateService, user_id):
#     debates = debate_serv.get_user_debates(user_id=user_id)

#     buttons = []

#     for debate in debates:
#         buttons.append([InlineKeyboardButton(text=debate.name, callback_data=debate.name)])

#     if buttons == []:
#         return False

#     buttons.append([InlineKeyboardButton(text="Назад", callback_data="Назад")])

#     return buttons


from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services import DebateService

cancel_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(text="Назад", callback_data="Назад")]])

message_type_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text="Тезис", callback_data="Тезис")], 
    [InlineKeyboardButton(text="Аргумент", callback_data="Аргумент")]
])

view_type_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text="Аргументы", callback_data="Аргументы"), InlineKeyboardButton(text="Тезисы", callback_data="Тезисы"), InlineKeyboardButton(text="Все сообщения", callback_data="Все сообщения")], 
    [InlineKeyboardButton(text="Назад", callback_data="Назад")]
])

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Мои дебаты", callback_data="Мои дебаты"), InlineKeyboardButton("Создать дебат", callback_data="Создать дебат")],
        [InlineKeyboardButton("Просмотреть дебат", callback_data="Просмотреть дебат")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Вы можете создать дебат по кнопке **Создать дебат**\n\n' \
    'Так же можете активировать дебат, после чего пересылать и сохранять в нем сообщения ко кнопке **Мои дебаты**\n\n'
    'После чего вы можете просмотреть сообщения из вашего дебата по кнопке **Просмотреть дебат**!', reply_markup=reply_markup)

async def get_debates_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE, debate_serv: DebateService, user_id):
    debates = debate_serv.get_user_debates(user_id=user_id)
    buttons = []
    for debate in debates:
        buttons.append([InlineKeyboardButton(text=debate.name, callback_data=debate.name)])
    if buttons == []:
        return False
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="Назад")])
    return buttons
