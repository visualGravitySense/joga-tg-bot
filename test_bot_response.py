#!/usr/bin/env python3
"""
Тест ответов бота
"""

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

async def test_bot_responses():
    """Тестирование ответов бота"""
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token=token)
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} активен!")
        print(f"📱 Имя: {me.first_name}")
        print(f"🆔 ID: {me.id}")
        
        # Получаем последние обновления
        updates = await bot.get_updates(limit=10)
        print(f"📨 Получено обновлений: {len(updates)}")
        
        if updates:
            print("📝 Последние сообщения:")
            for i, update in enumerate(updates[-5:], 1):
                if hasattr(update, 'message') and update.message:
                    user = update.message.from_user
                    text = update.message.text or "[не текст]"
                    print(f"   {i}. @{user.username or user.first_name}: {text[:50]}...")
        
        print("\n🎉 Бот готов к тестированию!")
        print("💡 Инструкции:")
        print("1. Откройте Telegram")
        print("2. Найдите бота: @aawraBot")
        print("3. Отправьте /start")
        print("4. Попробуйте команды: /help, /daily, /pose")
        print("5. Используйте кнопки в меню")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_bot_responses())
