#!/usr/bin/env python3
"""
Демонстрация функции /progress в реальном боте
"""

import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

async def demo_progress_in_bot():
    """Демонстрация функции прогресса в боте"""
    print("🧘 Демонстрация функции /progress в боте")
    print("=" * 50)
    
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token=token)
    
    try:
        me = await bot.get_me()
        print(f"✅ Бот @{me.username} готов к демонстрации!")
        print(f"📱 Имя: {me.first_name}")
        print(f"🆔 ID: {me.id}")
        
        print("\n🎯 Функция /progress включает:")
        print("1. 📊 Статистику занятий:")
        print("   • Общее количество сессий")
        print("   • Общее время практики")
        print("   • Текущая серия дней")
        print("   • Лучшая серия дней")
        
        print("\n2. 🏆 Систему достижений:")
        print("   • Первые шаги (1 сессия)")
        print("   • Новичок (10 сессий)")
        print("   • Практикующий (50 сессий)")
        print("   • Мастер йоги (100 сессий)")
        print("   • Постоянство (7 дней подряд)")
        print("   • Железная воля (30 дней подряд)")
        print("   • Час практики (1+ час)")
        print("   • Мастер времени (10+ часов)")
        
        print("\n3. 💫 Мотивационные сообщения:")
        print("   • Случайные вдохновляющие фразы")
        print("   • Поддержка на пути к целям")
        
        print("\n4. 📈 Дополнительные функции:")
        print("   • Избранные позы")
        print("   • Заметки к позам")
        print("   • Планы тренировок")
        print("   • Поиск поз")
        
        print("\n🚀 Как протестировать:")
        print("1. Откройте Telegram")
        print("2. Найдите бота: @aawraBot")
        print("3. Отправьте /start")
        print("4. Отправьте /progress")
        print("5. Или нажмите кнопку '📊 Мой прогресс'")
        
        print("\n💡 Для получения данных:")
        print("1. Попробуйте несколько поз из каталога")
        print("2. Оцените позы (⭐)")
        print("3. Добавьте позы в избранное (❤️)")
        print("4. Создайте заметки к позам (📝)")
        print("5. Проверьте прогресс снова")
        
        print("\n🎉 Функция /progress полностью готова к использованию!")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(demo_progress_in_bot())
