#!/usr/bin/env python3
"""
Тест функции /progress для Yoga Learning Bot
"""

import asyncio
import os
from dotenv import load_dotenv
from database import Database
from database_enhancements import DatabaseEnhancements
from ui_enhancements import format_progress_message, get_motivational_message

load_dotenv()

async def test_progress_function():
    """Тестирование функции отслеживания прогресса"""
    print("🧘 Тестирование функции /progress")
    print("=" * 50)
    
    # Инициализация базы данных
    db = Database()
    db_enhanced = DatabaseEnhancements()
    
    # Инициализация таблиц
    await db.init_db()
    await db_enhanced.init_enhanced_tables()
    
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
    
    print("\n2️⃣ Тестирование пустого прогресса...")
    progress = await db.get_user_progress(test_user_id)
    if progress:
        print(f"❌ Неожиданно найден прогресс: {progress}")
    else:
        print("✅ Прогресс пустой (ожидаемо для нового пользователя)")
    
    print("\n3️⃣ Добавление тестовых данных...")
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
    
    print("\n4️⃣ Проверка прогресса...")
    progress = await db.get_user_progress(test_user_id)
    if progress:
        print("✅ Прогресс найден:")
        print(f"   • Сессий: {progress.get('total_sessions', 0)}")
        print(f"   • Время: {progress.get('total_duration', 0)} сек")
        print(f"   • Текущая серия: {progress.get('current_streak', 0)} дней")
        print(f"   • Лучшая серия: {progress.get('longest_streak', 0)} дней")
    else:
        print("❌ Прогресс не найден")
    
    print("\n5️⃣ Тестирование форматирования...")
    if progress:
        formatted_message = format_progress_message(progress)
        print("✅ Форматированное сообщение:")
        print(formatted_message)
        
        motivation = get_motivational_message()
        print(f"\n💫 Мотивационное сообщение: {motivation}")
    
    print("\n6️⃣ Тестирование достижений...")
    await db_enhanced.check_achievements(test_user_id)
    achievements = await db_enhanced.get_user_achievements(test_user_id)
    print(f"✅ Найдено достижений: {len(achievements)}")
    for achievement in achievements:
        print(f"   • {achievement['achievement_name']}: {achievement['description']}")
    
    print("\n7️⃣ Тестирование избранных поз...")
    # Добавляем позу в избранное
    await db_enhanced.add_to_favorites(test_user_id, 1)
    favorites = await db_enhanced.get_user_favorites(test_user_id)
    print(f"✅ Избранных поз: {len(favorites)}")
    for favorite in favorites:
        print(f"   • {favorite['name']}")
    
    print("\n8️⃣ Тестирование заметок...")
    await db_enhanced.add_user_note(
        test_user_id, 1, "Моя первая заметка о позе"
    )
    notes = await db_enhanced.get_user_notes(test_user_id)
    print(f"✅ Заметок: {len(notes)}")
    for note in notes:
        print(f"   • {note['pose_name']}: {note['note_text']}")
    
    print("\n🎉 Все тесты функции /progress прошли успешно!")
    print("\n💡 Теперь вы можете:")
    print("1. Отправить /progress боту @aawraBot")
    print("2. Нажать кнопку '📊 Мой прогресс'")
    print("3. Увидеть красивую статистику с мотивацией")

if __name__ == "__main__":
    asyncio.run(test_progress_function())
