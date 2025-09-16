"""
Упрощенная демонстрация Yoga Learning Bot без aiosqlite
"""

import sqlite3
import json
import random
from pathlib import Path

def create_simple_database():
    """Создание простой базы данных SQLite"""
    print("🗄️ Создание базы данных...")
    
    conn = sqlite3.connect("simple_yoga_demo.db")
    cursor = conn.cursor()
    
    # Создаем таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS yoga_poses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sanskrit_name TEXT,
            category TEXT,
            difficulty_level TEXT,
            description TEXT,
            benefits TEXT,
            instructions TEXT,
            duration_seconds INTEGER DEFAULT 30
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            level TEXT DEFAULT 'beginner'
        )
    """)
    
    conn.commit()
    return conn, cursor

def add_sample_poses(cursor):
    """Добавление примеров поз йоги"""
    print("🧘 Добавление поз йоги...")
    
    poses = [
        ("Поза горы", "Tadasana", "standing", "beginner", 
         "Базовая стоячая поза", "Улучшает осанку", "Встаньте прямо", 30),
        ("Поза дерева", "Vrikshasana", "balance", "beginner",
         "Поза равновесия", "Развивает баланс", "Стойте на одной ноге", 45),
        ("Поза собаки мордой вниз", "Adho Mukha Svanasana", "inversion", "beginner",
         "Перевернутая поза", "Укрепляет руки", "Образуйте треугольник телом", 60),
        ("Поза воина I", "Virabhadrasana I", "standing", "intermediate",
         "Сильная стоячая поза", "Укрепляет ноги", "Сделайте выпад вперед", 45),
        ("Поза кобры", "Bhujangasana", "backbend", "beginner",
         "Поза лежа с прогибом", "Укрепляет спину", "Поднимите грудь", 30),
        ("Поза ребенка", "Balasana", "resting", "beginner",
         "Расслабляющая поза", "Снимает стресс", "Опуститесь на колени", 90),
        ("Поза кошки", "Marjariasana", "on_knees", "beginner",
         "Поза на четвереньках", "Улучшает гибкость", "Прогибайте спину", 60),
        ("Поза моста", "Setu Bandhasana", "backbend", "beginner",
         "Поза лежа с подъемом", "Укрепляет ягодицы", "Поднимите таз", 45),
        ("Поза лотоса", "Padmasana", "seated", "intermediate",
         "Медитативная поза", "Развивает гибкость", "Скрестите ноги", 120),
        ("Поза трупа", "Shavasana", "resting", "beginner",
         "Финальная поза", "Полное расслабление", "Лягте и расслабьтесь", 300)
    ]
    
    cursor.executemany("""
        INSERT INTO yoga_poses (name, sanskrit_name, category, difficulty_level, 
                              description, benefits, instructions, duration_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, poses)
    
    print(f"✅ Добавлено {len(poses)} поз")

