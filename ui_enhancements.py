"""
Дополнительные улучшения интерфейса для Yoga Learning Bot
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict, Optional

def get_pose_list_keyboard(poses: List[Dict], page: int = 0, per_page: int = 5):
    """Клавиатура для списка поз с пагинацией"""
    keyboard = InlineKeyboardBuilder()
    
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_poses = poses[start_idx:end_idx]
    
    # Добавляем кнопки для поз
    for pose in page_poses:
        keyboard.row(
            InlineKeyboardButton(
                text=f"🧘‍♀️ {pose['name'][:20]}{'...' if len(pose['name']) > 20 else ''}",
                callback_data=f"pose_{pose['id']}"
            )
        )
    
    # Кнопки навигации
    nav_buttons = []
    if page > 0:
        nav_buttons.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page-1}")
        )
    
    if end_idx < len(poses):
        nav_buttons.append(
            InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page+1}")
        )
    
    if nav_buttons:
        keyboard.row(*nav_buttons)
    
    # Кнопка возврата
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    
    return keyboard.as_markup()

def get_quick_actions_keyboard():
    """Клавиатура быстрых действий"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎲 Случайная поза", callback_data="random_pose"),
                InlineKeyboardButton(text="🌟 Поза дня", callback_data="daily_pose")
            ],
            [
                InlineKeyboardButton(text="📊 Прогресс", callback_data="progress"),
                InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
            ],
            [
                InlineKeyboardButton(text="🔍 Поиск", callback_data="search_poses"),
                InlineKeyboardButton(text="📚 Каталог", callback_data="catalog")
            ]
        ]
    )
    return keyboard

def get_favorites_keyboard(favorite_poses: List[Dict]):
    """Клавиатура избранных поз"""
    keyboard = InlineKeyboardBuilder()
    
    if not favorite_poses:
        keyboard.row(
            InlineKeyboardButton(
                text="📚 Перейти к каталогу",
                callback_data="catalog"
            )
        )
    else:
        for pose in favorite_poses:
            keyboard.row(
                InlineKeyboardButton(
                    text=f"❤️ {pose['name']}",
                    callback_data=f"pose_{pose['id']}"
                )
            )
    
    keyboard.row(InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main"))
    return keyboard.as_markup()

def get_workout_plans_keyboard():
    """Клавиатура планов тренировок"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🌅 Утренняя практика", callback_data="workout_morning"),
                InlineKeyboardButton(text="🌙 Вечерняя практика", callback_data="workout_evening")
            ],
            [
                InlineKeyboardButton(text="💪 Силовая тренировка", callback_data="workout_strength"),
                InlineKeyboardButton(text="😌 Расслабление", callback_data="workout_relaxation")
            ],
            [
                InlineKeyboardButton(text="🔄 Гибкость", callback_data="workout_flexibility"),
                InlineKeyboardButton(text="⚖️ Равновесие", callback_data="workout_balance")
            ],
            [
                InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_achievements_keyboard():
    """Клавиатура достижений"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏆 Все достижения", callback_data="achievements_all"),
                InlineKeyboardButton(text="🎯 Текущие цели", callback_data="achievements_current")
            ],
            [
                InlineKeyboardButton(text="📈 Статистика", callback_data="achievements_stats"),
                InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_pose_detail_keyboard(pose_id: int, is_favorite: bool = False):
    """Детальная клавиатура для позы"""
    keyboard = InlineKeyboardBuilder()
    
    # Основные действия
    keyboard.row(
        InlineKeyboardButton(text="⭐ Оценить", callback_data=f"rate_{pose_id}"),
        InlineKeyboardButton(text="⏱️ Таймер", callback_data=f"timer_{pose_id}")
    )
    
    # Дополнительные действия
    keyboard.row(
        InlineKeyboardButton(text="📝 Заметки", callback_data=f"notes_{pose_id}"),
        InlineKeyboardButton(
            text="❤️ Удалить из избранного" if is_favorite else "🤍 В избранное",
            callback_data=f"favorite_{pose_id}"
        )
    )
    
    # Навигация
    keyboard.row(
        InlineKeyboardButton(text="🔄 Другая поза", callback_data="random_pose"),
        InlineKeyboardButton(text="📚 Каталог", callback_data="catalog")
    )
    
    keyboard.row(InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main"))
    
    return keyboard.as_markup()

def get_settings_keyboard():
    """Расширенная клавиатура настроек"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Уровень сложности", callback_data="settings_difficulty"),
                InlineKeyboardButton(text="🔔 Уведомления", callback_data="settings_notifications")
            ],
            [
                InlineKeyboardButton(text="🌍 Язык", callback_data="settings_language"),
                InlineKeyboardButton(text="📊 Статистика", callback_data="settings_stats")
            ],
            [
                InlineKeyboardButton(text="🗑️ Очистить данные", callback_data="settings_clear"),
                InlineKeyboardButton(text="ℹ️ О боте", callback_data="settings_about")
            ],
            [
                InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_confirmation_keyboard(action: str, item_id: str = ""):
    """Клавиатура подтверждения действий"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data=f"confirm_{action}_{item_id}"),
                InlineKeyboardButton(text="❌ Нет", callback_data=f"cancel_{action}_{item_id}")
            ]
        ]
    )
    return keyboard

def format_progress_message(user_stats: Dict) -> str:
    """Форматирование сообщения о прогрессе"""
    total_sessions = user_stats.get('total_sessions', 0)
    total_duration = user_stats.get('total_duration', 0)
    current_streak = user_stats.get('current_streak', 0)
    longest_streak = user_stats.get('longest_streak', 0)
    
    # Конвертируем секунды в часы и минуты
    hours = total_duration // 3600
    minutes = (total_duration % 3600) // 60
    
    progress_text = f"""
📊 *Ваш прогресс в йоге*

🎯 **Сессии:**
• Всего практик: {total_sessions}
• Общее время: {hours}ч {minutes}м

🔥 **Серии:**
• Текущая серия: {current_streak} дней
• Лучшая серия: {longest_streak} дней

🏆 **Достижения:**
• {'🥇 Мастер йоги' if total_sessions >= 100 else '🥈 Продвинутый' if total_sessions >= 50 else '🥉 Начинающий'}
• {'🔥 Огненная серия' if current_streak >= 30 else '💪 Стабильная практика' if current_streak >= 7 else '🌱 Начало пути'}
"""
    
    return progress_text

def get_motivational_message() -> str:
    """Получение мотивационного сообщения"""
    messages = [
        "💪 Каждый день - это возможность стать лучше!",
        "🧘‍♀️ Йога - это путешествие к самому себе.",
        "🌟 Маленькие шаги ведут к большим изменениям.",
        "🌱 Рост происходит за пределами зоны комфорта.",
        "💫 Сегодняшняя практика - завтрашняя сила.",
        "🌈 В каждом вдохе есть возможность для мира.",
        "🦋 Превратите свои мечты в реальность через практику."
    ]
    
    import random
    return random.choice(messages)
