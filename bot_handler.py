import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json

class BotHandler:
    def __init__(self):
        self.BOT_TOKEN = os.environ.get('BOT_TOKEN')
        self.app = None
        self.initialize_bot()
    
    def initialize_bot(self):
        """Инициализация бота"""
        if self.BOT_TOKEN:
            self.app = ApplicationBuilder().token(self.BOT_TOKEN).build()
            self.register_handlers()
    
    def register_handlers(self):
        """Регистрация обработчиков"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        try:
            keyboard = [
                [InlineKeyboardButton("Запустить приложение", web_app=WebAppInfo("https://cntr-lounge-app.vercel.app/"))],
                [InlineKeyboardButton("Инстаграм 🫴", url="https://instagram.com/cntr_kimry")],
                [InlineKeyboardButton("Телеграм канал 📱", url="https://t.me/cntr_lounge")],
                [InlineKeyboardButton("ВК 🧍‍♂️", url="https://vk.com/cntr_lounge")],
                [InlineKeyboardButton("Оставить отзыв 🤞", url="https://yandex.ru/maps/org/cntr_lounge/119165709706/reviews/")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Добро пожаловать в CNTR Lounge! Выберите опцию:", 
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error in start: {e}")
            await update.message.reply_text("Добро пожаловать в CNTR Lounge!")
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик inline кнопок"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "address":
            await query.edit_message_text("📍 Адрес: г. Кимры, ул. Урицкого, д. 5")
        elif query.data == "review":
            await query.edit_message_text("💬 Оставьте свой отзыв, написав сообщение здесь.")
    
    async def process_update(self, update_data):
        """Обработка обновления от Telegram"""
        if self.app:
            update = Update.de_json(update_data, self.app.bot)
            await self.app.process_update(update)

# Глобальный экземпляр бота
bot_handler = BotHandler()