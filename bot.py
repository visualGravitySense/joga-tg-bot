"""
Основной файл Telegram бота для изучения йоги
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import BOT_TOKEN, ADMIN_USER_ID
from database import Database
from yoga_data import YogaDataManager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Инициализация базы данных
db = Database()
yoga_manager = YogaDataManager(db)

# Состояния для FSM
class UserStates(StatesGroup):
    waiting_for_level = State()
    waiting_for_rating = State()
    waiting_for_notes = State()

# Клавиатуры
def get_main_keyboard():
    """Главная клавиатура"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧘 Поза дня"), KeyboardButton(text="📚 Каталог поз")],
            [KeyboardButton(text="📊 Мой прогресс"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="ℹ️ Помощь"), KeyboardButton(text="🎯 Рекомендации")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard

def get_categories_keyboard():
    """Клавиатура категорий поз"""
    categories = yoga_manager.get_categories()
    keyboard = InlineKeyboardBuilder()
    
    # Добавляем кнопки по 2 в ряд
    for i in range(0, len(categories), 2):
        row = []
        for j in range(2):
            if i + j < len(categories):
                category = categories[i + j]
                category_names = {
                    "standing": "Стоячие",
                    "seated": "Сидячие", 
                    "on_knees": "На коленях",
                    "lying": "Лежачие",
                    "inversion": "Перевернутые",
                    "backbend": "Прогибы",
                    "forward_bend": "Наклоны вперед",
                    "twist": "Скручивания",
                    "resting": "Расслабляющие",
                    "balance": "Равновесие"
                }
                row.append(InlineKeyboardButton(
                    text=category_names.get(category, category),
                    callback_data=f"category_{category}"
                ))
        keyboard.row(*row)
    
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main"))
    return keyboard.as_markup()

def get_difficulty_keyboard():
    """Клавиатура уровней сложности"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 Начинающий", callback_data="difficulty_beginner"),
                InlineKeyboardButton(text="🟡 Средний", callback_data="difficulty_intermediate")
            ],
            [
                InlineKeyboardButton(text="🔴 Продвинутый", callback_data="difficulty_advanced"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

def get_pose_keyboard(pose_id: int):
    """Клавиатура для работы с позой"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ Оценить", callback_data=f"rate_{pose_id}"),
                InlineKeyboardButton(text="📝 Заметки", callback_data=f"notes_{pose_id}")
            ],
            [
                InlineKeyboardButton(text="🔄 Другая поза", callback_data="random_pose"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")
            ]
        ]
    )
    return keyboard

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user = message.from_user
    
    # Добавляем пользователя в базу данных
    await db.add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    welcome_text = f"""
🧘‍♀️ *Добро пожаловать в Yoga Learning Bot!*

Привет, {user.first_name}! 

Этот бот поможет вам изучить йогу с помощью:
• 📚 Каталога поз с подробными описаниями
• 🎯 Персональных рекомендаций
• 📊 Отслеживания прогресса
• 🧘 Позы дня для ежедневной практики

Выберите действие в меню ниже или используйте команды:
/help - помощь
/settings - настройки
/progress - ваш прогресс
"""
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
📖 *Справка по командам:*

/start - начать работу с ботом
/help - показать эту справку
/settings - настройки профиля
/progress - ваш прогресс
/pose - случайная поза
/daily - поза дня

🎯 *Основные функции:*
• 🧘 Поза дня - ежедневная рекомендация
• 📚 Каталог поз - поиск по категориям и сложности
• 📊 Мой прогресс - статистика занятий
• ⚙️ Настройки - уровень сложности и предпочтения
• 🎯 Рекомендации - персональные советы

💡 *Советы:*
• Начните с поз для начинающих
• Регулярно практикуйтесь для лучших результатов
• Оценивайте позы для улучшения рекомендаций
"""
    
    await message.answer(help_text, parse_mode="Markdown")

@dp.message(Command("settings"))
async def cmd_settings(message: types.Message):
    """Обработчик команды /settings"""
    user = await db.get_user(message.from_user.id)
    if user:
        level_text = {
            "beginner": "🟢 Начинающий",
            "intermediate": "🟡 Средний",
            "advanced": "🔴 Продвинутый"
        }.get(user.get('level', 'beginner'), '🟢 Начинающий')
        
        settings_text = f"""
⚙️ *Настройки профиля*

👤 Имя: {user.get('first_name', 'Не указано')}
📊 Уровень: {level_text}
📅 Регистрация: {user.get('created_at', 'Неизвестно')}

