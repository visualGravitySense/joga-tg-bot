"""
Демонстрация функциональности Yoga Learning Bot
"""

import asyncio
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импортов
sys.path.append(str(Path(__file__).parent))

from database import Database
from yoga_data import YogaDataManager
from kaggle_integration import KaggleDataLoader

async def demo_database():
    """Демонстрация работы с базой данных"""
    print("🗄️ Демонстрация базы данных")
    print("=" * 50)
    
    # Создаем тестовую базу данных
    db = Database("demo_yoga_bot.db")
    await db.init_db()
    
    # Добавляем пользователя
    await db.add_user(12345, "demo_user", "Demo", "User")
    user = await db.get_user(12345)
    print(f"✅ Пользователь добавлен: {user['first_name']} {user['last_name']}")
    
    # Добавляем позу
    await db.add_yoga_pose(
        name="Demo Mountain Pose",
        sanskrit_name="Demo Tadasana",
        category="standing",
        difficulty_level="beginner",
        description="Демонстрационная поза горы",
        benefits="Улучшает осанку и равновесие",
        instructions="Встаньте прямо, ноги вместе, руки по бокам"
    )
    
    # Получаем все позы
    poses = await db.get_yoga_poses()
    print(f"✅ Поз в базе данных: {len(poses)}")
    
    # Фильтруем по категории
    standing_poses = await db.get_yoga_poses(category="standing")
    print(f"✅ Стоячих поз: {len(standing_poses)}")
    
    # Фильтруем по сложности
    beginner_poses = await db.get_yoga_poses(difficulty_level="beginner")
    print(f"✅ Поз для начинающих: {len(beginner_poses)}")
    
    print()

async def demo_yoga_manager():
    """Демонстрация менеджера данных йоги"""
    print("🧘 Демонстрация менеджера данных йоги")
    print("=" * 50)
    
    # Создаем менеджер
    db = Database("demo_yoga_manager.db")
    await db.init_db()
    manager = YogaDataManager(db)
    
    # Инициализируем базовые позы
    await manager.initialize_basic_poses()
    poses = await manager.db.get_yoga_poses()
    print(f"✅ Инициализировано базовых поз: {len(poses)}")
    
    # Показываем категории
    categories = manager.get_categories()
    print(f"✅ Доступные категории: {', '.join(categories[:5])}...")
    
    # Показываем уровни сложности
    difficulties = manager.get_difficulty_levels()
    print(f"✅ Уровни сложности: {', '.join(difficulties)}")
    
    # Получаем случайную позу
    random_pose = await manager.get_random_pose()
    if random_pose:
        print(f"✅ Случайная поза: {random_pose['name']}")
        
        # Форматируем информацию о позе
        formatted_info = manager.format_pose_info(random_pose)
        print(f"📝 Форматированная информация ({len(formatted_info)} символов):")
        print(formatted_info[:200] + "..." if len(formatted_info) > 200 else formatted_info)
    
    print()

async def demo_kaggle_loader():
    """Демонстрация загрузчика Kaggle данных"""
    print("📊 Демонстрация загрузчика Kaggle данных")
    print("=" * 50)
    
    # Создаем загрузчик
    loader = KaggleDataLoader()
    
    # Создаем моковые данные
    data = await loader._create_mock_yoga_data()
    print(f"✅ Создано моковых данных: {len(data)} поз")
    
    # Получаем статистику
    stats = await loader.get_pose_statistics(data)
    print(f"📈 Статистика:")
    print(f"   • Всего поз: {stats['total_poses']}")
    print(f"   • Средняя продолжительность: {stats['average_duration']:.1f} сек")
    print(f"   • По категориям: {stats['by_category']}")
    print(f"   • По сложности: {stats['by_difficulty']}")
    
    # Поиск поз
    search_results = await loader.search_poses(data, "mountain")
    print(f"🔍 Поиск 'mountain': найдено {len(search_results)} результатов")
    
    # Получение поз по категории
    standing_poses = await loader.get_pose_by_category(data, "standing")
    print(f"🏃 Стоячих поз: {len(standing_poses)}")
    
    # Получение поз по сложности
    beginner_poses = await loader.get_pose_by_difficulty(data, "beginner")
    print(f"🟢 Поз для начинающих: {len(beginner_poses)}")
    
    # Случайная поза с фильтрацией
    random_beginner = await loader.get_random_pose(data, difficulty="beginner")
    if random_beginner:
        print(f"🎲 Случайная поза для начинающих: {random_beginner['name']}")
    
    print()

async def demo_bot_features():
    """Демонстрация функций бота"""
    print("🤖 Демонстрация функций бота")
    print("=" * 50)
    
    # Создаем менеджер для демонстрации
    db = Database("demo_bot_features.db")
    await db.init_db()
    manager = YogaDataManager(db)
    await manager.initialize_basic_poses()
    
    # Симулируем пользователя
    user_id = 12345
    await db.add_user(user_id, "demo_user", "Demo", "User", level="beginner")
    
    # Получаем позу дня для пользователя
    daily_pose = await manager.get_daily_pose(user_id)
    if daily_pose:
        print(f"🌟 Поза дня для пользователя: {daily_pose['name']}")
    
    # Получаем рекомендации
    user = await db.get_user(user_id)
    if user:
        level = user.get('level', 'beginner')
        recommendations = await manager.get_poses_by_difficulty(level)
        print(f"🎯 Рекомендации для уровня '{level}': {len(recommendations)} поз")
        
        if recommendations:
            print("   Топ-3 рекомендации:")
            for i, pose in enumerate(recommendations[:3], 1):
                print(f"   {i}. {pose['name']} ({pose['category']})")
    
    # Симулируем сессию пользователя
    if daily_pose:
        await db.add_user_session(
            user_id=user_id,
            pose_id=daily_pose['id'],
            duration_seconds=60,
            rating=5,
            notes="Отличная поза для начинающих!"
        )
        print(f"✅ Сессия записана: {daily_pose['name']} (5/5 ⭐)")
    
    # Обновляем прогресс
    await db.update_user_progress(
        user_id=user_id,
        total_sessions=1,
        total_duration=60,
        current_streak=1,
        longest_streak=1
    )
    
    # Показываем прогресс
    progress = await db.get_user_progress(user_id)
    if progress:
        print(f"📊 Прогресс пользователя:")
        print(f"   • Сессий: {progress['total_sessions']}")
        print(f"   • Время: {progress['total_duration']} сек")
        print(f"   • Серия: {progress['current_streak']} дней")
    
    print()

async def main():
    """Основная функция демонстрации"""
    print("🎭 Демонстрация Yoga Learning Bot")
    print("=" * 60)
    print()
    
    try:
        await demo_database()
        await demo_yoga_manager()
        await demo_kaggle_loader()
        await demo_bot_features()
        
        print("🎉 Демонстрация завершена успешно!")
        print()
        print("💡 Для запуска реального бота:")
        print("   1. Получите токен у @BotFather")
        print("   2. Создайте файл .env с токеном")
        print("   3. Запустите: python run.py")
        print()
        print("📚 Документация: README.md")
        print("🚀 Быстрый старт: QUICKSTART.md")
        
    except Exception as e:
        print(f"❌ Ошибка при демонстрации: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Очистка демонстрационных файлов
        import os
        demo_files = [
            "demo_yoga_bot.db",
            "demo_yoga_manager.db", 
            "demo_bot_features.db"
        ]
        
        for file in demo_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🧹 Очищен файл: {file}")

if __name__ == "__main__":
    asyncio.run(main())
