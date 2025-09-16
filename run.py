#!/usr/bin/env python3
"""
Скрипт для запуска Yoga Learning Bot
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем текущую директорию в путь для импортов
sys.path.append(str(Path(__file__).parent))

from bot import main

if __name__ == "__main__":
    try:
        print("🧘 Запуск Yoga Learning Bot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске бота: {e}")
        sys.exit(1)
