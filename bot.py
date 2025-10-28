from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from handlers import register_handlers

async def on_startup(app):
    print("Бот запущен...")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(on_startup).build()
    register_handlers(app)
    app.run_polling()

if __name__ == '__main__':
    main()
