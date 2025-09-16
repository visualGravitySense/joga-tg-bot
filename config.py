import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', 0))

# Настройки базы данных
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///yoga_bot.db')

# Kaggle API (опционально)
KAGGLE_USERNAME = os.getenv('KAGGLE_USERNAME')
KAGGLE_KEY = os.getenv('KAGGLE_KEY')

# Настройки приложения
APP_NAME = "Yoga Learning Bot"
VERSION = "1.0.0"

# Пути к файлам
DATA_DIR = "data"
IMAGES_DIR = "images"
VIDEOS_DIR = "videos"

# Создаем директории если их нет
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(VIDEOS_DIR, exist_ok=True)
