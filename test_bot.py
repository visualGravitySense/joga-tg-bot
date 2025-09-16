"""
Тесты для Yoga Learning Bot
"""

import asyncio
import pytest
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импортов
sys.path.append(str(Path(__file__).parent))

from database import Database
from yoga_data import YogaDataManager
from kaggle_integration import KaggleDataLoader

class TestDatabase:
    """Тесты для базы данных"""
    
    @pytest.fixture
    async def db(self):
        """Фикстура для создания тестовой базы данных"""
        test_db = Database("test_yoga_bot.db")
        await test_db.init_db()
        yield test_db
        # Очистка после тестов
        import os
        if os.path.exists("test_yoga_bot.db"):
            os.remove("test_yoga_bot.db")
    
    async def test_add_user(self, db):
        """Тест добавления пользователя"""
        await db.add_user(12345, "test_user", "Test", "User")
        user = await db.get_user(12345)
        assert user is not None
        assert user['user_id'] == 12345
        assert user['username'] == "test_user"
        assert user['first_name'] == "Test"
        assert user['last_name'] == "User"
    
    async def test_add_yoga_pose(self, db):
        """Тест добавления позы йоги"""
        await db.add_yoga_pose(
            name="Test Pose",
            sanskrit_name="Testasana",
            category="test",
            difficulty_level="beginner",
            description="Test description"
        )
        poses = await db.get_yoga_poses()
        assert len(poses) == 1
        assert poses[0]['name'] == "Test Pose"
        assert poses[0]['sanskrit_name'] == "Testasana"
    
    async def test_get_poses_by_category(self, db):
        """Тест получения поз по категории"""
        await db.add_yoga_pose("Pose 1", category="standing")
        await db.add_yoga_pose("Pose 2", category="seated")
        await db.add_yoga_pose("Pose 3", category="standing")
        
        standing_poses = await db.get_yoga_poses(category="standing")
        assert len(standing_poses) == 2
        
        seated_poses = await db.get_yoga_poses(category="seated")
        assert len(seated_poses) == 1
    
    async def test_get_poses_by_difficulty(self, db):
        """Тест получения поз по уровню сложности"""
        await db.add_yoga_pose("Beginner Pose", difficulty_level="beginner")
        await db.add_yoga_pose("Intermediate Pose", difficulty_level="intermediate")
        await db.add_yoga_pose("Another Beginner", difficulty_level="beginner")
        
        beginner_poses = await db.get_yoga_poses(difficulty_level="beginner")
        assert len(beginner_poses) == 2
        
        intermediate_poses = await db.get_yoga_poses(difficulty_level="intermediate")
        assert len(intermediate_poses) == 1

class TestYogaDataManager:
    """Тесты для менеджера данных йоги"""
    
    @pytest.fixture
    async def yoga_manager(self):
        """Фикстура для создания менеджера данных йоги"""
        db = Database("test_yoga_manager.db")
        await db.init_db()
        manager = YogaDataManager(db)
        yield manager
        # Очистка после тестов
        import os
        if os.path.exists("test_yoga_manager.db"):
            os.remove("test_yoga_manager.db")
    
    async def test_initialize_basic_poses(self, yoga_manager):
        """Тест инициализации базовых поз"""
        await yoga_manager.initialize_basic_poses()
        poses = await yoga_manager.db.get_yoga_poses()
        assert len(poses) >= 10  # Должно быть минимум 10 базовых поз
    
    async def test_get_categories(self, yoga_manager):
        """Тест получения категорий"""
        categories = yoga_manager.get_categories()
        assert "standing" in categories
        assert "seated" in categories
        assert "resting" in categories
        assert len(categories) >= 5
    
    async def test_get_difficulty_levels(self, yoga_manager):
        """Тест получения уровней сложности"""
        levels = yoga_manager.get_difficulty_levels()
        assert "beginner" in levels
        assert "intermediate" in levels
        assert "advanced" in levels
        assert len(levels) == 3
    
    async def test_format_pose_info(self, yoga_manager):
        """Тест форматирования информации о позе"""
        pose = {
            "name": "Test Pose",
            "sanskrit_name": "Testasana",
            "category": "standing",
            "difficulty_level": "beginner",
            "description": "Test description",
            "benefits": "Test benefits",
            "instructions": "Test instructions",
            "duration_seconds": 60
        }
        
        formatted = yoga_manager.format_pose_info(pose)
        assert "Test Pose" in formatted
        assert "Testasana" in formatted
        assert "Test description" in formatted
        assert "60 секунд" in formatted

