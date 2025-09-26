#!/usr/bin/env python3
"""
Симуляция команды /progress для тестирования
"""

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database import Database
from ui_enhancements import format_progress_message, get_motivational_message, get_achievements_keyboard, get_quick_actions_keyboard

load_dotenv()

async def simulate_progress_command():
    """Симуляция команды /progress"""
    print("🧘 Симуляция команды /progress")
    print("=" * 50)
    
    # Инициализация базы данных
    db = Database()
    await db.init_db()
    
    # Тестовый пользователь
    test_user_id = 12345
    
    print("1️⃣ Создание тестового пользователя...")
    await db.add_user(
        user_id=test_user_id,
        username="test_user",
        first_name="Test",
        last_name="User"
    )
    print("✅ Пользователь создан")
    
    print("\n2️⃣ Добавление тестовых данных...")
    # Добавляем несколько сессий
    await db.add_user_session(
        user_id=test_user_id,
        pose_id=1,
        duration_seconds=300,  # 5 минут
        rating=5,
        notes="Отличная поза для начинающих!"
    )
    
    await db.add_user_session(
        user_id=test_user_id,
        pose_id=2,
        duration_seconds=600,  # 10 минут
        rating=4,
        notes="Хорошая растяжка"
    )
    
    # Обновляем прогресс
    await db.update_user_progress(
        user_id=test_user_id,
        total_sessions=2,
        total_duration=900,  # 15 минут
        current_streak=2,
        longest_streak=2
    )
    print("✅ Тестовые данные добавлены")
    
    print("\n3️⃣ Тестирование функции /progress...")
    
    # Получаем прогресс
    progress = await db.get_user_progress(test_user_id)
    print(f"📊 Прогресс: {progress}")
    
    if progress:
        # Форматируем сообщение
        progress_text = format_progress_message(progress)
        
        # Добавляем мотивационное сообщение
        motivation = get_motivational_message()
        progress_text += f"\n💫 *Мотивация:*\n{motivation}"
        
        print("✅ Сообщение сформировано:")
        print(progress_text)
        
        # Проверяем клавиатуру
        keyboard = get_achievements_keyboard()
        print(f"✅ Клавиатура создана: {type(keyboard)}")
        
    else:
        progress_text = """
📊 *Ваш прогресс*

Пока у вас нет записанных сессий.
Начните практику, чтобы отслеживать свой прогресс!

💡 Попробуйте позы из каталога или позу дня.
"""
        print("✅ Сообщение для нового пользователя:")
        print(progress_text)
        
        keyboard = get_quick_actions_keyboard()
        print(f"✅ Клавиатура создана: {type(keyboard)}")
    
    print("\n4️⃣ Тестирование с реальным ботом...")
    
    # Создаем бота
    bot = Bot(token=BOT_TOKEN)
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} готов")
        
        # Отправляем тестовое сообщение
        await bot.send_message(
            chat_id=test_user_id,
            text="🧘 Тест функции /progress\n\n" + progress_text,
            parse_mode="Markdown"
        )
        print("✅ Тестовое сообщение отправлено")
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
    
    finally:
        await bot.session.close()
    
    print("\n🎉 Симуляция завершена!")
    print("💡 Теперь попробуйте отправить /progress боту @aawraBot")

if __name__ == "__main__":
    asyncio.run(simulate_progress_command())