Выберите новый уровень сложности:
"""
        
        await message.answer(
            settings_text,
            reply_markup=get_difficulty_keyboard(),
            parse_mode="Markdown"
        )

@dp.message(Command("progress"))
async def cmd_progress(message: types.Message):
    """Обработчик команды /progress"""
    user_id = message.from_user.id
    progress = await db.get_user_progress(user_id)
    
    if progress:
        progress_text = f"""
📊 *Ваш прогресс*

🎯 Всего сессий: {progress.get('total_sessions', 0)}
⏱️ Общее время: {progress.get('total_duration', 0) // 60} минут
🔥 Текущая серия: {progress.get('current_streak', 0)} дней
🏆 Лучшая серия: {progress.get('longest_streak', 0)} дней
📅 Последняя сессия: {progress.get('last_session_date', 'Никогда')}
"""
    else:
        progress_text = """
📊 *Ваш прогресс*

Пока у вас нет записанных сессий.
Начните практику, чтобы отслеживать свой прогресс!
"""
    
    await message.answer(progress_text, parse_mode="Markdown")

@dp.message(Command("pose"))
async def cmd_random_pose(message: types.Message):
    """Обработчик команды /pose - случайная поза"""
    user = await db.get_user(message.from_user.id)
    difficulty = user.get('level', 'beginner') if user else 'beginner'
    
    pose = await yoga_manager.get_random_pose(difficulty=difficulty)
    if pose:
        await show_pose_info(message, pose)
    else:
        await message.answer("❌ Не удалось найти подходящую позу. Попробуйте позже.")

@dp.message(Command("daily"))
async def cmd_daily_pose(message: types.Message):
    """Обработчик команды /daily - поза дня"""
    pose = await yoga_manager.get_daily_pose(message.from_user.id)
    if pose:
        daily_text = "🌟 *Поза дня*\n\n" + yoga_manager.format_pose_info(pose)
        await message.answer(
            daily_text,
            reply_markup=get_pose_keyboard(pose['id']),
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Не удалось получить позу дня. Попробуйте позже.")

# Обработчики кнопок
@dp.message(F.text == "🧘 Поза дня")
async def daily_pose_handler(message: types.Message):
    """Обработчик кнопки 'Поза дня'"""
    await cmd_daily_pose(message)

@dp.message(F.text == "📚 Каталог поз")
async def catalog_handler(message: types.Message):
    """Обработчик кнопки 'Каталог поз'"""
    await message.answer(
        "📚 *Каталог поз йоги*\n\nВыберите категорию:",
        reply_markup=get_categories_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(F.text == "📊 Мой прогресс")
async def progress_handler(message: types.Message):
    """Обработчик кнопки 'Мой прогресс'"""
    await cmd_progress(message)

@dp.message(F.text == "⚙️ Настройки")
async def settings_handler(message: types.Message):
    """Обработчик кнопки 'Настройки'"""
    await cmd_settings(message)

@dp.message(F.text == "ℹ️ Помощь")
async def help_handler(message: types.Message):
    """Обработчик кнопки 'Помощь'"""
    await cmd_help(message)

@dp.message(F.text == "🎯 Рекомендации")
async def recommendations_handler(message: types.Message):
    """Обработчик кнопки 'Рекомендации'"""
    user = await db.get_user(message.from_user.id)
    if user:
        level = user.get('level', 'beginner')
        poses = await yoga_manager.get_poses_by_difficulty(level)
        
        if poses:
            # Берем первые 3 позы как рекомендации
            recommended_poses = poses[:3]
            recommendations_text = f"🎯 *Рекомендации для уровня '{level}'*\n\n"
            
            for i, pose in enumerate(recommended_poses, 1):
                recommendations_text += f"{i}. *{pose['name']}*\n"
                if pose.get('description'):
                    recommendations_text += f"   {pose['description'][:100]}...\n\n"
            
            await message.answer(recommendations_text, parse_mode="Markdown")
        else:
            await message.answer("❌ Нет доступных рекомендаций для вашего уровня.")
    else:
        await message.answer("❌ Сначала настройте свой профиль в разделе 'Настройки'.")

# Обработчики callback-запросов
@dp.callback_query(F.data.startswith("category_"))
async def category_callback(callback: types.CallbackQuery):
    """Обработчик выбора категории"""
    category = callback.data.split("_", 1)[1]
    poses = await yoga_manager.get_poses_by_category(category)
    
    if poses:
        category_names = {
            "standing": "Стоячие позы",
            "seated": "Сидячие позы", 
            "on_knees": "Позы на коленях",
            "lying": "Лежачие позы",
            "inversion": "Перевернутые позы",
            "backbend": "Прогибы",
            "forward_bend": "Наклоны вперед",
            "twist": "Скручивания",
            "resting": "Расслабляющие позы",
            "balance": "Позы равновесия"
        }
        
        category_text = f"📂 *{category_names.get(category, category)}*\n\n"
        
        for i, pose in enumerate(poses[:5], 1):  # Показываем первые 5 поз
            category_text += f"{i}. *{pose['name']}*\n"
            if pose.get('description'):
                category_text += f"   {pose['description'][:80]}...\n\n"
        
        if len(poses) > 5:
            category_text += f"... и еще {len(poses) - 5} поз"
        
        await callback.message.edit_text(
            category_text,
            reply_markup=get_categories_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await callback.answer("❌ В этой категории пока нет поз.")

@dp.callback_query(F.data.startswith("difficulty_"))
async def difficulty_callback(callback: types.CallbackQuery):
    """Обработчик выбора уровня сложности"""
    difficulty = callback.data.split("_", 1)[1]
    user_id = callback.from_user.id
    
    await db.update_user_level(user_id, difficulty)
    
    difficulty_names = {
        "beginner": "🟢 Начинающий",
        "intermediate": "🟡 Средний",
        "advanced": "🔴 Продвинутый"
    }
    
    await callback.message.edit_text(
        f"✅ Уровень сложности изменен на: {difficulty_names.get(difficulty, difficulty)}",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_main")]
            ]
        )
    )

@dp.callback_query(F.data == "back_to_main")
async def back_to_main_callback(callback: types.CallbackQuery):
    """Обработчик возврата в главное меню"""
    await callback.message.edit_text(
        "🏠 *Главное меню*\n\nВыберите действие:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "random_pose")
async def random_pose_callback(callback: types.CallbackQuery):
    """Обработчик запроса случайной позы"""
    user = await db.get_user(callback.from_user.id)
    difficulty = user.get('level', 'beginner') if user else 'beginner'
    
    pose = await yoga_manager.get_random_pose(difficulty=difficulty)
    if pose:
        await show_pose_info_callback(callback, pose)
    else:
        await callback.answer("❌ Не удалось найти подходящую позу.")

@dp.callback_query(F.data.startswith("rate_"))
async def rate_pose_callback(callback: types.CallbackQuery):
    """Обработчик оценки позы"""
    pose_id = int(callback.data.split("_", 1)[1])
    
    # Создаем клавиатуру с оценками
    rating_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐", callback_data=f"rating_{pose_id}_1"),
                InlineKeyboardButton(text="⭐⭐", callback_data=f"rating_{pose_id}_2"),
                InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"rating_{pose_id}_3"),
                InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data=f"rating_{pose_id}_4"),
                InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data=f"rating_{pose_id}_5")
            ],
            [InlineKeyboardButton(text="🔙 Назад", callback_data=f"pose_{pose_id}")]
        ]
    )
    
    await callback.message.edit_text(
        "⭐ *Оцените эту позу:*\n\nКак вам понравилась поза?",
        reply_markup=rating_keyboard,
        parse_mode="Markdown"
    )

@dp.callback_query(F.data.startswith("rating_"))
async def rating_submit_callback(callback: types.CallbackQuery):
    """Обработчик отправки оценки"""
    parts = callback.data.split("_")
    pose_id = int(parts[1])
    rating = int(parts[2])
    
    # Записываем оценку в базу данных
    await db.add_user_session(
        user_id=callback.from_user.id,
        pose_id=pose_id,
        duration_seconds=0,  # Пока не отслеживаем время
        rating=rating
    )
    
    await callback.answer(f"✅ Спасибо за оценку! ({rating}/5)")
    
    # Возвращаемся к информации о позе
    pose = await db.get_yoga_pose_by_id(pose_id)
    if pose:
        await show_pose_info_callback(callback, pose)

# Вспомогательные функции
async def show_pose_info(message: types.Message, pose: Dict):
    """Показать информацию о позе"""
    pose_text = yoga_manager.format_pose_info(pose)
    await message.answer(
        pose_text,
        reply_markup=get_pose_keyboard(pose['id']),
        parse_mode="Markdown"
    )

async def show_pose_info_callback(callback: types.CallbackQuery, pose: Dict):
    """Показать информацию о позе через callback"""
    pose_text = yoga_manager.format_pose_info(pose)
    await callback.message.edit_text(
        pose_text,
        reply_markup=get_pose_keyboard(pose['id']),
        parse_mode="Markdown"
    )

# Обработчик неизвестных сообщений
@dp.message()
async def unknown_message(message: types.Message):
    """Обработчик неизвестных сообщений"""
    await message.answer(
        "❓ Не понимаю эту команду. Используйте /help для получения справки.",
        reply_markup=get_main_keyboard()
    )

async def main():
    """Основная функция запуска бота"""
    # Инициализация базы данных
    await db.init_db()
    await yoga_manager.initialize_basic_poses()
    
    logger.info("Бот запущен!")
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
