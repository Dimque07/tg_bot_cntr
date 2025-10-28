from flask import Flask, request, jsonify
import os
import json
import asyncio
from bot_handler import bot_handler

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>CNTR Telegram Bot</h1>
    <p>Bot is running on Vercel!</p>
    <p><a href="/set_webhook">Set Webhook</a></p>
    <p><a href="/webhook_info">Get Webhook Info</a></p>
    """

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработчик вебхуков от Telegram"""
    if request.is_json:
        update = request.get_json()
        print("Received update:", update)
        
        # Асинхронная обработка обновления
        try:
            if bot_handler.app:
                asyncio.run(bot_handler.process_update(update))
            return jsonify({"status": "ok"})
        except Exception as e:
            print(f"Error processing update: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return jsonify({"error": "Invalid data"}), 400

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука"""
    webhook_url = f"https://{request.host}/webhook"
    bot_token = os.environ.get('BOT_TOKEN')
    
    if not bot_token:
        return "BOT_TOKEN not set in environment variables", 500
    
    set_webhook_url = f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}"
    
    return f"""
    <h1>Set Webhook</h1>
    <p>Bot Token: {bot_token[:10]}...</p>
    <p>Webhook URL: {webhook_url}</p>
    <p>Set webhook URL: <a href="{set_webhook_url}">{set_webhook_url}</a></p>
    <p><a href="{set_webhook_url}" target="_blank">Click here to set webhook</a></p>
    """

@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    """Получение информации о вебхуке"""
    import requests
    bot_token = os.environ.get('BOT_TOKEN')
    
    if not bot_token:
        return "BOT_TOKEN not set", 500
    
    response = requests.get(f"https://api.telegram.org/bot{bot_token}/getWebhookInfo")
    return jsonify(response.json())

# Для локальной разработки
if __name__ == '__main__':
    app.run(debug=True)