class TestKaggleDataLoader:
    """Тесты для загрузчика данных Kaggle"""
    
    @pytest.fixture
    def kaggle_loader(self):
        """Фикстура для создания загрузчика данных"""
        return KaggleDataLoader()
    
    async def test_create_mock_data(self, kaggle_loader):
        """Тест создания моковых данных"""
        data = await kaggle_loader._create_mock_yoga_data()
        assert len(data) >= 10
        assert all('name' in pose for pose in data)
        assert all('sanskrit_name' in pose for pose in data)
        assert all('category' in pose for pose in data)
    
    async def test_get_pose_by_category(self, kaggle_loader):
        """Тест получения поз по категории"""
        data = await kaggle_loader._create_mock_yoga_data()
        standing_poses = await kaggle_loader.get_pose_by_category(data, "standing")
        assert len(standing_poses) >= 1
        assert all(pose['category'] == 'standing' for pose in standing_poses)
    
    async def test_get_pose_by_difficulty(self, kaggle_loader):
        """Тест получения поз по уровню сложности"""
        data = await kaggle_loader._create_mock_yoga_data()
        beginner_poses = await kaggle_loader.get_pose_by_difficulty(data, "beginner")
        assert len(beginner_poses) >= 1
        assert all(pose['difficulty'] == 'beginner' for pose in beginner_poses)
    
    async def test_search_poses(self, kaggle_loader):
        """Тест поиска поз"""
        data = await kaggle_loader._create_mock_yoga_data()
        results = await kaggle_loader.search_poses(data, "mountain")
        assert len(results) >= 1
        assert any("mountain" in pose['name'].lower() for pose in results)
    
    async def test_get_random_pose(self, kaggle_loader):
        """Тест получения случайной позы"""
        data = await kaggle_loader._create_mock_yoga_data()
        random_pose = await kaggle_loader.get_random_pose(data)
        assert random_pose is not None
        assert random_pose in data
        
        # Тест с фильтрацией
        beginner_pose = await kaggle_loader.get_random_pose(data, difficulty="beginner")
        if beginner_pose:
            assert beginner_pose['difficulty'] == 'beginner'
    
    async def test_get_pose_statistics(self, kaggle_loader):
        """Тест получения статистики"""
        data = await kaggle_loader._create_mock_yoga_data()
        stats = await kaggle_loader.get_pose_statistics(data)
        
        assert 'total_poses' in stats
        assert 'by_category' in stats
        assert 'by_difficulty' in stats
        assert 'average_duration' in stats
        
        assert stats['total_poses'] == len(data)
        assert stats['average_duration'] > 0

# Функции для ручного тестирования
async def test_database_operations():
    """Ручное тестирование операций с базой данных"""
    print("🧪 Тестирование базы данных...")
    
    db = Database("test_manual.db")
    await db.init_db()
    
    # Тест добавления пользователя
    await db.add_user(12345, "test_user", "Test", "User")
    user = await db.get_user(12345)
    print(f"✅ Пользователь добавлен: {user['first_name']} {user['last_name']}")
    
    # Тест добавления позы
    await db.add_yoga_pose(
        name="Test Mountain Pose",
        sanskrit_name="Test Tadasana",
        category="standing",
        difficulty_level="beginner",
        description="Test description"
    )
    poses = await db.get_yoga_poses()
    print(f"✅ Поза добавлена: {poses[0]['name']}")
    
    # Тест фильтрации
    standing_poses = await db.get_yoga_poses(category="standing")
    print(f"✅ Стоячие позы: {len(standing_poses)}")
    
    # Очистка
    import os
    if os.path.exists("test_manual.db"):
        os.remove("test_manual.db")
    
    print("✅ Все тесты базы данных прошли успешно!")

async def test_yoga_data_manager():
    """Ручное тестирование менеджера данных йоги"""
    print("🧪 Тестирование менеджера данных йоги...")
    
    db = Database("test_yoga_manager_manual.db")
    await db.init_db()
    manager = YogaDataManager(db)
    
    # Инициализация базовых поз
    await manager.initialize_basic_poses()
    poses = await manager.db.get_yoga_poses()
    print(f"✅ Инициализировано {len(poses)} базовых поз")
    
    # Тест категорий
    categories = manager.get_categories()
    print(f"✅ Доступно категорий: {len(categories)}")
    
    # Тест форматирования
    if poses:
        formatted = manager.format_pose_info(poses[0])
        print(f"✅ Форматирование работает: {len(formatted)} символов")
    
    # Очистка
    import os
    if os.path.exists("test_yoga_manager_manual.db"):
        os.remove("test_yoga_manager_manual.db")
    
    print("✅ Все тесты менеджера данных прошли успешно!")

async def test_kaggle_loader():
    """Ручное тестирование загрузчика Kaggle"""
    print("🧪 Тестирование загрузчика Kaggle...")
    
    loader = KaggleDataLoader()
    
    # Создание моковых данных
    data = await loader._create_mock_yoga_data()
    print(f"✅ Создано {len(data)} моковых поз")
    
    # Тест статистики
    stats = await loader.get_pose_statistics(data)
    print(f"✅ Статистика: {stats['total_poses']} поз, средняя продолжительность {stats['average_duration']:.1f} сек")
    
    # Тест поиска
    results = await loader.search_poses(data, "mountain")
    print(f"✅ Поиск 'mountain': найдено {len(results)} результатов")
    
    # Тест случайной позы
    random_pose = await loader.get_random_pose(data, difficulty="beginner")
    if random_pose:
        print(f"✅ Случайная поза для начинающих: {random_pose['name']}")
    
    print("✅ Все тесты загрузчика Kaggle прошли успешно!")

async def run_all_tests():
    """Запуск всех ручных тестов"""
    print("🚀 Запуск всех тестов...\n")
    
    try:
        await test_database_operations()
        print()
        await test_yoga_data_manager()
        print()
        await test_kaggle_loader()
        print()
        print("🎉 Все тесты прошли успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Запуск ручных тестов
    asyncio.run(run_all_tests())
