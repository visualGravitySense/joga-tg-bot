#!/usr/bin/env python3
"""
Тест подключения к Telegram Bot API
"""

import asyncio
import os
from aiogram import Bot

async def test_bot_connection():
    """Тестирование подключения к боту"""
    # Токен бота
    token = "6323610595:AAHa3Jj237fKuToxDBPIqVeMNB5wIVAiSHg"
    
    try:
        print("🔗 Подключение к Telegram Bot API...")
        bot = Bot(token=token)
        
        # Получаем информацию о боте
        me = await bot.get_me()
        
        print("✅ Бот подключен успешно!")
        print(f"📱 Имя бота: {me.first_name}")
        print(f"🤖 Username: @{me.username}")
        print(f"🆔 ID бота: {me.id}")
        # print(f"📝 Описание: {me.description or 'Не указано'}")
        
        # Закрываем соединение
        await bot.session.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_bot_connection())
    if success:
        print("\n🎉 Бот готов к работе!")
        print("💡 Теперь вы можете запустить бота командой: python run.py")
    else:
        print("\n❌ Проверьте токен бота и подключение к интернету")
