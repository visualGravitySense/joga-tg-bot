"""
Дополнительные функции для базы данных Yoga Learning Bot
"""

import sqlite3
import asyncio
import aiosqlite
from typing import List, Dict, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class DatabaseEnhancements:
    def __init__(self, db_path: str = "yoga_bot.db"):
        self.db_path = db_path
    
    async def init_enhanced_tables(self):
        """Инициализация дополнительных таблиц"""
        async with aiosqlite.connect(self.db_path) as db:
            # Таблица избранных поз
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    pose_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (pose_id) REFERENCES yoga_poses (id),
                    UNIQUE(user_id, pose_id)
                )
            """)
            
            # Таблица заметок пользователя
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    pose_id INTEGER,
                    note_text TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (pose_id) REFERENCES yoga_poses (id)
                )
            """)
            
            # Таблица достижений
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    achievement_type TEXT,
                    achievement_name TEXT,
                    description TEXT,
                    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Таблица планов тренировок
            await db.execute("""
                CREATE TABLE IF NOT EXISTS workout_plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    difficulty_level TEXT,
                    duration_minutes INTEGER,
                    poses TEXT,  -- JSON список ID поз
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
            logger.info("Дополнительные таблицы инициализированы")
    
    async def add_to_favorites(self, user_id: int, pose_id: int) -> bool:
        """Добавление позы в избранное"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR IGNORE INTO user_favorites (user_id, pose_id)
                    VALUES (?, ?)
                """, (user_id, pose_id))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка добавления в избранное: {e}")
            return False
    
    async def remove_from_favorites(self, user_id: int, pose_id: int) -> bool:
        """Удаление позы из избранного"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    DELETE FROM user_favorites 
                    WHERE user_id = ? AND pose_id = ?
                """, (user_id, pose_id))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка удаления из избранного: {e}")
            return False
    
    async def get_user_favorites(self, user_id: int) -> List[Dict]:
        """Получение избранных поз пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT yp.*, uf.created_at as favorited_at
                FROM yoga_poses yp
                JOIN user_favorites uf ON yp.id = uf.pose_id
                WHERE uf.user_id = ?
                ORDER BY uf.created_at DESC
            """, (user_id,)) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
    
    async def is_favorite(self, user_id: int, pose_id: int) -> bool:
        """Проверка, является ли поза избранной"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT 1 FROM user_favorites 
                WHERE user_id = ? AND pose_id = ?
            """, (user_id, pose_id)) as cursor:
                return await cursor.fetchone() is not None
    
    async def add_user_note(self, user_id: int, pose_id: int, note_text: str) -> bool:
        """Добавление заметки к позе"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR REPLACE INTO user_notes 
                    (user_id, pose_id, note_text, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (user_id, pose_id, note_text))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка добавления заметки: {e}")
            return False
    
    async def get_user_notes(self, user_id: int, pose_id: int = None) -> List[Dict]:
        """Получение заметок пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            query = """
                SELECT un.*, yp.name as pose_name
                FROM user_notes un
                JOIN yoga_poses yp ON un.pose_id = yp.id
                WHERE un.user_id = ?
            """
            params = [user_id]
            
            if pose_id:
                query += " AND un.pose_id = ?"
                params.append(pose_id)
            
            query += " ORDER BY un.updated_at DESC"
            
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
    
    async def delete_user_notes(self, user_id: int, pose_id: int) -> bool:
        """Удаление заметок пользователя к конкретной позе"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    DELETE FROM user_notes 
                    WHERE user_id = ? AND pose_id = ?
                """, (user_id, pose_id))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка удаления заметок: {e}")
            return False
    
    async def unlock_achievement(self, user_id: int, achievement_type: str, 
                                achievement_name: str, description: str) -> bool:
        """Разблокировка достижения"""
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute("""
                    INSERT OR IGNORE INTO user_achievements 
                    (user_id, achievement_type, achievement_name, description)
                    VALUES (?, ?, ?, ?)
                """, (user_id, achievement_type, achievement_name, description))
                await db.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка разблокировки достижения: {e}")
            return False
    
    async def get_user_achievements(self, user_id: int) -> List[Dict]:
        """Получение достижений пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT * FROM user_achievements 
                WHERE user_id = ?
                ORDER BY unlocked_at DESC
            """, (user_id,)) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
    
    async def check_achievements(self, user_id: int):
        """Проверка и разблокировка достижений"""
        # Получаем статистику пользователя
        progress = await self.get_user_progress(user_id)
        if not progress:
            return
        
        total_sessions = progress.get('total_sessions', 0)
        current_streak = progress.get('current_streak', 0)
        total_duration = progress.get('total_duration', 0)
        
        # Проверяем различные достижения
        achievements_to_check = [
            {
                'type': 'sessions',
                'name': 'Первые шаги',
                'description': 'Завершить первую практику',
                'condition': total_sessions >= 1
            },
            {
                'type': 'sessions',
                'name': 'Новичок',
                'description': 'Завершить 10 практик',
                'condition': total_sessions >= 10
            },
            {
                'type': 'sessions',
                'name': 'Практикующий',
                'description': 'Завершить 50 практик',
                'condition': total_sessions >= 50
            },
            {
                'type': 'sessions',
                'name': 'Мастер йоги',
                'description': 'Завершить 100 практик',
                'condition': total_sessions >= 100
            },
            {
                'type': 'streak',
                'name': 'Постоянство',
                'description': 'Практиковаться 7 дней подряд',
                'condition': current_streak >= 7
            },
            {
                'type': 'streak',
                'name': 'Железная воля',
                'description': 'Практиковаться 30 дней подряд',
                'condition': current_streak >= 30
            },
            {
                'type': 'time',
                'name': 'Час практики',
                'description': 'Практиковаться более 1 часа',
                'condition': total_duration >= 3600
            },
            {
                'type': 'time',
                'name': 'Мастер времени',
                'description': 'Практиковаться более 10 часов',
                'condition': total_duration >= 36000
            }
        ]
        
        # Разблокируем достижения
        for achievement in achievements_to_check:
            if achievement['condition']:
                await self.unlock_achievement(
                    user_id,
                    achievement['type'],
                    achievement['name'],
                    achievement['description']
                )
    
    async def get_user_progress(self, user_id: int) -> Optional[Dict]:
        """Получение прогресса пользователя (копия из основного класса)"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT * FROM user_progress WHERE user_id = ?
            """, (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
    
    async def search_poses(self, query: str, user_id: int = None) -> List[Dict]:
        """Поиск поз по названию"""
        async with aiosqlite.connect(self.db_path) as db:
            search_query = f"%{query.lower()}%"
            async with db.execute("""
                SELECT * FROM yoga_poses 
                WHERE LOWER(name) LIKE ? OR LOWER(sanskrit_name) LIKE ? OR LOWER(description) LIKE ?
                ORDER BY name
            """, (search_query, search_query, search_query)) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
    
    async def get_workout_plans(self, difficulty_level: str = None) -> List[Dict]:
        """Получение планов тренировок"""
        async with aiosqlite.connect(self.db_path) as db:
            query = "SELECT * FROM workout_plans WHERE 1=1"
            params = []
            
            if difficulty_level:
                query += " AND difficulty_level = ?"
                params.append(difficulty_level)
            
            query += " ORDER BY name"
            
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
