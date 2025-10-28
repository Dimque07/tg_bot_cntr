from telegram.ext import ApplicationBuilder, ContextTypes
from config import BOT_TOKEN
from handlers import register_handlers
import os
from telegram import Update
import json

# Создаем приложение
app = ApplicationBuilder().token(BOT_TOKEN).build()
register_handlers(app)

async def on_startup(app):
    print("Бот запущен...")
    # Устанавливаем вебхук при старте
    webhook_url = os.environ.get('WEBHOOK_URL', '') + '/api/webhook'
    if webhook_url:
        await app.bot.set_webhook(webhook_url)

def main_handler(update_data):
    """Обработчик для вебхуков"""
    async def process_update():
        update = Update.de_json(update_data, app.bot)
        await app.process_update(update)
    
    # Запускаем обработку
    import asyncio
    asyncio.run(process_update())

# Для локальной разработки (polling)
def main():
    app.run_polling()

if __name__ == '__main__':
    main()