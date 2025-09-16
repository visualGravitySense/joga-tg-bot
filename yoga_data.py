"""
Модуль для работы с данными о йоге
Содержит базовые данные о позах йоги и функции для их обработки
"""

import json
import logging
from typing import List, Dict, Optional
from database import Database

logger = logging.getLogger(__name__)

class YogaDataManager:
    def __init__(self, db: Database):
        self.db = db
    
    async def initialize_basic_poses(self):
        """Инициализация базовых поз йоги"""
        basic_poses = [
            {
                "name": "Поза горы (Тадасана)",
                "sanskrit_name": "Tadasana",
                "category": "standing",
                "difficulty_level": "beginner",
                "description": "Базовая стоячая поза, основа для всех других поз",
                "benefits": "Улучшает осанку, укрепляет ноги, развивает равновесие",
                "instructions": "Встаньте прямо, ноги вместе, руки по бокам. Распределите вес равномерно на обе стопы.",
                "duration_seconds": 30
            },
            {
                "name": "Поза дерева (Врикшасана)",
                "sanskrit_name": "Vrikshasana",
                "category": "standing",
                "difficulty_level": "beginner",
                "description": "Поза равновесия на одной ноге",
                "benefits": "Укрепляет ноги, улучшает равновесие, развивает концентрацию",
                "instructions": "Встаньте на одну ногу, вторую согните и поставьте стопу на внутреннюю часть бедра опорной ноги. Руки сложите в намасте перед грудью.",
                "duration_seconds": 45
            },
            {
                "name": "Поза кошки (Марджариасана)",
                "sanskrit_name": "Marjariasana",
                "category": "on_knees",
                "difficulty_level": "beginner",
                "description": "Поза на четвереньках с прогибом спины",
                "benefits": "Укрепляет позвоночник, улучшает гибкость спины, снимает напряжение",
                "instructions": "Встаньте на четвереньки. На вдохе прогните спину, подняв голову и копчик. На выдохе округлите спину, опустив голову.",
                "duration_seconds": 60
            },
            {
                "name": "Поза ребенка (Баласана)",
                "sanskrit_name": "Balasana",
                "category": "resting",
                "difficulty_level": "beginner",
                "description": "Расслабляющая поза на коленях",
                "benefits": "Расслабляет тело, снимает стресс, растягивает бедра и спину",
                "instructions": "Сядьте на колени, опустите туловище вперед, вытянув руки перед собой. Лбом коснитесь пола.",
                "duration_seconds": 90
            },
            {
                "name": "Поза собаки мордой вниз (Адхо Мукха Шванасана)",
                "sanskrit_name": "Adho Mukha Svanasana",
                "category": "inversion",
                "difficulty_level": "beginner",
                "description": "Перевернутая поза, образующая треугольник",
                "benefits": "Укрепляет руки и ноги, растягивает позвоночник, улучшает кровообращение",
                "instructions": "Встаньте на четвереньки, затем поднимите бедра вверх, выпрямив ноги. Образуйте треугольник телом.",
                "duration_seconds": 60
            },
            {
                "name": "Поза воина I (Вирабхадрасана I)",
                "sanskrit_name": "Virabhadrasana I",
                "category": "standing",
                "difficulty_level": "intermediate",
                "description": "Сильная стоячая поза с выпадом",
                "benefits": "Укрепляет ноги, развивает выносливость, улучшает равновесие",
                "instructions": "Сделайте выпад вперед, задняя нога прямая, передняя согнута под 90 градусов. Руки поднимите вверх.",
                "duration_seconds": 45
            },
            {
                "name": "Поза кобры (Бхуджангасана)",
                "sanskrit_name": "Bhujangasana",
                "category": "backbend",
                "difficulty_level": "beginner",
                "description": "Поза лежа с прогибом спины",
                "benefits": "Укрепляет спину, улучшает гибкость позвоночника, раскрывает грудную клетку",
                "instructions": "Лягте на живот, ладони под плечами. На вдохе поднимите грудь, опираясь на руки.",
                "duration_seconds": 30
            },
            {
                "name": "Поза моста (Сету Бандхасана)",
                "sanskrit_name": "Setu Bandhasana",
                "category": "backbend",
                "difficulty_level": "beginner",
                "description": "Поза лежа с подъемом таза",
                "benefits": "Укрепляет ягодицы и спину, растягивает грудную клетку, улучшает кровообращение",
                "instructions": "Лягте на спину, согните колени. Поднимите таз вверх, образуя мост.",
                "duration_seconds": 45
            },
            {
                "name": "Поза лотоса (Падмасана)",
                "sanskrit_name": "Padmasana",
                "category": "seated",
                "difficulty_level": "intermediate",
                "description": "Классическая медитативная поза",
                "benefits": "Улучшает осанку, развивает гибкость бедер, способствует медитации",
                "instructions": "Сядьте, скрестив ноги, поместив каждую стопу на противоположное бедро. Руки на коленях.",
                "duration_seconds": 120
            },
            {
                "name": "Поза трупа (Шавасана)",
                "sanskrit_name": "Shavasana",
                "category": "resting",
                "difficulty_level": "beginner",
                "description": "Финальная расслабляющая поза",
                "benefits": "Полное расслабление, снятие стресса, восстановление энергии",
                "instructions": "Лягте на спину, руки и ноги свободно. Закройте глаза и полностью расслабьтесь.",
                "duration_seconds": 300
            }
        ]
        
        for pose in basic_poses:
            try:
                await self.db.add_yoga_pose(**pose)
                logger.info(f"Добавлена поза: {pose['name']}")
            except Exception as e:
                logger.error(f"Ошибка при добавлении позы {pose['name']}: {e}")
    
    async def get_poses_by_category(self, category: str) -> List[Dict]:
        """Получение поз по категории"""
        return await self.db.get_yoga_poses(category=category)
    
    async def get_poses_by_difficulty(self, difficulty: str) -> List[Dict]:
        """Получение поз по уровню сложности"""
        return await self.db.get_yoga_poses(difficulty_level=difficulty)
    
    async def get_random_pose(self, category: str = None, 
                            difficulty: str = None) -> Optional[Dict]:
        """Получение случайной позы"""
        import random
        poses = await self.db.get_yoga_poses(category=category, 
                                           difficulty_level=difficulty)
        return random.choice(poses) if poses else None
    
    async def get_daily_pose(self, user_id: int) -> Optional[Dict]:
        """Получение позы дня для пользователя"""
        # Простая логика - можно улучшить на основе предпочтений пользователя
        user = await self.db.get_user(user_id)
        if user:
            difficulty = user.get('level', 'beginner')
            return await self.get_random_pose(difficulty=difficulty)
        return await self.get_random_pose(difficulty='beginner')
    
    def get_categories(self) -> List[str]:
        """Получение списка категорий поз"""
        return [
            "standing",      # Стоячие позы
            "seated",        # Сидячие позы
            "on_knees",      # Позы на коленях
            "lying",         # Лежачие позы
            "inversion",     # Перевернутые позы
            "backbend",      # Прогибы
            "forward_bend",  # Наклоны вперед
            "twist",         # Скручивания
            "resting",       # Расслабляющие позы
            "balance"        # Позы равновесия
        ]
    
    def get_difficulty_levels(self) -> List[str]:
        """Получение уровней сложности"""
        return ["beginner", "intermediate", "advanced"]
    
    def format_pose_info(self, pose: Dict) -> str:
        """Форматирование информации о позе для отправки пользователю"""
        info = f"🧘 *{pose['name']}*\n"
        
        if pose.get('sanskrit_name'):
            info += f"📜 Санскрит: {pose['sanskrit_name']}\n"
        
        if pose.get('category'):
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
            info += f"📂 Категория: {category_names.get(pose['category'], pose['category'])}\n"
        
        if pose.get('difficulty_level'):
            difficulty_names = {
                "beginner": "Начинающий",
                "intermediate": "Средний", 
                "advanced": "Продвинутый"
            }
            info += f"⭐ Уровень: {difficulty_names.get(pose['difficulty_level'], pose['difficulty_level'])}\n"
        
        if pose.get('description'):
            info += f"\n📝 *Описание:*\n{pose['description']}\n"
        
        if pose.get('benefits'):
            info += f"\n💪 *Польза:*\n{pose['benefits']}\n"
        
        if pose.get('instructions'):
            info += f"\n📋 *Инструкции:*\n{pose['instructions']}\n"
        
        if pose.get('duration_seconds'):
            info += f"\n⏱️ *Рекомендуемое время:* {pose['duration_seconds']} секунд"
        
        return info
