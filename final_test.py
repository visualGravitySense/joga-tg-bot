#!/usr/bin/env python3
"""
Финальный тест Yoga Learning Bot
"""

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

async def final_test():
    """Финальный тест всех компонентов бота"""
    print("🧘 Финальный тест Yoga Learning Bot")
    print("=" * 50)
    
    # Тест 1: Подключение к боту
    print("1️⃣ Тестирование подключения к боту...")
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ BOT_TOKEN не найден")
        return False
    
    bot = Bot(token=token)
    try:
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} активен")
        print(f"📱 Имя: {me.first_name}")
        print(f"🆔 ID: {me.id}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False
    
    # Тест 2: Получение сообщений
    print("\n2️⃣ Тестирование получения сообщений...")
    try:
        updates = await bot.get_updates(limit=5)
        print(f"✅ Получено {len(updates)} обновлений")
        if updates:
            print("📝 Последние сообщения:")
            for i, update in enumerate(updates[-3:], 1):
                if hasattr(update, 'message') and update.message:
                    user = update.message.from_user
                    text = update.message.text or "[не текст]"
                    print(f"   {i}. @{user.username or user.first_name}: {text[:30]}...")
    except Exception as e:
        print(f"❌ Ошибка получения сообщений: {e}")
        return False
    
    # Тест 3: Проверка файлов проекта
    print("\n3️⃣ Проверка файлов проекта...")
    required_files = [
        'bot.py', 'database.py', 'yoga_data.py', 'config.py',
        'README.md', 'requirements.txt', '.env'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {missing_files}")
        return False
    else:
        print("✅ Все необходимые файлы присутствуют")
    
    # Тест 4: Проверка импортов
    print("\n4️⃣ Тестирование импортов...")
    try:
        import aiosqlite
        import pandas
        import numpy
        print("✅ Все зависимости импортируются успешно")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    
    await bot.session.close()
    
    print("\n🎉 Все тесты пройдены успешно!")
    print("\n📋 Информация о боте:")
    print(f"🤖 Username: @{me.username}")
    print(f"🔗 Ссылка: https://t.me/{me.username}")
    print(f"📱 Имя: {me.first_name}")
    print(f"🆔 ID: {me.id}")
    
    print("\n💡 Инструкции для тестирования:")
    print("1. Откройте Telegram")
    print(f"2. Найдите бота: @{me.username}")
    print("3. Отправьте /start")
    print("4. Попробуйте команды: /help, /daily, /pose")
    print("5. Используйте кнопки в меню")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(final_test())
    if success:
        print("\n✅ Yoga Learning Bot готов к использованию!")
    else:
        print("\n❌ Есть проблемы, требующие исправления")
