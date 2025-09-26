#!/usr/bin/env python3
"""
Проверка статуса бота
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

async def check_bot_status():
    """Проверка статуса бота"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ BOT_TOKEN не найден")
        return False
    
    bot = Bot(token=token)
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} работает!")
        print(f"📱 Имя: {me.first_name}")
        print(f"🆔 ID: {me.id}")
        
        # Проверяем обновления
        updates = await bot.get_updates(limit=5)
        print(f"📨 Последние обновления: {len(updates)}")
        
        if updates:
            print("📝 Последние сообщения:")
            for i, update in enumerate(updates[-3:], 1):  # Показываем последние 3
                if hasattr(update, 'message') and update.message:
                    user = update.message.from_user
                    text = update.message.text or "[не текст]"
                    print(f"   {i}. @{user.username or user.first_name}: {text[:30]}...")
        
        print("\n🎉 Бот готов к тестированию!")
        print("🔗 Ссылка на бота: https://t.me/aawraBot")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False
    
    finally:
        await bot.session.close()

if __name__ == "__main__":
    success = asyncio.run(check_bot_status())
    sys.exit(0 if success else 1)
