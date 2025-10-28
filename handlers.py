from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
            [InlineKeyboardButton("Запустить приложение", web_app=WebAppInfo("https://cntr-lounge-app.vercel.app/"))],
            [InlineKeyboardButton("Инстаграм 🫴", url="https://instagram.com/cntr_kimry")],
            [InlineKeyboardButton("Телеграм канал 📱", url="https://t.me/cntr_lounge")],
            [InlineKeyboardButton("ВК 🧍‍♂️", url="https://vk.com/cntr_lounge")],  # Исправлено на url
            [InlineKeyboardButton("Оставить отзыв 🤞", url="https://yandex.ru/maps/org/cntr_lounge/119165709706/reviews/?ll=37.356962%2C56.873082&z=16")]  # Исправлено на url
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Добро пожаловать в CNTR Lounge! Выберите опцию:", reply_markup=reply_markup)
    except Exception as e:
        print(f"Ошибка в start: {e}")
        # Альтернативный вариант без клавиатуры
        await update.message.reply_text("Добро пожаловать в CNTR Lounge!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Этот обработчик теперь будет работать только с callback_data кнопками
    if query.data == "address":
        await query.edit_message_text("Адрес: г. Кимры, ул. Урицкого, д. 5")
    elif query.data == "review":
        await query.edit_message_text("Оставьте свой отзыв, написав сообщение здесь.")

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))