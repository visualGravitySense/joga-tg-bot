# 🚀 Развертывание Yoga Learning Bot

## 📋 Обзор проекта

Мы создали полнофункциональный Telegram бот для изучения йоги со следующими возможностями:

### ✨ Основные функции
- 🧘 **Поза дня** - ежедневные рекомендации
- 📚 **Каталог поз** - поиск по категориям и сложности
- 📊 **Отслеживание прогресса** - статистика занятий
- ⚙️ **Настройки профиля** - выбор уровня сложности
- 🎯 **Персональные рекомендации** - на основе предпочтений
- ⭐ **Система оценок** - для улучшения рекомендаций

### 🏗️ Архитектура
- **Backend**: Python 3.8+ с aiogram 3.2.0
- **База данных**: SQLite с aiosqlite
- **Данные**: 10+ базовых поз йоги с описаниями
- **Интеграция**: Готовность к подключению Kaggle API

## 📁 Структура проекта

```
yoga-bot/
├── bot.py                 # Основной файл бота
├── config.py              # Конфигурация приложения
├── database.py            # Работа с базой данных
├── yoga_data.py           # Управление данными о йоге
├── kaggle_integration.py  # Интеграция с Kaggle
├── test_bot.py            # Тесты приложения
├── demo.py                # Полная демонстрация
├── simple_demo.py         # Упрощенная демонстрация
├── deploy.py              # Скрипт развертывания
├── run.py                 # Запуск бота
├── requirements.txt       # Зависимости Python
├── README.md             # Полная документация
├── QUICKSTART.md         # Быстрый старт
├── DEPLOYMENT.md         # Этот файл
└── .gitignore            # Игнорируемые файлы
```

## 🚀 Варианты развертывания

### 1. Локальное развертывание

#### Быстрый старт (3 минуты)
```bash
# 1. Создайте бота в Telegram через @BotFather
# 2. Создайте файл .env с токеном
echo "BOT_TOKEN=ваш_токен_здесь" > .env

# 3. Запустите развертывание
python deploy.py
```

#### Ручная установка
```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла
cp .env.example .env
# Отредактируйте .env файл с вашим токеном

# Инициализация базы данных
python -c "
import asyncio
from database import Database
from yoga_data import YogaDataManager

async def init():
    db = Database()
    await db.init_db()
    manager = YogaDataManager(db)
    await manager.initialize_basic_poses()
    print('База данных инициализирована')

asyncio.run(init())
"

# Запуск бота
python run.py
```

### 2. Развертывание на VPS

#### Подготовка сервера
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python и pip
sudo apt install python3 python3-pip python3-venv -y

# Создание пользователя для бота
sudo useradd -m -s /bin/bash yogabot
sudo su - yogabot
```

#### Установка приложения
```bash
# Клонирование проекта
git clone <your-repo-url> yoga-bot
cd yoga-bot

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка конфигурации
cp .env.example .env
nano .env  # Добавьте ваш токен
```

#### Настройка systemd сервиса
```bash
# Создание сервиса
sudo nano /etc/systemd/system/yoga-bot.service
```

Содержимое файла сервиса:
```ini
[Unit]
Description=Yoga Learning Bot
After=network.target

[Service]
Type=simple
User=yogabot
WorkingDirectory=/home/yogabot/yoga-bot
Environment=PATH=/home/yogabot/yoga-bot/venv/bin
ExecStart=/home/yogabot/yoga-bot/venv/bin/python run.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Запуск сервиса
sudo systemctl daemon-reload
sudo systemctl enable yoga-bot
sudo systemctl start yoga-bot
sudo systemctl status yoga-bot
```

### 3. Развертывание в Docker

#### Создание Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  yoga-bot:
    build: .
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_USER_ID=${ADMIN_USER_ID}
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

#### Запуск
```bash
# Создание .env файла
echo "BOT_TOKEN=ваш_токен" > .env

# Запуск контейнера
docker-compose up -d
```

### 4. Развертывание на Heroku

#### Подготовка
```bash
# Установка Heroku CLI
# Создание Procfile
echo "worker: python run.py" > Procfile

