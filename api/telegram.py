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
        response = "✅ Telegram Bot Endpoint is WORKING!\n"
        response += f"✅ BOT_TOKEN: {bool(BOT_TOKEN)}\n"
        response += f"✅ Path: {self.path}"
        self.wfile.write(response.encode())
    
    def do_POST(self):
        print("🔔 POST request received!")
        
        # Сразу отвечаем 200 OK
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "message": "received"}).encode())
        
        # Обрабатываем данные
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = json.loads(post_data.decode('utf-8'))
            
            print(f"📨 Update: {json.dumps(update, indent=2)}")
            
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                text = update['message'].get('text', '')
                user_name = update['message']['from'].get('first_name', 'User')
                
                print(f"💬 From {user_name}: {text}")
                
                if '/start' in text:
                    print("🎯 Processing /start command")
                    self.send_telegram_response(
                        chat_id, 
                        f"🎉 ПРИВЕТ, {user_name}! БОТ ЗАРАБОТАЛ!\n\nЭто тестовое сообщение с Vercel!"
                    )
                    
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def send_telegram_response(self, chat_id, text):
        if not BOT_TOKEN:
            print("❌ BOT_TOKEN not set!")
            return
            
        try:
            url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
            data = {
                'chat_id': chat_id,
                'text': text
            }
            
            print(f"📤 Sending to Telegram: {data}")
            response = requests.post(url, json=data, timeout=10)
            print(f"📨 Response: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"❌ Failed to send: {e}")