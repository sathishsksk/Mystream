import motor.motor_asyncio
import datetime
from typing import List, Dict, Any

class Database:
    def __init__(self, uri: str, database_name: str):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.users = self.db.users
        self.files = self.db.files
        self.streams = self.db.streams
    
    # User Management
    def new_user(self, id: int) -> Dict[str, Any]:
        return {
            "id": id,
            "join_date": datetime.datetime.utcnow(),
            "last_active": datetime.datetime.utcnow(),
            "file_count": 0
        }
    
    async def add_user(self, id: int):
        user = self.new_user(id)
        await self.users.insert_one(user)
    
    async def is_user_exist(self, id: int) -> bool:
        user = await self.users.find_one({'id': id})
        return bool(user)
    
    async def total_users_count(self) -> int:
        return await self.users.count_documents({})
    
    async def get_all_users(self) -> List[int]:
        users = []
        async for user in self.users.find({}):
            users.append(user['id'])
        return users
    
    async def delete_user(self, user_id: int):
        await self.users.delete_many({'id': user_id})
    
    async def update_user_activity(self, user_id: int):
        await self.users.update_one(
            {'id': user_id},
            {'$set': {'last_active': datetime.datetime.utcnow()}}
        )
    
    # File Management
    async def add_file_record(self, file_id: str, file_name: str, file_size: int, 
                            download_link: str, stream_links: Dict = None, user_id: int = None):
        file_record = {
            "file_id": file_id,
            "file_name": file_name,
            "file_size": file_size,
            "download_link": download_link,
            "stream_links": stream_links or {},
            "user_id": user_id,
            "upload_date": datetime.datetime.utcnow(),
            "download_count": 0
        }
        await self.files.insert_one(file_record)
        
        # Update user file count
        if user_id:
            await self.users.update_one(
                {'id': user_id},
                {'$inc': {'file_count': 1}}
            )
    
    async def get_file(self, file_id: str) -> Dict[str, Any]:
        return await self.files.find_one({'file_id': file_id})
    
    async def increment_download_count(self, file_id: str):
        await self.files.update_one(
            {'file_id': file_id},
            {'$inc': {'download_count': 1}}
        )
    
    async def get_user_files(self, user_id: int) -> List[Dict[str, Any]]:
        files = []
        async for file in self.files.find({'user_id': user_id}).sort('upload_date', -1).limit(50):
            files.append(file)
        return files
    
    # Streaming Management
    async def add_stream_record(self, file_id: str, stream_url: str, quality: str = "original"):
        stream_record = {
            "file_id": file_id,
            "stream_url": stream_url,
            "quality": quality,
            "created_at": datetime.datetime.utcnow(),
            "view_count": 0
        }
        await self.streams.insert_one(stream_record)
    
    async def increment_stream_views(self, file_id: str):
        await self.streams.update_one(
            {'file_id': file_id},
            {'$inc': {'view_count': 1}}
        )
