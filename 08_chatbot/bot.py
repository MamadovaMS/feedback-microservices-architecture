import logging
import requests
import random
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler, CallbackQueryHandler
)

# --- НАСТРОЙКИ ---
TOKEN = "9211877281:AAHzZTqxCb2bKjrxYR4SkS-sajenBouiD3Y"  # Вставь свой новый токен, если старый не работает
API_URL = "http://localhost:5283/api/feedback"

# Состояния диалога
NAME, EMAIL, TOPIC, MESSAGE = range(4)

# Настройка логирования в файл (Требование на 5 баллов)
logging.basicConfig(
    filename='bot_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Саркастичные фразы после отправки
SUCCESS_PHRASES = [
    "Ну надо же, ты смог нажать «Отправить». Заявка улетела на сервер. Он, конечно, не в восторге, но принял.",
    "Окей, записал. Считай, что ты только что стал частью истории. Ну, или локальной базы данных.",
    "Готово. Теперь мы оба можем сделать вид, что этого не было. Отдыхай.",
    "Принято. Я передам это... кому-нибудь. Наверное.",
    "Заявка ушла. Не благодари, это буквально моя работа."
]

# --- 1. КОМАНДА /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user.first_name
    context.user_data.clear()
    logging.info(f"Пользователь {user} начал диалог.")
    await update.message.reply_text(
        f"О, привет, {user}. 👋\n"
        "Я бот для сбора обратной связи. Да, еще один.\n\n"
        "Если хочешь узнать, что я умею (спойлер: немного), напиши /help.\n"
        "Или давай покончим с этим быстрее. Как тебя зовут? (или /cancel, если передумал)"
    )
    return NAME

# --- 2. КОМАНДА /help (Требование на 5 баллов) ---
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 *Мои таланты:*\n\n"
        "🔹 /start — запустить этот цирк заново\n"
        "🔹 /help — ты только что это сделал. Поздравляю.\n"
        "🔹 /cancel — выйти из чата, пока не поздно\n\n"
        "Я спрошу твое имя, email и сообщение. Потом отправлю это на сервер и выдам тебе номер заявки. "
        "Не пытайся сопротивляться, алгоритм уже запущен 😉",
        parse_mode='Markdown'
    )

# --- 3. ПОЛУЧАЕМ ИМЯ ---
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['name'] = update.message.text
    await update.message.chat.send_action(action="typing")
    await update.message.reply_text("Записал. Надеюсь, ты не назвался 'Анонимус'.\n📧 Теперь кинь свой email:")
    return EMAIL

# --- 4. ПОЛУЧАЕМ EMAIL (с валидацией) ---
async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    if "@" not in email or "." not in email:
        await update.message.reply_text("🤔 Серьезно? Это даже на email не похоже. Давай еще раз, только нормально:")
        return EMAIL
    
    context.user_data['email'] = email
    await update.message.chat.send_action(action="typing")
    
    # Inline-кнопки для выбора темы
    keyboard = [
        [InlineKeyboardButton("💼 Работа", callback_data="Работа")],
        [InlineKeyboardButton("🤝 Сотрудничество", callback_data="Сотрудничество")],
        [InlineKeyboardButton("❓ Вопрос", callback_data="Вопрос")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Ок, email сохранен (обещаю не продавать его спамерам... почти).\nВыбери тему, чтобы я знал, как к этому относиться:",
        reply_markup=reply_markup
    )
    return TOPIC

# --- 5. ПОЛУЧАЕМ ТЕМУ ЧЕРЕЗ КНОПКУ ---
async def get_topic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    context.user_data['topic'] = query.data
    await query.edit_message_text(f"Тема: *{query.data}*. Ну ладно, пойдет.*", parse_mode='Markdown')
    
    await query.message.chat.send_action(action="typing")
    await query.message.reply_text("А теперь напиши само сообщение. Постарайся уложиться в пару предложений 💬")
    return MESSAGE

# --- 6. ПОЛУЧАЕМ СООБЩЕНИЕ И ОТПРАВЛЯЕМ ---
async def get_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['message'] = update.message.text
    
    data = {
        "name": context.user_data['name'],
        "email": context.user_data['email'],
        "topic": context.user_data.get('topic', 'Не указана'),
        "message": context.user_data['message']
    }
    
    await update.message.chat.send_action(action="typing")
    
    try:
        response = requests.post(API_URL, json=data, timeout=10)
        
        if response.status_code in [200, 201]:
            result = response.json()
            bot_id = result.get('id', 'Неизвестно')
            
            logging.info(f"Заявка успешно отправлена. ID: {bot_id}")
            
            phrase = random.choice(SUCCESS_PHRASES)
            
            # Кнопка "Отправить еще"
            keyboard = [[InlineKeyboardButton("🔁 Сделать это еще раз", callback_data="restart")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"✅ {phrase}\n\n"
                f"📋 *Твой номер заявки:* `#{bot_id}`\n"
                f"Сохрани его, вдруг пригодится.",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            logging.error(f"Ошибка сервера: {response.status_code}")
            await update.message.reply_text(f"⚠️ Сервер выдал ошибку {response.status_code}. Какой сюрприз.")
            
    except Exception as e:
        logging.error(f"Ошибка соединения: {e}")
        await update.message.reply_text(
            f"❌ Сервер на 5283 порту, кажется, умер. Или просто устал.\n"
            f"Попробуй позже или проверь, запущен ли C#-сервис.",
            parse_mode='Markdown'
        )
    
    return ConversationHandler.END

# --- 7. КНОПКА "ОТПРАВИТЬ ЕЩЕ" ---
async def restart_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    context.user_data.clear()
    await query.edit_message_text("Еще раз? Ну ок, твой энтузиазм впечатляет. 🔄")
    await query.message.reply_text("Как тебя зовут на этот раз?")
    return NAME

# --- 8. ОТМЕНА (/cancel) ---
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logging.info("Диалог отменен пользователем.")
    await update.message.reply_text("Сдался? Понимаю. Напиши /start, когда наберешься смелости.")
    return ConversationHandler.END

# --- ЗАПУСК ---
def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            TOPIC: [CallbackQueryHandler(get_topic)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message)],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("help", help_command),
        ],
    )

    # Добавляем обработчик для кнопки "Отправить еще" вне ConversationHandler
    application.add_handler(CallbackQueryHandler(restart_button, pattern="^restart$"))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))

    print("🤖 Бот запущен (с ноткой сарказма). Иди в Telegram и напиши /start")
    logging.info("=== Бот успешно запущен ===")
    application.run_polling()

if __name__ == '__main__':
    main()