# Создание runtime.txt
echo "python-3.10.0" > runtime.txt
```

#### Развертывание
```bash
# Логин в Heroku
heroku login

# Создание приложения
heroku create your-yoga-bot

# Установка переменных окружения
heroku config:set BOT_TOKEN=ваш_токен
heroku config:set ADMIN_USER_ID=ваш_id

# Развертывание
git push heroku main

# Запуск worker
heroku ps:scale worker=1
```

## 🔧 Настройка и конфигурация

### Переменные окружения
```env
# Обязательные
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_USER_ID=123456789

# Опциональные
DATABASE_URL=sqlite:///yoga_bot.db
KAGGLE_USERNAME=your_username
KAGGLE_KEY=your_key
```

### Настройка логирования
```python
# В config.py
LOG_LEVEL=INFO
LOG_FILE=yoga_bot.log
```

### Настройка базы данных
```python
# Для PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/yoga_bot

# Для MySQL
DATABASE_URL=mysql://user:password@localhost/yoga_bot
```

## 📊 Мониторинг и обслуживание

### Логи
```bash
# Просмотр логов
tail -f yoga_bot.log

# Логи systemd
sudo journalctl -u yoga-bot -f
```

### Резервное копирование
```bash
# Бэкап базы данных
cp yoga_bot.db backup_$(date +%Y%m%d).db

# Автоматический бэкап
echo "0 2 * * * cp /path/to/yoga_bot.db /backup/yoga_bot_$(date +\%Y\%m\%d).db" | crontab -
```

### Обновление
```bash
# Остановка бота
sudo systemctl stop yoga-bot

# Обновление кода
git pull origin main

# Установка новых зависимостей
pip install -r requirements.txt

# Запуск бота
sudo systemctl start yoga-bot
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Полные тесты
python test_bot.py

# Упрощенная демонстрация
python simple_demo.py

# Проверка конфигурации
python deploy.py --check
```

### Тестирование в продакшене
```bash
# Проверка статуса
sudo systemctl status yoga-bot

# Проверка логов
sudo journalctl -u yoga-bot --since "1 hour ago"

# Тест подключения к Telegram
python -c "
import asyncio
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
async def test():
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    me = await bot.get_me()
    print(f'Бот: @{me.username}')
    await bot.session.close()

asyncio.run(test())
"
```

## 🚨 Устранение неполадок

### Частые проблемы

#### Бот не отвечает
```bash
# Проверка токена
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Токен:', os.getenv('BOT_TOKEN')[:10] + '...')"

# Проверка подключения
ping api.telegram.org
```

#### Ошибки базы данных
```bash
# Проверка файла базы данных
ls -la yoga_bot.db

# Пересоздание базы данных
rm yoga_bot.db
python -c "
import asyncio
from database import Database
from yoga_data import YogaDataManager

async def recreate():
    db = Database()
    await db.init_db()
    manager = YogaDataManager(db)
    await manager.initialize_basic_poses()
    print('База данных пересоздана')

asyncio.run(recreate())
"
```

#### Проблемы с зависимостями
```bash
# Переустановка зависимостей
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Проверка версий
pip list | grep -E "(aiogram|aiosqlite|pandas)"
```

## 📈 Масштабирование

### Горизонтальное масштабирование
- Использование Redis для состояния
- Балансировка нагрузки между экземплярами
- Микросервисная архитектура

### Вертикальное масштабирование
- Увеличение ресурсов сервера
- Оптимизация запросов к базе данных
- Кэширование часто используемых данных

## 🔐 Безопасность

### Рекомендации
- Использование HTTPS для webhook
- Регулярное обновление зависимостей
- Мониторинг логов на подозрительную активность
- Ограничение доступа к админским функциям

### Настройка webhook (опционально)
```python
# В bot.py
await bot.set_webhook(
    url="https://yourdomain.com/webhook",
    secret_token="your_secret_token"
)
```

## 📞 Поддержка

### Полезные ресурсы
- [Документация aiogram](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Kaggle API](https://www.kaggle.com/docs/api)

### Контакты
- GitHub Issues для багов
- Telegram для вопросов
- Email для коммерческих запросов

---

**Удачного развертывания! 🚀**
