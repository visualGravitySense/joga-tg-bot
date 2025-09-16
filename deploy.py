"""
Скрипт для развертывания Yoga Learning Bot
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('yoga_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def check_requirements():
    """Проверка требований для запуска"""
    logger.info("🔍 Проверка требований...")
    
    # Проверка Python версии
    if sys.version_info < (3, 8):
        logger.error("❌ Требуется Python 3.8 или выше")
        return False
    
    logger.info(f"✅ Python версия: {sys.version}")
    
    # Проверка файла requirements.txt
    if not Path("requirements.txt").exists():
        logger.error("❌ Файл requirements.txt не найден")
        return False
    
    logger.info("✅ Файл requirements.txt найден")
    
    # Проверка переменных окружения
    if not os.getenv('BOT_TOKEN'):
        logger.warning("⚠️ Переменная BOT_TOKEN не установлена")
        logger.info("💡 Создайте файл .env с вашим токеном бота")
        return False
    
    logger.info("✅ Переменная BOT_TOKEN установлена")
    
    return True

def create_directories():
    """Создание необходимых директорий"""
    logger.info("📁 Создание директорий...")
    
    directories = ['data', 'images', 'videos', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"✅ Директория {directory} создана")
    
    return True

def install_dependencies():
    """Установка зависимостей"""
    logger.info("📦 Установка зависимостей...")
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("✅ Зависимости установлены успешно")
            return True
        else:
            logger.error(f"❌ Ошибка при установке зависимостей: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Ошибка при установке зависимостей: {e}")
        return False

async def initialize_database():
    """Инициализация базы данных"""
    logger.info("🗄️ Инициализация базы данных...")
    
    try:
        from database import Database
        from yoga_data import YogaDataManager
        
        db = Database()
        await db.init_db()
        
        yoga_manager = YogaDataManager(db)
        await yoga_manager.initialize_basic_poses()
        
        logger.info("✅ База данных инициализирована")
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при инициализации базы данных: {e}")
        return False

def create_env_file():
    """Создание файла .env если его нет"""
    env_file = Path('.env')
    
    if not env_file.exists():
        logger.info("📝 Создание файла .env...")
        
        env_content = """# Telegram Bot Token (получите у @BotFather)
BOT_TOKEN=your_bot_token_here

# Database settings
DATABASE_URL=sqlite:///yoga_bot.db

# Kaggle API (опционально, для загрузки данных)
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key

# Admin settings
ADMIN_USER_ID=your_telegram_user_id
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        logger.info("✅ Файл .env создан")
        logger.info("⚠️ Не забудьте заполнить BOT_TOKEN в файле .env")
        return False
    else:
        logger.info("✅ Файл .env уже существует")
        return True

def check_bot_token():
    """Проверка токена бота"""
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv('BOT_TOKEN')
    
    if not token or token == 'your_bot_token_here':
        logger.error("❌ Токен бота не установлен")
        logger.info("💡 Получите токен у @BotFather в Telegram и добавьте в .env")
        return False
    
    # Простая проверка формата токена
    if not token.count(':') == 1 or len(token.split(':')) != 2:
        logger.error("❌ Неверный формат токена бота")
        return False
    
    logger.info("✅ Токен бота валиден")
    return True

async def test_bot_connection():
    """Тест подключения к Telegram API"""
    logger.info("🔗 Тестирование подключения к Telegram API...")
    
    try:
        from aiogram import Bot
        from dotenv import load_dotenv
        
        load_dotenv()
        token = os.getenv('BOT_TOKEN')
        
        bot = Bot(token=token)
        me = await bot.get_me()
        
        logger.info(f"✅ Бот подключен: @{me.username} ({me.first_name})")
        await bot.session.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка подключения к Telegram API: {e}")
        return False

def show_deployment_info():
    """Показать информацию о развертывании"""
    logger.info("""
🎉 Yoga Learning Bot готов к запуску!

📋 Информация о развертывании:
• База данных: SQLite (yoga_bot.db)
• Логи: yoga_bot.log
• Конфигурация: .env файл

🚀 Команды для запуска:
• python run.py - запуск бота
• python test_bot.py - тестирование
• python deploy.py --check - проверка конфигурации

📱 Для использования:
1. Найдите вашего бота в Telegram
2. Отправьте /start
3. Изучайте йогу!

🔧 Для разработки:
• Добавьте новые позы в yoga_data.py
• Расширьте функциональность в bot.py
• Используйте Kaggle данные через kaggle_integration.py

📚 Документация: README.md
""")

async def main():
    """Основная функция развертывания"""
    logger.info("🚀 Начинаем развертывание Yoga Learning Bot...")
    
    # Создание директорий
    if not create_directories():
        return False
    
    # Создание .env файла если нужно
    env_ready = create_env_file()
    
    # Проверка требований
    if not check_requirements():
        if not env_ready:
            logger.info("💡 Заполните .env файл и запустите развертывание снова")
        return False
    
    # Проверка токена бота
    if not check_bot_token():
        return False
    
    # Установка зависимостей
    if not install_dependencies():
        return False
    
    # Инициализация базы данных
    if not await initialize_database():
        return False
    
    # Тест подключения к Telegram
    if not await test_bot_connection():
        return False
    
    # Показать информацию о развертывании
    show_deployment_info()
    
    logger.info("✅ Развертывание завершено успешно!")
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Развертывание Yoga Learning Bot')
    parser.add_argument('--check', action='store_true', help='Только проверка конфигурации')
    
    args = parser.parse_args()
    
    if args.check:
        # Только проверка
        logger.info("🔍 Проверка конфигурации...")
        success = check_requirements() and check_bot_token()
        if success:
            logger.info("✅ Конфигурация корректна")
        else:
            logger.info("❌ Конфигурация требует исправления")
        sys.exit(0 if success else 1)
    else:
        # Полное развертывание
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
