from http.server import BaseHTTPRequestHandler
import json
import os
import requests

BOT_TOKEN = os.environ.get('BOT_TOKEN')

class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"CNTR Bot is running! Send /start in Telegram.")
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            print("📨 Received update:", json.dumps(update, indent=2))
            
            # Обрабатываем сообщение
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                text = update['message']['text'].strip()
                first_name = update['message']['from'].get('first_name', '')
                
                print(f"💬 Message from {first_name}: {text}")
                
                if text == '/start':
                    self.handle_start_command(chat_id, first_name)
                else:
                    self.send_message(chat_id, "Используйте /start для начала работы")
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "processed"}).encode())
            
        except Exception as e:
            print(f"❌ Error: {e}")
            self.send_response(500)
            self.end_headers()
    
    def handle_start_command(self, chat_id, first_name):
        """Обработчик команды /start"""
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "🚀 Запустить приложение", 
                        "web_app": {"url": "https://cntr-lounge-app.vercel.app/"}
                    }
                ],
                [
                    {
                        "text": "📷 Инстаграм", 
                        "url": "https://instagram.com/cntr_kimry"
                    },
                    {
                        "text": "📱 Телеграм канал", 
                        "url": "https://t.me/cntr_lounge"
                    }
                ],
                [
                    {
                        "text": "👥 ВК", 
                        "url": "https://vk.com/cntr_lounge"
                    },
                    {
                        "text": "⭐ Оставить отзыв", 
                        "url": "https://yandex.ru/maps/org/cntr_lounge/119165709706/reviews/"
                    }
                ]
            ]
        }
        
        message_text = f"""
Привет, {first_name}! 👋

Добро пожаловать в CNTR Lounge! 

Здесь вы можете:
• Забронировать столик через наше приложение
• Узнать актуальные новости
• Оставить отзыв о посещении

Выберите нужную опцию ниже ⬇️
        """.strip()
        
        self.send_message(chat_id, message_text, keyboard)
    
    def send_message(self, chat_id, text, reply_markup=None):
        """Отправка сообщения в Telegram"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            data['reply_markup'] = reply_markup
        
        try:
            response = requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                json=data,
                timeout=10
            )
            print(f"📤 Sent message to {chat_id}, status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"⚠️ Telegram API error: {response.text}")
                
        except Exception as e:
            print(f"❌ Failed to send message: {e}")