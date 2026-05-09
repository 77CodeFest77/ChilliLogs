import discord
import os
import requests
import json
import re

# Настройки из секретов GitHub
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
# Твоя ссылка на Firebase (обязательно с /.json в конце)
FIREBASE_URL = "https://serveraj-eb052-default-rtdb.firebaseio.com/.json"

client = discord.Client()

@client.event
async def on_ready():
    print(f"✅ Бот в сети: {client.user}")

@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID:
        # Ищем JobId в сообщении
        job_id_match = re.search(r'([a-f0-9\-]{36})', message.content)
        
        if job_id_match:
            job_id = job_id_match.group(1)
            print(f"🔥 Найден ID: {job_id}. Отправляю в Firebase...")
            
            # Данные для базы
            payload = {
                "jobId": job_id,
                "time": str(message.created_at.strftime("%H:%M:%S")),
                "server_text": message.content[:50]
            }
            
            try:
                # В Firebase используем PUT, чтобы перезаписывать данные
                r = requests.put(FIREBASE_URL, json=payload)
                if r.status_code == 200:
                    print("🚀 Firebase успешно обновлен!")
                else:
                    print(f"⚠️ Ошибка Firebase: {r.status_code}")
            except Exception as e:
                print(f"❌ Ошибка: {e}")

client.run(TOKEN)
