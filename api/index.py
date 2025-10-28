from http.server import BaseHTTPRequestHandler
import os
import json
from bot import main_handler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            update = json.loads(post_data.decode('utf-8'))
            # Эмулируем объект Update для python-telegram-bot
            from telegram import Update
            from telegram.ext import ContextTypes
            
            # Здесь нужно преобразовать данные для обработки
            # Это упрощенная версия - вам может понадобиться адаптация
            result = main_handler(update)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            
        except Exception as e:
            print(f"Error: {e}")
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running on Vercel!")