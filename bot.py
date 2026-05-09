import discord
import os
import requests
import re
import asyncio

TOKEN = os.getenv('DISCORD_TOKEN')
FIREBASE_URL = os.getenv('FIREBASE_URL')
TARGET_CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"✅ Бот в сети: {self.user}")
        
        # Подождем 3 секунды, чтобы кэш каналов обновился
        await asyncio.sleep(3)
        
        channel = self.get_channel(TARGET_CHANNEL_ID)
        if channel:
            print(f"🎯 ЦЕЛЬ НАЙДЕНА: #{channel.name}")
            print(f"📡 Слушаю канал {TARGET_CHANNEL_ID}...")
        else:
            print(f"❌ ОШИБКА: Канал {TARGET_CHANNEL_ID} не найден!")
            print("Возможные причины:")
            print("1. Бот (твой аккаунт) не состоит на этом сервере.")
            print("2. У тебя нет прав на просмотр этого канала.")
            print("3. В секретах GitHub указан неверный ID.")

    async def on_message(self, message):
        if message.channel.id != TARGET_CHANNEL_ID:
            return

        if message.author == self.user:
            return

        # Поиск JobID
        match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', message.content.lower())
        
        if match:
            job_id = match.group(1)
            print(f"💎 НАЙДЕН СЕРВЕР: {job_id}")
            
            payload = {
                "jobId": job_id,
                "time": str(message.created_at.strftime("%H:%M:%S"))
            }
            
            try:
                r = requests.put(FIREBASE_URL, json=payload)
                if r.status_code == 200:
                    print("🔥 Firebase обновлен!")
            except Exception as e:
                print(f"❌ Ошибка отправки: {e}")

client = MyClient()
client.run(TOKEN)
