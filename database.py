import sqlite3
import asyncio
import aiosqlite
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "yoga_bot.db"):
        self.db_path = db_path
    
    async def init_db(self):
        """Инициализация базы данных"""
        async with aiosqlite.connect(self.db_path) as db:
            # Таблица пользователей
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    level TEXT DEFAULT 'beginner',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица поз йоги
            await db.execute("""
                CREATE TABLE IF NOT EXISTS yoga_poses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    sanskrit_name TEXT,
                    category TEXT,
                    difficulty_level TEXT,
                    description TEXT,
                    benefits TEXT,
                    instructions TEXT,
                    image_url TEXT,
                    video_url TEXT,
                    duration_seconds INTEGER DEFAULT 30
                )
            """)
            
            # Таблица сессий пользователей
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    pose_id INTEGER,
                    session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    duration_seconds INTEGER,
                    rating INTEGER,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (pose_id) REFERENCES yoga_poses (pose_id)
                )
            """)
            
            # Таблица прогресса пользователей
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    total_sessions INTEGER DEFAULT 0,
                    total_duration INTEGER DEFAULT 0,
                    favorite_poses TEXT,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_session_date TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            await db.commit()
            logger.info("База данных инициализирована")
    
    async def add_user(self, user_id: int, username: str = None, 
                      first_name: str = None, last_name: str = None):
        """Добавление нового пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, last_name, last_activity)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, username, first_name, last_name))
            await db.commit()
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение информации о пользователе"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT * FROM users WHERE user_id = ?
            """, (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
    
    async def update_user_level(self, user_id: int, level: str):
        """Обновление уровня пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE users SET level = ? WHERE user_id = ?
            """, (level, user_id))
            await db.commit()
    
    async def add_yoga_pose(self, name: str, sanskrit_name: str = None,
                           category: str = None, difficulty_level: str = "beginner",
                           description: str = None, benefits: str = None,
                           instructions: str = None, image_url: str = None,
                           video_url: str = None, duration_seconds: int = 30):
        """Добавление новой позы йоги"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO yoga_poses 
                (name, sanskrit_name, category, difficulty_level, description,
                 benefits, instructions, image_url, video_url, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, sanskrit_name, category, difficulty_level, description,
                  benefits, instructions, image_url, video_url, duration_seconds))
            await db.commit()
    
    async def get_yoga_poses(self, category: str = None, 
                           difficulty_level: str = None) -> List[Dict]:
        """Получение поз йоги с фильтрацией"""
        async with aiosqlite.connect(self.db_path) as db:
            query = "SELECT * FROM yoga_poses WHERE 1=1"
            params = []
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            if difficulty_level:
                query += " AND difficulty_level = ?"
                params.append(difficulty_level)
            
            query += " ORDER BY name"
            
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
    
    async def get_yoga_pose_by_id(self, pose_id: int) -> Optional[Dict]:
        """Получение позы йоги по ID"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT * FROM yoga_poses WHERE id = ?
            """, (pose_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
    
    async def add_user_session(self, user_id: int, pose_id: int,
                              duration_seconds: int, rating: int = None,
                              notes: str = None):
        """Добавление сессии пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO user_sessions 
                (user_id, pose_id, duration_seconds, rating, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, pose_id, duration_seconds, rating, notes))
            await db.commit()
    
    async def get_user_progress(self, user_id: int) -> Optional[Dict]:
        """Получение прогресса пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT * FROM user_progress WHERE user_id = ?
            """, (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    columns = [description[0] for description in cursor.description]
                    return dict(zip(columns, row))
                return None
    
    async def update_user_progress(self, user_id: int, total_sessions: int = None,
                                  total_duration: int = None, current_streak: int = None,
                                  longest_streak: int = None):
        """Обновление прогресса пользователя"""
        async with aiosqlite.connect(self.db_path) as db:
            # Проверяем, существует ли запись
            async with db.execute("""
                SELECT id FROM user_progress WHERE user_id = ?
            """, (user_id,)) as cursor:
                exists = await cursor.fetchone()
            
            if exists:
                # Обновляем существующую запись
                query = "UPDATE user_progress SET "
                params = []
                
                if total_sessions is not None:
                    query += "total_sessions = ?, "
                    params.append(total_sessions)
                
                if total_duration is not None:
                    query += "total_duration = ?, "
                    params.append(total_duration)
                
                if current_streak is not None:
                    query += "current_streak = ?, "
                    params.append(current_streak)
                
                if longest_streak is not None:
                    query += "longest_streak = ?, "
                    params.append(longest_streak)
                
                query += "last_session_date = CURRENT_TIMESTAMP WHERE user_id = ?"
                params.append(user_id)
                
                await db.execute(query, params)
            else:
                # Создаем новую запись
                await db.execute("""
                    INSERT INTO user_progress 
                    (user_id, total_sessions, total_duration, current_streak, longest_streak)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, total_sessions or 0, total_duration or 0, 
                      current_streak or 0, longest_streak or 0))
            
            await db.commit()
