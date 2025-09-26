#!/usr/bin/env python3
"""
Тест команды /progress
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

# Инициализация
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
db = Database()

@dp.message(Command("progress"))
async def cmd_progress(message: types.Message):
    """Обработчик команды /progress"""
    print(f"🔍 Получена команда /progress от пользователя {message.from_user.id}")
    
    user_id = message.from_user.id
    progress = await db.get_user_progress(user_id)
    
    print(f"📊 Прогресс пользователя: {progress}")
    
    if progress:
        progress_text = format_progress_message(progress)
        
        # Добавляем мотивационное сообщение
        motivation = get_motivational_message()
        progress_text += f"\n💫 *Мотивация:*\n{motivation}"
        
        print(f"📝 Отправляем сообщение: {progress_text[:100]}...")
        
        await message.answer(
            progress_text,
            reply_markup=get_achievements_keyboard(),
            parse_mode="Markdown"
        )
    else:
        progress_text = """
📊 *Ваш прогресс*

Пока у вас нет записанных сессий.
Начните практику, чтобы отслеживать свой прогресс!

💡 Попробуйте позы из каталога или позу дня.
"""
        
        print(f"📝 Отправляем сообщение для нового пользователя")
        
        await message.answer(
            progress_text,
            reply_markup=get_quick_actions_keyboard(),
            parse_mode="Markdown"
        )

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    print(f"🔍 Получена команда /start от пользователя {message.from_user.id}")
    
    user = message.from_user
    
    # Добавляем пользователя в базу данных
    await db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = f"""
🧘‍♀️ *Добро пожаловать в Yoga Learning Bot!*

Привет, {user.first_name}! 👋

Этот бот поможет вам изучить йогу с помощью:
• 📚 Каталога поз с подробными описаниями
• 🎯 Персональных рекомендаций
• 📊 Отслеживания прогресса
• 🧘‍♀️ Позы дня для ежедневной практики

Выберите действие в меню ниже или используйте команды:
/help - помощь
/settings - настройки
/progress - ваш прогресс
"""
    
    await message.answer(
        welcome_text,
        parse_mode="Markdown"
    )

async def main():
    """Основная функция"""
    print("🚀 Запуск тестового бота для проверки /progress")
    
    # Инициализация базы данных
    await db.init_db()
    
    print("✅ База данных инициализирована")
    print("📱 Бот готов к тестированию")
    print("💡 Отправьте /start, затем /progress боту @aawraBot")
    
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
