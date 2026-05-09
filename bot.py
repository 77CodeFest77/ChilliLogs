import discord
from discord.ext import commands
import os
import requests
import json

# Загрузка настроек из секретов GitHub
TOKEN = os.getenv('DISCORD_TOKEN')
FB_URL = os.getenv('FIREBASE_URL') + "current_server.json"
TARGET_CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

# Настройка селф-бота (работает через твой личный аккаунт)
bot = commands.Bot(command_prefix="!", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Бот авторизован: {bot.user}")
    print(f"📡 Мониторинг канала: {TARGET_CHANNEL_ID}")

@bot.event
async def on_message(message):
    # Слушаем только конкретный канал с логами
    if message.channel.id == TARGET_CHANNEL_ID:
        # Проверяем наличие JobId (ключ к серверу)
        if "JobId" in message.content:
            print("🚀 Обнаружен богатый сервер! Отправляю в Firebase...")
            
            # Формируем данные
            payload = {
                "log_text": message.content,
                "time": str(message.created_at),
                "author": str(message.author)
            }
            
            # Отправка в Firebase
            try:
                response = requests.put(FB_URL, json=payload)
                if response.status_code == 200:
                    print("💎 Данные успешно записаны в базу.")
                else:
                    print(f"⚠️ Ошибка базы: {response.status_code}")
            except Exception as e:
                print(f"❌ Ошибка запроса: {e}")

bot.run(TOKEN)

