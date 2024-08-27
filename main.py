import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего бота
TELEGRAM_TOKEN = '7338560584:AAE_Toy6YD1IcgOoilbLnj8ZZvIdrhXqm9Y'

# ID канала, куда будут отправляться отзывы
CHANNEL_ID = '-1002214625883'  # Замените на правильный chat_id вашего канала

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение с кнопками"""
    keyboard = [
        [InlineKeyboardButton("Категории фитнес-видео", callback_data='choose_category')],
        [InlineKeyboardButton("Оставить отзыв", callback_data='leave_feedback')],
        [InlineKeyboardButton("Посмотреть отзывы", callback_data='view_feedback')],
        [InlineKeyboardButton("Записаться на фитнес курсы", callback_data='enroll_courses')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    """Обрабатывает нажатие кнопок"""
    query = update.callback_query
    await query.answer()

    if query.data == 'choose_category':
        await choose_category(update, context)
    elif query.data.startswith('category_'):
        await choose_video(update, context, query.data.split('_')[1])
    elif query.data.startswith('video_'):
        await send_video_link(update, context, query.data.split('_')[1])
    elif query.data == 'leave_feedback':
        await leave_feedback(update, context)
    elif query.data == 'view_feedback':
        await view_feedback(update, context)
    elif query.data == 'enroll_courses':
        await enroll_courses(update, context)

async def choose_category(update: Update, context: CallbackContext) -> None:
    """Выбор категории фитнес-видео"""
    keyboard = [
        [InlineKeyboardButton("Йога", callback_data='category_yoga')],
        [InlineKeyboardButton("Силовые тренировки", callback_data='category_strength')],
        [InlineKeyboardButton("Кардио", callback_data='category_cardio')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text('Выберите категорию:', reply_markup=reply_markup)

async def choose_video(update: Update, context: CallbackContext, category: str) -> None:
    """Выбор видео в зависимости от категории"""
    videos = {
        'yoga': [
            ('Йога для начинающих', 'https://www.youtube.com/watch?v=link1'),
            ('Йога для расслабления', 'https://www.youtube.com/watch?v=link2'),
            ('Йога для гибкости', 'https://www.youtube.com/watch?v=link3'),
        ],
        'strength': [
            ('Силовая тренировка для дома', 'https://www.youtube.com/watch?v=link4'),
            ('Тренировка на силу для ног', 'https://www.youtube.com/watch?v=link5'),
            ('Силовая тренировка с гантелями', 'https://www.youtube.com/watch?v=link6'),
        ],
        'cardio': [
            ('Кардио тренировка для сжигания жира', 'https://www.youtube.com/watch?v=link7'),
            ('Кардио тренировка дома', 'https://www.youtube.com/watch?v=link8'),
            ('Интенсивное кардио для начинающих', 'https://www.youtube.com/watch?v=link9'),
        ],
    }
    
    keyboard = []
    for title, link in videos.get(category, []):
        keyboard.append([InlineKeyboardButton(title, callback_data=f'video_{link}')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text('Выберите видео:', reply_markup=reply_markup)

async def send_video_link(update: Update, context: CallbackContext, link: str) -> None:
    """Отправляет ссылку на видео"""
    await update.callback_query.message.reply_text(f"Ваше видео: {link}")

async def leave_feedback(update: Update, context: CallbackContext) -> None:
    """Просит пользователя оставить отзыв"""
    await update.callback_query.message.reply_text('Пожалуйста, отправьте ваш отзыв текстовым сообщением.')

    # Установка состояния для следующего сообщения
    context.user_data['awaiting_feedback'] = True

async def view_feedback(update: Update, context: CallbackContext) -> None:
    """Отправляет сообщение со ссылкой на канал отзывов"""
    await update.callback_query.message.reply_text(f"Посмотреть отзывы можно здесь: https://t.me/+10Hkq3tJNbA5ZDky")

async def enroll_courses(update: Update, context: CallbackContext) -> None:
    """Отправляет описание курсов и ссылку на менеджера"""
    description = (
        "Самые лучшие фитнес курсы в Узбекистане.\n"
        "Для записи на курсы и информации о них пожалуйста, свяжитесь с нашим менеджером по ссылке: https://t.me/gk_sh_29"
    )
    await update.callback_query.message.reply_text(description)

async def handle_feedback(update: Update, context: CallbackContext) -> None:
    """Обрабатывает отзыв пользователя"""
    if context.user_data.get('awaiting_feedback') and update.message:
        feedback = update.message.text
        user = update.message.from_user
        user_info = f"Отзыв от @{user.username}" if user.username else f"Отзыв от {user.first_name}"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=f"{user_info}\n\nНовый отзыв:\n{feedback}")
        await update.message.reply_text("Спасибо за ваш отзыв!")
        context.user_data['awaiting_feedback'] = False

def main() -> None:
    """Запускает бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    start_handler = CommandHandler("start", start)
    button_handler = CallbackQueryHandler(button)
    feedback_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_feedback)
    
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(feedback_handler)
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