def add_sample_user(cursor):
    """Добавление примера пользователя"""
    print("👤 Добавление пользователя...")
    
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, username, first_name, last_name, level)
        VALUES (?, ?, ?, ?, ?)
    """, (12345, "demo_user", "Demo", "User", "beginner"))
    
    print("✅ Пользователь добавлен")

def demo_queries(cursor):
    """Демонстрация различных запросов"""
    print("\n📊 Демонстрация запросов:")
    print("=" * 50)
    
    # Все позы
    cursor.execute("SELECT COUNT(*) FROM yoga_poses")
    total_poses = cursor.fetchone()[0]
    print(f"✅ Всего поз в базе: {total_poses}")
    
    # Позы по категориям
    cursor.execute("SELECT category, COUNT(*) FROM yoga_poses GROUP BY category")
    categories = cursor.fetchall()
    print("📂 Позы по категориям:")
    for category, count in categories:
        print(f"   • {category}: {count} поз")
    
    # Позы по сложности
    cursor.execute("SELECT difficulty_level, COUNT(*) FROM yoga_poses GROUP BY difficulty_level")
    difficulties = cursor.fetchall()
    print("⭐ Позы по сложности:")
    for difficulty, count in difficulties:
        print(f"   • {difficulty}: {count} поз")
    
    # Случайная поза для начинающих
    cursor.execute("""
        SELECT name, sanskrit_name, description, duration_seconds 
        FROM yoga_poses 
        WHERE difficulty_level = 'beginner' 
        ORDER BY RANDOM() 
        LIMIT 1
    """)
    random_pose = cursor.fetchone()
    if random_pose:
        print(f"\n🎲 Случайная поза для начинающих:")
        print(f"   • Название: {random_pose[0]}")
        print(f"   • Санскрит: {random_pose[1]}")
        print(f"   • Описание: {random_pose[2]}")
        print(f"   • Продолжительность: {random_pose[3]} сек")
    
    # Поиск поз
    cursor.execute("""
        SELECT name, category FROM yoga_poses 
        WHERE name LIKE '%поза%' OR sanskrit_name LIKE '%asana%'
    """)
    search_results = cursor.fetchall()
    print(f"\n🔍 Поиск 'поза': найдено {len(search_results)} результатов")
    for name, category in search_results[:3]:
        print(f"   • {name} ({category})")

def demo_user_features(cursor):
    """Демонстрация функций пользователя"""
    print("\n👤 Демонстрация функций пользователя:")
    print("=" * 50)
    
    # Получаем пользователя
    cursor.execute("SELECT * FROM users WHERE user_id = 12345")
    user = cursor.fetchone()
    if user:
        print(f"✅ Пользователь: {user[2]} {user[3]} (уровень: {user[4]})")
    
    # Рекомендации для пользователя
    cursor.execute("""
        SELECT name, category, duration_seconds 
        FROM yoga_poses 
        WHERE difficulty_level = 'beginner' 
        ORDER BY RANDOM() 
        LIMIT 3
    """)
    recommendations = cursor.fetchall()
    print(f"\n🎯 Рекомендации для начинающих:")
    for i, (name, category, duration) in enumerate(recommendations, 1):
        print(f"   {i}. {name} ({category}) - {duration} сек")
    
    # Статистика по продолжительности
    cursor.execute("SELECT AVG(duration_seconds) FROM yoga_poses")
    avg_duration = cursor.fetchone()[0]
    print(f"\n⏱️ Средняя продолжительность поз: {avg_duration:.1f} секунд")

def demo_bot_commands():
    """Демонстрация команд бота"""
    print("\n🤖 Демонстрация команд бота:")
    print("=" * 50)
    
    commands = [
        ("/start", "Начать работу с ботом"),
        ("/help", "Показать справку"),
        ("/daily", "Получить позу дня"),
        ("/pose", "Случайная поза"),
        ("/progress", "Ваш прогресс"),
        ("/settings", "Настройки профиля")
    ]
    
    print("📱 Доступные команды:")
    for command, description in commands:
        print(f"   • {command} - {description}")
    
    print("\n🎯 Интерактивные кнопки:")
    buttons = [
        "🧘 Поза дня",
        "📚 Каталог поз", 
        "📊 Мой прогресс",
        "⚙️ Настройки",
        "🎯 Рекомендации"
    ]
    
    for button in buttons:
        print(f"   • {button}")

def main():
    """Основная функция демонстрации"""
    print("🎭 Упрощенная демонстрация Yoga Learning Bot")
    print("=" * 60)
    
    try:
        # Создаем базу данных
        conn, cursor = create_simple_database()
        
        # Добавляем данные
        add_sample_poses(cursor)
        add_sample_user(cursor)
        
        # Демонстрируем функциональность
        demo_queries(cursor)
        demo_user_features(cursor)
        demo_bot_commands()
        
        # Закрываем соединение
        conn.close()
        
        print("\n🎉 Демонстрация завершена успешно!")
        print("\n💡 Для запуска реального бота:")
        print("   1. Получите токен у @BotFather в Telegram")
        print("   2. Создайте файл .env с токеном")
        print("   3. Запустите: python run.py")
        print("\n📚 Документация:")
        print("   • README.md - полная документация")
        print("   • QUICKSTART.md - быстрый старт")
        print("   • demo.py - полная демонстрация (требует aiosqlite)")
        
    except Exception as e:
        print(f"❌ Ошибка при демонстрации: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Очистка
        import os
        if os.path.exists("simple_yoga_demo.db"):
            os.remove("simple_yoga_demo.db")
            print("\n🧹 Демонстрационная база данных очищена")

if __name__ == "__main__":
    main()
