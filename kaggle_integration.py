"""
Модуль для интеграции с Kaggle API и загрузки данных о йоге
"""

import os
import json
import logging
import asyncio
import aiohttp
from typing import List, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class KaggleDataLoader:
    def __init__(self, kaggle_username: str = None, kaggle_key: str = None):
        self.kaggle_username = kaggle_username
        self.kaggle_key = kaggle_key
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    async def download_yoga_dataset(self, dataset_name: str = "yoga-poses"):
        """
        Загрузка датасета йоги с Kaggle
        Пока что используем моковые данные, так как для реальной интеграции нужен Kaggle API
        """
        try:
            # В реальном проекте здесь был бы код для загрузки с Kaggle
            # Пока создаем моковые данные на основе известных датасетов
            mock_data = await self._create_mock_yoga_data()
            
            # Сохраняем данные в JSON файл
            output_file = self.data_dir / f"{dataset_name}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mock_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Данные сохранены в {output_file}")
            return mock_data
            
        except Exception as e:
            logger.error(f"Ошибка при загрузке данных: {e}")
            return None
    
    async def _create_mock_yoga_data(self) -> List[Dict]:
        """
        Создание моковых данных на основе реальных датасетов йоги
        Основано на Yoga-82 и других открытых датасетах
        """
        return [
            {
                "id": 1,
                "name": "Mountain Pose",
                "sanskrit_name": "Tadasana",
                "category": "standing",
                "difficulty": "beginner",
                "description": "Foundation pose for all standing poses",
                "benefits": ["Improves posture", "Strengthens legs", "Develops balance"],
                "instructions": [
                    "Stand with feet together",
                    "Distribute weight evenly",
                    "Lengthen spine",
                    "Relax shoulders"
                ],
                "duration_seconds": 30,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 2,
                "name": "Tree Pose",
                "sanskrit_name": "Vrikshasana",
                "category": "balance",
                "difficulty": "beginner",
                "description": "Balancing pose on one leg",
                "benefits": ["Improves balance", "Strengthens legs", "Develops focus"],
                "instructions": [
                    "Stand on one leg",
                    "Place other foot on inner thigh",
                    "Bring hands to prayer position",
                    "Focus on a fixed point"
                ],
                "duration_seconds": 45,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 3,
                "name": "Downward Facing Dog",
                "sanskrit_name": "Adho Mukha Svanasana",
                "category": "inversion",
                "difficulty": "beginner",
                "description": "Inverted V-shaped pose",
                "benefits": ["Strengthens arms", "Stretches spine", "Improves circulation"],
                "instructions": [
                    "Start on hands and knees",
                    "Tuck toes under",
                    "Lift hips up and back",
                    "Straighten legs as much as possible"
                ],
                "duration_seconds": 60,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 4,
                "name": "Warrior I",
                "sanskrit_name": "Virabhadrasana I",
                "category": "standing",
                "difficulty": "intermediate",
                "description": "Strong standing pose with lunge",
                "benefits": ["Strengthens legs", "Builds stamina", "Improves balance"],
                "instructions": [
                    "Step one foot forward into lunge",
                    "Bend front knee to 90 degrees",
                    "Keep back leg straight",
                    "Raise arms overhead"
                ],
                "duration_seconds": 45,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 5,
                "name": "Cobra Pose",
                "sanskrit_name": "Bhujangasana",
                "category": "backbend",
                "difficulty": "beginner",
                "description": "Gentle backbend lying down",
                "benefits": ["Strengthens back", "Improves spine flexibility", "Opens chest"],
                "instructions": [
                    "Lie on stomach",
                    "Place palms under shoulders",
                    "Press into hands to lift chest",
                    "Keep elbows close to body"
                ],
                "duration_seconds": 30,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 6,
                "name": "Child's Pose",
                "sanskrit_name": "Balasana",
                "category": "resting",
                "difficulty": "beginner",
                "description": "Restorative kneeling pose",
                "benefits": ["Relaxes body", "Relieves stress", "Stretches hips and back"],
                "instructions": [
                    "Kneel on floor",
                    "Sit back on heels",
                    "Fold forward",
                    "Extend arms or rest by sides"
                ],
                "duration_seconds": 90,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 7,
                "name": "Cat Pose",
                "sanskrit_name": "Marjariasana",
                "category": "on_knees",
                "difficulty": "beginner",
                "description": "Gentle spinal movement on hands and knees",
                "benefits": ["Improves spine flexibility", "Relieves back tension", "Massages organs"],
                "instructions": [
                    "Start on hands and knees",
                    "Inhale: arch back, lift head and tailbone",
                    "Exhale: round spine, tuck chin and tailbone",
                    "Move slowly with breath"
                ],
                "duration_seconds": 60,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 8,
                "name": "Bridge Pose",
                "sanskrit_name": "Setu Bandhasana",
                "category": "backbend",
                "difficulty": "beginner",
                "description": "Gentle backbend lying down",
                "benefits": ["Strengthens glutes", "Opens chest", "Improves circulation"],
                "instructions": [
                    "Lie on back",
                    "Bend knees, feet hip-width apart",
                    "Press feet down to lift hips",
                    "Interlace fingers under body"
                ],
                "duration_seconds": 45,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 9,
                "name": "Lotus Pose",
                "sanskrit_name": "Padmasana",
                "category": "seated",
                "difficulty": "intermediate",
                "description": "Classic meditation pose",
                "benefits": ["Improves posture", "Develops hip flexibility", "Aids meditation"],
                "instructions": [
                    "Sit with legs crossed",
                    "Place each foot on opposite thigh",
                    "Keep spine straight",
                    "Rest hands on knees"
                ],
                "duration_seconds": 120,
                "image_url": None,
                "video_url": None
            },
            {
                "id": 10,
                "name": "Corpse Pose",
                "sanskrit_name": "Shavasana",
                "category": "resting",
                "difficulty": "beginner",
                "description": "Final relaxation pose",
                "benefits": ["Complete relaxation", "Reduces stress", "Restores energy"],
                "instructions": [
                    "Lie on back",
                    "Arms and legs relaxed",
                    "Close eyes",
                    "Focus on breathing"
                ],
                "duration_seconds": 300,
                "image_url": None,
                "video_url": None
            }
        ]
    
    async def load_yoga_data_from_file(self, filename: str = "yoga-poses.json") -> Optional[List[Dict]]:
        """Загрузка данных о йоге из локального файла"""
        try:
            file_path = self.data_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.info(f"Загружено {len(data)} поз из файла {filename}")
                return data
            else:
                logger.warning(f"Файл {filename} не найден")
                return None
        except Exception as e:
            logger.error(f"Ошибка при загрузке файла {filename}: {e}")
            return None
    
    async def get_pose_by_category(self, data: List[Dict], category: str) -> List[Dict]:
        """Получение поз по категории"""
        return [pose for pose in data if pose.get('category') == category]
    
    async def get_pose_by_difficulty(self, data: List[Dict], difficulty: str) -> List[Dict]:
        """Получение поз по уровню сложности"""
        return [pose for pose in data if pose.get('difficulty') == difficulty]
    
    async def search_poses(self, data: List[Dict], query: str) -> List[Dict]:
        """Поиск поз по названию или описанию"""
        query = query.lower()
        results = []
        
        for pose in data:
            if (query in pose.get('name', '').lower() or
                query in pose.get('sanskrit_name', '').lower() or
                query in pose.get('description', '').lower()):
                results.append(pose)
        
        return results
    
    async def get_random_pose(self, data: List[Dict], category: str = None, 
                            difficulty: str = None) -> Optional[Dict]:
        """Получение случайной позы с фильтрацией"""
        import random
        
        filtered_data = data
        
        if category:
            filtered_data = [pose for pose in filtered_data if pose.get('category') == category]
        
        if difficulty:
            filtered_data = [pose for pose in filtered_data if pose.get('difficulty') == difficulty]
        
        return random.choice(filtered_data) if filtered_data else None
    
    async def get_pose_statistics(self, data: List[Dict]) -> Dict:
        """Получение статистики по позам"""
        stats = {
            "total_poses": len(data),
            "by_category": {},
            "by_difficulty": {},
            "average_duration": 0
        }
        
        total_duration = 0
        
        for pose in data:
            # Статистика по категориям
            category = pose.get('category', 'unknown')
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            
            # Статистика по сложности
            difficulty = pose.get('difficulty', 'unknown')
            stats["by_difficulty"][difficulty] = stats["by_difficulty"].get(difficulty, 0) + 1
            
            # Средняя продолжительность
            duration = pose.get('duration_seconds', 0)
            total_duration += duration
        
        if data:
            stats["average_duration"] = total_duration / len(data)
        
        return stats

# Пример использования
async def main():
    """Пример использования KaggleDataLoader"""
    loader = KaggleDataLoader()
    
    # Загружаем моковые данные
    data = await loader.download_yoga_dataset()
    
    if data:
        print(f"Загружено {len(data)} поз")
        
        # Получаем статистику
        stats = await loader.get_pose_statistics(data)
        print(f"Статистика: {stats}")
        
        # Ищем позы по категории
        standing_poses = await loader.get_pose_by_category(data, "standing")
        print(f"Стоячие позы: {len(standing_poses)}")
        
        # Получаем случайную позу
        random_pose = await loader.get_random_pose(data, difficulty="beginner")
        if random_pose:
            print(f"Случайная поза: {random_pose['name']}")

if __name__ == "__main__":
    asyncio.run(main())
