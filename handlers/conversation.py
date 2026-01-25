from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, CommandHandler, filters, CallbackQueryHandler
from services import MessageService, DebateService
from database import get_session
from .keyboard import show_main_menu, cancel_keyboard, get_debates_keyboard, message_type_keyboard, view_type_keyboard

ENTER_DEBATE_NAME = 1
SELECT_DEBATE_TO_ACTIVATE = 2
FORWARD_MESSAGE = 3
SELECT_MESSAGE_TYPE = 4
SELECT_DEBATE_TO_VIEW = 5
SELECT_VIEW_TYPE = 6

async def cancel(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()

    session = get_session()
    debate_serv = DebateService(session)

    user_id = query.from_user.id

    debate = debate_serv.get_active_debate(user_id=user_id)

    if debate:
        result = debate_serv.deactivate_debate(debate_id=debate.debate_id, user_id=user_id)

        if not result:
            await query.message.reply_text("Не удалось деактивировать дебат")

        else:
            await query.message.reply_text("Дебат деактивирован!")

    await show_main_menu(query, context)

    context.user_data.clear()

    session.close()
    return ConversationHandler.END


async def start_create_debate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.message.edit_text("Дайте название новому дебату, пхе!", reply_markup=cancel_keyboard)

    return ENTER_DEBATE_NAME

async def enter_debate_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = get_session()
    debate_serv = DebateService(session)
    
    debate_name = update.message.text
    user_id = update.message.from_user.id
    
    result = debate_serv.create_debate(user_id=user_id, name=debate_name)

    if not result:
        await update.message.reply_text("Дебат с таким названием уже существует.. :(")

    if result:
        await update.message.reply_text("Дебат успешно создан! :3")

    await show_main_menu(update, context)
    session.close()

    return ConversationHandler.END


async def show_user_debates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = get_session()
    debate_serv = DebateService(session)

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id


    keyboard = await get_debates_keyboard(update=query, context=context, user_id=user_id, debate_serv=debate_serv)

    if not keyboard:
        await query.message.reply_text("К сожалению, у вас еще нет созданных дебатов! Вы можете создать дебат с помощью кнопки **Создать дебат**")
        await show_main_menu(query, context)
        session.close()

        return ConversationHandler.END

    await query.message.edit_text("Выберите дебат, который хотите активировать", reply_markup=InlineKeyboardMarkup(keyboard))

    session.close()

    return SELECT_DEBATE_TO_ACTIVATE

async def select_debate_to_activate(update: Update, context: ContextTypes):
    session = get_session()
    debate_serv = DebateService(session)
    
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    debate_name = query.data

    debate = debate_serv.get_debate_by_name(debate_name, user_id=user_id)
    
    if not debate:
        await query.message.reply_text("Дебата с таким названием не существует!")
        await query.message.delete()
        await show_main_menu(query, context)
        session.close()

        return ConversationHandler.END
    
    result = debate_serv.activate_debate(debate.debate_id, user_id=user_id)

    if not result:
        await query.message.edit_text("Не получилось активировать дебат :(")
        await show_main_menu(query, context)
        session.close()

        return ConversationHandler.END 
    else:
        await query.message.edit_text("Вы активировали дебат! Можете пересылать сообщения пользователей, после чего они будут сохранены в дебате", reply_markup=cancel_keyboard)

    context.user_data["active_debate"] = debate

    session.close()

    return FORWARD_MESSAGE

async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.forward_origin

    user_id = 0
    username = "Пользователь"

    if message.type == "user":
        user_id = message.sender_user.id
        username = message.sender_user.username

    context.user_data["user_id"] = user_id
    context.user_data["username"] = username
    context.user_data["text"] = update.message.text
    
    await update.message.reply_text("Какой тип этого сообщения?", reply_markup=message_type_keyboard)

    return SELECT_MESSAGE_TYPE


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = get_session()
    message_serv = MessageService(session)

    query = update.callback_query
    await query.answer()

    state = query.data

    debate = context.user_data["active_debate"]
    user_id = context.user_data["user_id"]
    username = context.user_data["username"]
    text = context.user_data["text"]


    result = message_serv.create_message(
        debate_id=debate.debate_id,
        user_id=user_id,
        username=username,
        state=state,
        text=text
    )

    if not result:
        await query.message.edit_text("Не удалось сохранить сообщение :(")
    else: 
        await query.message.edit_text("Сообщение сохранено!")

    session.close()

    return FORWARD_MESSAGE
    
async def start_show_debates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = get_session()
    debate_serv = DebateService(session)

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    keyboard = await get_debates_keyboard(update=query, context=context, user_id=user_id, debate_serv=debate_serv)

    if not keyboard:
        await query.message.reply_text("К сожалению, у вас еще нет созданных дебатов! Вы можете создать дебат с помощью кнопки **Создать дебат**")
        await show_main_menu(query, context)
        
        return ConversationHandler.END

    await query.message.edit_text("Выберите дебат, который хотите просмотреть", reply_markup=InlineKeyboardMarkup(keyboard))

    session.close()

    return SELECT_DEBATE_TO_VIEW


async def select_debate_to_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    session = get_session()
    debate_serv = DebateService(session)

    debate_name = query.data

    debate = debate_serv.get_debate_by_name(name=debate_name, user_id=user_id)

    if not debate:
        await query.message.edit_text("Дебат не найден")
        await show_main_menu(query, context)
        session.close()

        return ConversationHandler.END

    context.user_data["debate"] = debate

    await query.message.edit_text("Какие сообщения вы хотите просмотреть?", reply_markup=view_type_keyboard)

    session.close()

    return SELECT_VIEW_TYPE


async def show_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    session = get_session()
    message_serv = MessageService(session)

    messages_type = query.data

    await query.message.delete()

    if messages_type == "Аргументы":
        debate = context.user_data["debate"]
        messages = message_serv.get_arguments(debate_id=debate.debate_id)

        for message in messages:
            await query.message.reply_text(f"{message.text} \n\n-{message.from_username}")

    elif messages_type == "Тезисы":
        debate = context.user_data["debate"]
        messages = message_serv.get_theses(debate_id=debate.debate_id)

        for message in messages:
            await query.message.reply_text(f"{message.text} \n\n-{message.from_username}")
    
    else:
        debate = context.user_data["debate"]
        messages = message_serv.get_messages(debate_id=debate.debate_id)

        for message in messages:
            await query.message.reply_text(f"{message.text} \n\n-{message.from_username}")

    session.close()
    await show_main_menu(query, context)

    return ConversationHandler.END

create_debate_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(pattern="^Создать дебат$", callback=start_create_debate)
    ],
    states={
        ENTER_DEBATE_NAME: [MessageHandler(filters.TEXT & ~ filters.COMMAND, enter_debate_name)]
    },
    fallbacks=[
        CallbackQueryHandler(pattern="^Назад$", callback=cancel)
    ]
)

create_message_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(pattern="^Мои дебаты$", callback=show_user_debates)
    ],
    states={
        SELECT_DEBATE_TO_ACTIVATE: [CallbackQueryHandler(callback=select_debate_to_activate)],
        FORWARD_MESSAGE: [MessageHandler(filters.FORWARDED, handle_forwarded_message)],
        SELECT_MESSAGE_TYPE: [CallbackQueryHandler(callback=save_message)]
    },
    fallbacks=[
        CallbackQueryHandler(pattern="^Назад$", callback=cancel)
    ]
)

show_debates_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(start_show_debates, pattern="^Просмотреть дебат$")
    ],
    states={
        SELECT_DEBATE_TO_VIEW: [CallbackQueryHandler(select_debate_to_view)],
        SELECT_VIEW_TYPE: [CallbackQueryHandler(show_messages)]
    },
    fallbacks=[
        CallbackQueryHandler(cancel, pattern="^Назад$")
    ]
)