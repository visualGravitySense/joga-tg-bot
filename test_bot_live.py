#!/usr/bin/env python3
"""
Тест живого бота - проверяем, что бот отвечает на сообщения
"""

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

async def test_live_bot():
    """Тестирование живого бота"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ BOT_TOKEN не найден в .env файле")
        return
    
    bot = Bot(token=token)
    
    try:
        # Получаем информацию о боте
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} активен!")
        print(f"📱 Имя: {me.first_name}")
        print(f"🆔 ID: {me.id}")
        
        # Проверяем, что бот может получать обновления
        print("\n🔍 Проверка получения обновлений...")
        
        # Получаем последние обновления
        updates = await bot.get_updates(limit=1)
        print(f"📨 Получено обновлений: {len(updates)}")
        
        if updates:
            print("✅ Бот получает сообщения!")
            last_update = updates[0]
            if hasattr(last_update, 'message') and last_update.message:
                print(f"📝 Последнее сообщение: {last_update.message.text[:50]}...")
        else:
            print("ℹ️ Нет новых сообщений (это нормально для нового бота)")
        
        print("\n🎉 Бот готов к работе!")
        print("💡 Инструкции для тестирования:")
        print("   1. Откройте Telegram")
        print("   2. Найдите бота: @aawraBot")
        print("   3. Отправьте /start")
        print("   4. Попробуйте команды: /help, /daily, /pose")
        print("   5. Используйте кнопки в меню")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
    
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_live_bot())
