import discord
import os
import requests
import json
import re

# Загрузка секретов из GitHub
TOKEN = os.getenv('DISCORD_TOKEN')
GIST_TOKEN = os.getenv('GIST_TOKEN')
GIST_ID = os.getenv('GIST_ID')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Инициализация клиента (для discord.py-self)
client = discord.Client()

@client.event
async def on_ready():
    print(f"✅ Бот запущен!")
    print(f"👤 Аккаунт: {client.user}")
    print(f"📡 Мониторинг канала: {CHANNEL_ID}")

@client.event
async def on_message(message):
    # Фильтр по ID канала
    if message.channel.id == CHANNEL_ID:
        
        # Поиск JobId через регулярное выражение
        job_id_match = re.search(r'([a-f0-9\-]{36})', message.content)
        
        if job_id_match:
            job_id = job_id_match.group(1)
            print(f"💎 Нашел JobId: {job_id}. Обновляю Gist...")
            
            url = f"https://api.github.com/gists/{GIST_ID}"
            headers = {
                "Authorization": f"token {GIST_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Данные для записи в файл
            content_data = {
                "jobId": job_id,
                "info": "Rich Server Found",
                "time": str(message.created_at)
            }
            
            payload = {
                "files": {
                    "servers.json": {
                        "content": json.dumps(content_data, indent=4)
                    }
                }
            }
            
            try:
                r = requests.patch(url, headers=headers, json=payload)
                if r.status_code == 200:
                    print("🚀 Gist успешно обновлен!")
                else:
                    print(f"⚠️ Ошибка API: {r.status_code}")
            except Exception as e:
                print(f"❌ Ошибка: {e}")

# Запуск бота (без аргумента bot=False, так как библиотека сама всё поймет)
client.run(TOKEN)
