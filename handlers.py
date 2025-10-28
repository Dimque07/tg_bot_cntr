from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import json

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
            [InlineKeyboardButton("Запустить приложение", web_app=WebAppInfo("https://cntr-lounge-app.vercel.app/"))],
            [InlineKeyboardButton("Инстаграм 🫴", url="https://instagram.com/cntr_kimry")],
            [InlineKeyboardButton("Телеграм канал 📱", url="https://t.me/cntr_lounge")],
            [InlineKeyboardButton("ВК 🧍‍♂️", url="https://vk.com/cntr_lounge")],
            [InlineKeyboardButton("Оставить отзыв 🤞", url="https://yandex.ru/maps/org/cntr_lounge/119165709706/reviews/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Добро пожаловать в CNTR Lounge! Выберите опцию:", reply_markup=reply_markup)
    except Exception as e:
        print(f"Ошибка в start: {e}")
        await update.message.reply_text("Добро пожаловать в CNTR Lounge!")

async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из веб-приложения"""
    try:
        data = json.loads(update.effective_message.web_app_data.data)
        # Здесь можно обработать данные бронирования
        from booking import save_booking
        save_booking(data)
        await update.message.reply_text("✅ Бронирование успешно сохранено!")
    except Exception as e:
        print(f"Ошибка обработки web-app данных: {e}")
        await update.message.reply_text("❌ Произошла ошибка при сохранении бронирования")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "address":
        await query.edit_message_text("Адрес: г. Кимры, ул. Урицкого, д. 5")
    elif query.data == "review":
        await query.edit_message_text("Оставьте свой отзыв, написав сообщение здесь.")

def register_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    app.add_handler(CallbackQueryHandler(button_handler))