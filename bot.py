import discord
import os
import requests
import json
import re

# Загрузка секретов из GitHub (настрой их во вкладке Secrets)
TOKEN = os.getenv('DISCORD_TOKEN')
GIST_TOKEN = os.getenv('GIST_TOKEN')
GIST_ID = os.getenv('GIST_ID')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Используем Client для селф-бота (проще и стабильнее)
client = discord.Client()

@client.event
async def on_ready():
    print(f"✅ Бот успешно запущен!")
    print(f"👤 Аккаунт: {client.user}")
    print(f"📡 Слушаю канал: {CHANNEL_ID}")

@client.event
async def on_message(message):
    # Проверяем, что сообщение пришло именно из нужного канала
    if message.channel.id == CHANNEL_ID:
        
        # Ищем JobId (строка из 36 символов: цифры, буквы и дефисы)
        job_id_match = re.search(r'([a-f0-9\-]{36})', message.content)
        
        if job_id_match:
            job_id = job_id_match.group(1)
            print(f"💎 Нашел JobId: {job_id}. Обновляю Gist...")
            
            # Ссылка на API твоего Гиста
            url = f"https://api.github.com/gists/{GIST_ID}"
            headers = {
                "Authorization": f"token {GIST_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Содержимое, которое запишем в servers.json
            content_data = {
                "jobId": job_id,
                "server_info": "Rich Server Found",
                "raw_text": message.content[:100], # Кусочек текста лога для проверки
                "time": str(message.created_at)
            }
            
            # Формируем запрос к GitHub API
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
                    print("🚀 Gist успешно обновлен! Можно заходить.")
                else:
                    print(f"⚠️ Ошибка GitHub API: {r.status_code}")
                    print(f"Ответ: {r.text}")
            except Exception as e:
                print(f"❌ Ошибка при отправке: {e}")

# Запуск бота
client.run(TOKEN, bot=False)
