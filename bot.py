import discord
import os
import requests
import re

TOKEN = os.getenv('DISCORD_TOKEN')
FIREBASE_URL = os.getenv('FIREBASE_URL')
TARGET_CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Бот запущен: {self.user}")
        
        # Проверяем, видит ли бот нужный канал
        channel = self.get_channel(TARGET_CHANNEL_ID)
        if channel:
            print(f"🎯 ЦЕЛЬ НАЙДЕНА: #{channel.name} (ID: {TARGET_CHANNEL_ID})")
            print("🚀 Ожидаю сообщения с JobID...")
        else:
            print(f"❌ ОШИБКА: Канал с ID {TARGET_CHANNEL_ID} не найден!")
            print("Проверь, есть ли у твоего аккаунта доступ к этому каналу.")

    async def on_message(self, message):
        if message.channel.id != TARGET_CHANNEL_ID:
            return

        if message.author == self.user:
            return

        # Ищем JobID (формат 8-4-4-4-12)
        match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', message.content.lower())
        
        if match:
            job_id = match.group(1)
            print(f"💎 Нашел сервер! ID: {job_id}")
            
            payload = {
                "jobId": job_id,
                "time": str(message.created_at.strftime("%H:%M:%S"))
            }
            
            r = requests.put(FIREBASE_URL, json=payload)
            if r.status_code == 200:
                print("🔥 Firebase обновлен!")

client = MyClient()
client.run(TOKEN)
